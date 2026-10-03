// Kontaktný formulár: prijme dopyt z webu a pošle ho Martinovi e-mailom cez Resend (resend.com).
// Premenné prostredia (Vercel → Settings → Environment Variables):
//   RESEND_API_KEY  povinné, API kľúč z Resend
//   CONTACT_TO      komu chodia dopyty, viac adries oddeľ čiarkou (predvolene martin.juriga@merucompany.sk)
//   CONTACT_BCC     voliteľné, skrytá kópia, viac adries oddeľ čiarkou
//   CONTACT_FROM    odosielateľ, musí byť z overenej domény v Resend,
//                   napr. "Web Martin Juriga <web@martinjuriga.sk>"

const list = (v) => (v || '').split(',').map((a) => a.trim()).filter(Boolean);
const TO = list(process.env.CONTACT_TO || 'martin.juriga@merucompany.sk');
const BCC = list(process.env.CONTACT_BCC);
const FROM = process.env.CONTACT_FROM || 'Web Martin Juriga <onboarding@resend.dev>';
const TOPICS = ['Finančný plán', 'Investície', 'Hypotéka', 'Poistenie', 'Dôchodok'];

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clean = (v, max) => (typeof v === 'string' ? v.trim().slice(0, max) : '');

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
  const stranka = clean(body.stranka, 200);

  if (!meno || !telefon || !body.suhlas) return res.status(400).json({ ok: false, error: 'required' });
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return res.status(400).json({ ok: false, error: 'email' });

  const key = process.env.RESEND_API_KEY;
  if (!key) return res.status(500).json({ ok: false, error: 'config' });

  const rows = [
    ['Téma', tema],
    ['Meno', meno],
    ['Telefón', telefon],
    ['E-mail', email || '–'],
    ['Správa', sprava || '–'],
    ['Stránka', stranka || '–'],
  ];
  const html = `<div style="font-family:Arial,sans-serif;font-size:15px;color:#0b1020">
  <h2 style="margin:0 0 16px">Nový dopyt z webu martinjuriga.sk</h2>
  <table cellpadding="8" style="border-collapse:collapse">${rows
    .map(([k, v]) => `<tr><td style="color:#667085;vertical-align:top">${k}</td><td style="white-space:pre-wrap">${esc(v)}</td></tr>`)
    .join('')}</table>
  <p style="margin-top:20px"><a href="tel:${esc(telefon.replace(/\s+/g, ''))}">Zavolať ${esc(meno)}</a></p>
</div>`;
  const text = rows.map(([k, v]) => `${k}: ${v}`).join('\n');

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: FROM,
        to: TO,
        ...(BCC.length ? { bcc: BCC } : {}),
        subject: `Nový dopyt: ${tema} – ${meno}`,
        html,
        text,
        ...(email ? { reply_to: email } : {}),
      }),
    });
    if (!r.ok) {
      console.error('Resend', r.status, await r.text());
      return res.status(502).json({ ok: false, error: 'send' });
    }
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error('Resend', e);
    return res.status(502).json({ ok: false, error: 'send' });
  }
}
