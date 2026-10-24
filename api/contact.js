// Kontaktný formulár: prijme dopyt z webu a pošle ho Martinovi e-mailom cez Resend (resend.com).
//
// BEZPEČNOSŤ: e-mail ide VŽDY len na pevné adresy (CONTACT_TO / CONTACT_BCC). Na adresu,
// ktorú zadá návštevník, sa nič neposiela – ide len do reply_to. Automatické potvrdenie
// klientovi bolo vypnuté (10/2026): takýto formulár sa dá zneužiť na rozosielanie e-mailov
// cudzím ľuďom z domény send.peakstudio.sk, čo míňa spoločný limit a kazí reputáciu domény.
// Premenné prostredia (Vercel → Settings → Environment Variables):
//   RESEND_API_KEY  povinné, API kľúč z Resend
//   CONTACT_TO      komu chodia dopyty, viac adries oddeľ čiarkou (predvolene martin.juriga@merucompany.sk)
//   CONTACT_BCC     voliteľné, skrytá kópia, viac adries oddeľ čiarkou
//   CONTACT_FROM    odosielateľ, musí byť z overenej domény v Resend,
//                   tu: "Web Martin Juriga <formular@send.peakstudio.sk>"

const list = (v) => (v || '').split(',').map((a) => a.trim()).filter(Boolean);
const TO = list(process.env.CONTACT_TO || 'martin.juriga@merucompany.sk');
const BCC = list(process.env.CONTACT_BCC);
const FROM = process.env.CONTACT_FROM || 'Web Martin Juriga <onboarding@resend.dev>';
const SITE = 'https://martinjuriga.sk';

const TOPICS = ['Investície', 'Hypotéka', 'Poistenie', 'Dôchodok', 'Rezerva', 'II. a III. pilier', 'Poistenie nehnuteľnosti', 'PZP'];
const PAGES = {
  '/': 'Úvodná stránka',
  '/hypoteky-a-uvery/': 'Hypotéky a úvery',
  '/refinancovanie/': 'Refinancovanie',
  '/skratenie-uveru/': 'Skrátenie úveru',
  '/investovanie/': 'Investovanie',
  '/sporenie-pre-deti/': 'Sporenie pre deti',
  '/dochodok/': 'Dôchodok',
  '/zivotne-poistenie/': 'Životné poistenie',
  '/majetkove-poistenie/': 'Majetkové poistenie',
  '/financny-plan/': 'Finančný plán',
};

// Formulár smie prísť len z týchto webov (prehliadač posiela hlavičku Origin vždy)
const ALLOWED_HOSTS = ['martinjuriga.sk', 'www.martinjuriga.sk', 'localhost:3000'];
const allowedOrigin = (origin) => {
  if (!origin) return false;
  try {
    const host = new URL(origin).host;
    return ALLOWED_HOSTS.includes(host) || host.endsWith('.vercel.app');
  } catch {
    return false;
  }
};

// Brzda: max. 3 odoslania za minútu z jednej IP (v pamäti inštancie – nie tvrdý limit,
// ale naivné zaplavenie z jednej adresy zastaví)
const RATE_LIMIT = 3;
const RATE_WINDOW_MS = 60_000;
const hits = new Map();
function rateLimited(ip) {
  const now = Date.now();
  const recent = (hits.get(ip) || []).filter((t) => now - t < RATE_WINDOW_MS);
  recent.push(now);
  hits.set(ip, recent);
  if (hits.size > 5000) hits.clear();
  return recent.length > RATE_LIMIT;
}

// Typické znaky spamu: odkazy a azbuka (klienti píšu po slovensky/česky)
const LINK_RE = /(https?:\/\/|www\.|\b[a-z0-9-]+\.(buzz|xyz|top|click|link|ru|site|online|shop)\b)/i;
const CYRILLIC_RE = /[\u0400-\u04FF]/;

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clean = (v, max) => (typeof v === 'string' ? v.trim().slice(0, max) : '');

// spoločný rámec e-mailu v štýle webu (tabuľky a inline štýly kvôli e-mailovým programom)
const layout = (inner, footer) => `<!doctype html><html lang="sk"><body style="margin:0;padding:0;background:#f8f6f5">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f8f6f5;padding:24px 12px">
<tr><td align="center">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#ffffff;border-radius:20px;overflow:hidden;font-family:Arial,Helvetica,sans-serif;color:#1c1c1c">
<tr><td style="padding:22px 28px;border-bottom:1px solid #eeeae7">
  <table role="presentation" cellpadding="0" cellspacing="0"><tr>
    <td style="padding-right:12px"><img src="${SITE}/img/email-logo.png?v=2" width="53" height="28" alt="" style="display:block;border:0" /></td>
    <td style="font-size:16px;font-weight:bold;line-height:1.2">Martin Juriga<br /><span style="font-size:10px;font-weight:normal;letter-spacing:2px;color:#7e756d">FINANČNÉ PLÁNOVANIE</span></td>
  </tr></table>
</td></tr>
<tr><td style="padding:28px">${inner}</td></tr>
<tr><td style="padding:18px 28px;background:#fbfaf9;border-top:1px solid #eeeae7;font-size:12px;line-height:1.5;color:#7e756d">${footer}</td></tr>
</table>
</td></tr></table></body></html>`;

const button = (href, label) =>
  `<a href="${href}" style="display:inline-block;background:#e09a5b;color:#ffffff;text-decoration:none;font-weight:bold;font-size:15px;padding:12px 22px;border-radius:999px">${label}</a>`;

async function send(key, payload) {
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!r.ok) throw new Error(`Resend ${r.status}: ${await r.text()}`);
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false, error: 'method' });
  }

  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  if (rateLimited(ip)) return res.status(429).json({ ok: false, error: 'rate' });
  if (!allowedOrigin(req.headers.origin)) return res.status(403).json({ ok: false, error: 'origin' });

  let body = req.body || {};
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch { body = {}; }
  }

  // pole proti spamu: človek ho nevidí, robot ho vyplní
  if (body.botcheck) return res.status(200).json({ ok: true });

  const meno = clean(body.meno, 100);
  const telefon = clean(body.telefon, 40);
  const email = clean(body.email, 120);
  const sprava = clean(body.sprava, 3000);
  const tema = TOPICS.includes(body.tema) ? body.tema : 'Iné';
  const cesta = clean(body.stranka, 200);
  const stranka = PAGES[cesta] || cesta || 'neznáma';

  if (!meno || !telefon || !body.suhlas) return res.status(400).json({ ok: false, error: 'required' });
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return res.status(400).json({ ok: false, error: 'email' });

  // spam (odkazy, azbuka) ticho zahodíme – robotovi tvrdíme, že prešiel
  if ([meno, sprava].some((v) => LINK_RE.test(v) || CYRILLIC_RE.test(v))) {
    console.warn('spam zahodený', { ip });
    return res.status(200).json({ ok: true });
  }

  const key = process.env.RESEND_API_KEY;
  if (!key) return res.status(500).json({ ok: false, error: 'config' });

  // ---------- e-mail pre Martina ----------
  const tel = telefon.replace(/[^\d+]/g, '');
  const pageLink = PAGES[cesta] ? `<a href="${SITE}${esc(cesta)}" style="color:#e09a5b;text-decoration:none">${esc(stranka)}</a>` : esc(stranka);
  const rows = [
    ['Téma', esc(tema), tema],
    ['Meno', esc(meno), meno],
    ['Telefón', `<a href="tel:${esc(tel)}" style="color:#e09a5b;text-decoration:none;font-weight:bold">${esc(telefon)}</a>`, telefon],
    ['E-mail', email ? `<a href="mailto:${esc(email)}" style="color:#e09a5b;text-decoration:none">${esc(email)}</a>` : '–', email || '–'],
    ['Správa', sprava ? esc(sprava) : '–', sprava || '–'],
    ['Odoslané zo stránky', pageLink, stranka],
  ];
  const inner = `
  <p style="margin:0 0 6px;font-size:12px;font-weight:bold;letter-spacing:2px;color:#e09a5b">NOVÝ DOPYT Z WEBU</p>
  <h1 style="margin:0 0 20px;font-size:24px;line-height:1.2">${esc(meno)} – ${esc(tema)}</h1>
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #eeeae7;border-radius:14px;border-collapse:separate">
    ${rows.map(([k, v], i) => `<tr><td style="padding:12px 16px;width:150px;font-size:13px;color:#7e756d;vertical-align:top;${i ? 'border-top:1px solid #f5f2f0;' : ''}">${k}</td><td style="padding:12px 16px;font-size:15px;line-height:1.5;white-space:pre-wrap;${i ? 'border-top:1px solid #f5f2f0;' : ''}">${v}</td></tr>`).join('')}
  </table>
  <p style="margin:24px 0 0">${button(`tel:${esc(tel)}`, `Zavolať ${esc(meno)}`)}</p>
  <p style="margin:16px 0 0;font-size:13px;color:#7e756d">${email ? 'Na tento e-mail môžete odpovedať priamo, odpoveď pôjde klientovi.' : 'Klient nezadal e-mail, ozvite sa mu telefonicky.'}</p>`;
  const text = ['Nový dopyt z webu martinjuriga.sk', '', ...rows.map(([k, , t]) => `${k}: ${t}`)].join('\n');

  try {
    await send(key, {
      from: FROM,
      to: TO,
      ...(BCC.length ? { bcc: BCC } : {}),
      subject: `Nový dopyt: ${tema} – ${meno}`,
      html: layout(inner, `Dopyt prišiel cez kontaktný formulár na <a href="${SITE}" style="color:#7e756d">martinjuriga.sk</a>.`),
      text,
      ...(email ? { reply_to: email } : {}),
    });
  } catch (e) {
    console.error(e);
    return res.status(502).json({ ok: false, error: 'send' });
  }

  return res.status(200).json({ ok: true });
}
