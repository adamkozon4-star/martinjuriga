// Kontaktný formulár: prijme dopyt z webu, pošle ho Martinovi e-mailom cez Resend (resend.com)
// a klientovi, ak zadal e-mail, pošle krátke potvrdenie.
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
// potvrdenie klientovi ide z rovnakej adresy, ale s Martinovým menom; odpoveď smeruje Martinovi
const FROM_ADDR = (FROM.match(/<([^>]+)>/) || [, FROM])[1];
const CONFIRM_FROM = `Martin Juriga <${FROM_ADDR}>`;
const MARTIN_EMAIL = 'martin.juriga@merucompany.sk';
const PHONE = '+421 915 448 705';
const SITE = 'https://martinjuriga.sk';

const TOPICS = ['Finančný plán', 'Investície', 'Hypotéka', 'Poistenie', 'Dôchodok'];
const PAGES = {
  '/': 'Úvodná stránka',
  '/hypoteky-a-uvery/': 'Hypotéky a úvery',
  '/refinancovanie/': 'Refinancovanie',
  '/investovanie/': 'Investovanie',
  '/sporenie-pre-deti/': 'Sporenie pre deti',
  '/dochodok/': 'Dôchodok',
  '/zivotne-poistenie/': 'Životné poistenie',
  '/majetkove-poistenie/': 'Majetkové poistenie',
  '/financny-plan/': 'Finančný plán',
};

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clean = (v, max) => (typeof v === 'string' ? v.trim().slice(0, max) : '');

// spoločný rámec e-mailu v štýle webu (tabuľky a inline štýly kvôli e-mailovým programom)
const layout = (inner, footer) => `<!doctype html><html lang="sk"><body style="margin:0;padding:0;background:#f8f6f5">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f8f6f5;padding:24px 12px">
<tr><td align="center">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#ffffff;border-radius:20px;overflow:hidden;font-family:Arial,Helvetica,sans-serif;color:#1c1c1c">
<tr><td style="padding:22px 28px;border-bottom:1px solid #eeeae7">
  <table role="presentation" cellpadding="0" cellspacing="0"><tr>
    <td style="padding-right:12px"><img src="${SITE}/img/email-logo.png" width="47" height="28" alt="" style="display:block;border:0" /></td>
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

  // ---------- potvrdenie pre klienta ----------
  // Zámerne bez mena a textu, ktorý klient napísal, aby sa formulár nedal zneužiť na rozosielanie cudzieho obsahu.
  if (email) {
    const confirm = `
    <h1 style="margin:0 0 16px;font-size:24px;line-height:1.25">Ďakujem za vašu správu</h1>
    <p style="margin:0 0 14px;font-size:15px;line-height:1.6">Dobrý deň,</p>
    <p style="margin:0 0 14px;font-size:15px;line-height:1.6">vaša správa na tému <strong>${esc(tema)}</strong> mi prišla. Čoskoro sa vám ozvem a dohodneme si stretnutie, osobne alebo online, ako vám to bude vyhovovať. Prvé stretnutie je zadarmo a nezáväzné.</p>
    <p style="margin:0 0 22px;font-size:15px;line-height:1.6">Ak sa chcete spojiť skôr, zavolajte mi alebo jednoducho odpovedzte na tento e-mail.</p>
    <p style="margin:0 0 24px">${button(`tel:${PHONE.replace(/\s/g, '')}`, `Zavolať ${PHONE}`)}</p>
    <p style="margin:0;font-size:15px;line-height:1.6">S pozdravom<br /><strong>Martin Juriga</strong><br /><span style="color:#7e756d">${MARTIN_EMAIL}</span></p>`;
    const legal = `Martin Juriga, podriadený finančný agent zapísaný v registri NBS pod č. 277707. Tento e-mail ste dostali, pretože ste vyplnili kontaktný formulár na <a href="${SITE}" style="color:#7e756d">martinjuriga.sk</a>. Ak ste ho neodoslali vy, môžete ho ignorovať.`;
    try {
      await send(key, {
        from: CONFIRM_FROM,
        to: [email],
        reply_to: MARTIN_EMAIL,
        subject: 'Ďakujem za správu – Martin Juriga',
        html: layout(confirm, legal),
        text: `Dobrý deň,\n\nvaša správa na tému ${tema} mi prišla. Čoskoro sa vám ozvem a dohodneme si stretnutie, osobne alebo online. Prvé stretnutie je zadarmo a nezáväzné.\n\nAk sa chcete spojiť skôr, zavolajte mi na ${PHONE} alebo odpovedzte na tento e-mail.\n\nS pozdravom\nMartin Juriga\n${MARTIN_EMAIL}\n\nMartin Juriga, podriadený finančný agent zapísaný v registri NBS pod č. 277707.`,
      });
    } catch (e) {
      // dopyt už Martinovi odišiel, chybu potvrdenia len zapíšeme
      console.error('potvrdenie', e);
    }
  }

  return res.status(200).json({ ok: true });
}
