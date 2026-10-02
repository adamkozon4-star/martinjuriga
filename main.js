// Dopyty chodia na tento e-mail cez formsubmit.co (zadarmo, bez registrácie).
// Prvý odoslaný dopyt pošle na e-mail potvrdzovaciu správu, Martin ju raz potvrdí.
// Ak by sa neskôr použil web3forms.com, stačí vyplniť WEB3FORMS_KEY.
const FORM_EMAIL = 'martin.juriga@merucompany.sk';
const WEB3FORMS_KEY = '';
const PHONE = '+421 915 448 705';

const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];

/* ---------- header a mobilné menu ---------- */
const header = $('.header');
const burger = $('.burger');
const mobileBar = $('.mobile-bar');

const onScroll = () => {
  const y = window.scrollY;
  header.classList.toggle('is-scrolled', y > 20);
  mobileBar.classList.toggle('is-visible', y > window.innerHeight * 0.7);
};
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

burger.addEventListener('click', () => {
  const open = header.classList.toggle('menu-open');
  burger.setAttribute('aria-expanded', open);
});
$$('.nav a').forEach((a) => a.addEventListener('click', () => {
  header.classList.remove('menu-open');
  burger.setAttribute('aria-expanded', 'false');
}));

/* ---------- postupné zobrazovanie ---------- */
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (!e.isIntersecting) return;
    e.target.classList.add('is-in');
    io.unobserve(e.target);
  });
}, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

// súrodencom v jednej mriežke pridáme malé oneskorenie
$$('.reveal').forEach((el) => {
  const siblings = $$(':scope > .reveal', el.parentElement);
  const i = siblings.indexOf(el);
  if (i > 0) el.style.transitionDelay = `${Math.min(i, 6) * 80}ms`;
  io.observe(el);
});

/* ---------- postup: linka sa plní pri scrollovaní ---------- */
const steps = $('.steps');
const stepItems = $$('.step');
const updateSteps = () => {
  const r = steps.getBoundingClientRect();
  const vh = window.innerHeight;
  const p = Math.min(1, Math.max(0, (vh * 0.75 - r.top) / (r.height + vh * 0.25)));
  steps.style.setProperty('--p', `${12 + p * 76}%`);
  const active = Math.ceil(p * stepItems.length + 0.2);
  stepItems.forEach((s, i) => s.classList.toggle('is-active', i < active && p > 0));
};
window.addEventListener('scroll', updateSteps, { passive: true });
updateSteps();

/* ---------- životné situácie (záložky) ---------- */
const tabs = $$('.life__tab');
const selectTab = (tab) => {
  tabs.forEach((t) => {
    const on = t === tab;
    t.classList.toggle('is-active', on);
    t.setAttribute('aria-selected', on);
    t.tabIndex = on ? 0 : -1;
    $(`#${t.getAttribute('aria-controls')}`).hidden = !on;
  });
};
tabs.forEach((t, i) => {
  t.addEventListener('click', () => selectTab(t));
  t.addEventListener('keydown', (e) => {
    const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
    if (!d) return;
    const next = tabs[(i + d + tabs.length) % tabs.length];
    selectTab(next);
    next.focus();
  });
});

/* ---------- kalkulačka ---------- */
const eur = (n) => `${Math.round(n).toLocaleString('sk-SK')} €`;
const yearsLabel = (n) => `${n} ${n === 1 ? 'rok' : n < 5 ? 'roky' : 'rokov'}`;
const inputs = { amount: $('#amount'), years: $('#years'), rate: $('#rate') };
const profiles = $$('.profile');
let shown = 0;
let raf;

const animateTo = (target) => {
  cancelAnimationFrame(raf);
  const start = shown;
  const t0 = performance.now();
  const step = (t) => {
    const k = Math.min(1, (t - t0) / 500);
    shown = start + (target - start) * (1 - Math.pow(1 - k, 3));
    $('#r-total').textContent = eur(shown);
    if (k < 1) raf = requestAnimationFrame(step);
  };
  raf = requestAnimationFrame(step);
};

const futureValue = (P, months, r) => (r ? P * ((Math.pow(1 + r, months) - 1) / r) : P * months);

// graf: plná čiara = hodnota investície, prerušovaná = vklady bez úrokov
const drawChart = (P, years, r) => {
  const W = 400, H = 170, top = 10;
  const max = futureValue(P, years * 12, r);
  const pts = [];
  for (let i = 0; i <= 40; i++) {
    const m = (years * 12 * i) / 40;
    const x = (W * i) / 40;
    pts.push([x, H - (futureValue(P, m, r) / max) * (H - top), H - ((P * m) / max) * (H - top)]);
  }
  const line = pts.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)} ${y.toFixed(1)}`).join(' ');
  $('#g-line').setAttribute('d', line);
  $('#g-area').setAttribute('d', `${line} L${W} ${H} L0 ${H} Z`);
  $('#g-dep').setAttribute('d', pts.map(([x, , y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)} ${y.toFixed(1)}`).join(' '));
  $('#g-mid').textContent = `o ${yearsLabel(Math.round(years / 2))}`;
  $('#g-end').textContent = `o ${yearsLabel(years)}`;
};

const setAlloc = (stocks) => {
  $('#alloc-stocks').style.width = `${stocks}%`;
  $('#alloc-s').textContent = `${stocks} %`;
  $('#alloc-b').textContent = `${100 - stocks} %`;
};

const calc = () => {
  const P = +inputs.amount.value;
  const years = +inputs.years.value;
  const r = +inputs.rate.value / 100 / 12;
  const total = futureValue(P, years * 12, r);
  const deposits = P * years * 12;

  Object.values(inputs).forEach((el) => {
    el.style.setProperty('--fill', `${((el.value - el.min) / (el.max - el.min)) * 100}%`);
  });
  $('#o-amount').textContent = eur(P);
  $('#o-years').textContent = yearsLabel(years);
  $('#r-years').textContent = yearsLabel(years);
  $('#o-rate').textContent = `${String(inputs.rate.value).replace('.', ',')} %`;
  $('#r-dep').textContent = eur(deposits);
  $('#r-gain').textContent = eur(total - deposits);
  drawChart(P, years, r);
  animateTo(total);
};

profiles.forEach((btn) => btn.addEventListener('click', () => {
  profiles.forEach((b) => {
    b.classList.toggle('is-active', b === btn);
    b.setAttribute('aria-checked', b === btn);
  });
  inputs.rate.value = btn.dataset.rate;
  setAlloc(+btn.dataset.stocks);
  calc();
}));

// ručná zmena výnosu zruší výber stratégie
inputs.rate.addEventListener('input', () => {
  const match = profiles.find((b) => +b.dataset.rate === +inputs.rate.value);
  profiles.forEach((b) => {
    b.classList.toggle('is-active', b === match);
    b.setAttribute('aria-checked', b === match);
  });
  if (match) setAlloc(+match.dataset.stocks);
});
Object.values(inputs).forEach((el) => el.addEventListener('input', calc));
calc();

/* ---------- referencie ---------- */
// Sem doplň skutočné recenzie od klientov, sekcia sa potom zobrazí sama.
// { text: '…', name: 'Jana K.', place: 'Žilina' }
const REVIEWS = [];

if (REVIEWS.length) {
  const esc = (t) => t.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  $('#reviews-list').innerHTML = REVIEWS.map((r) => `
    <article class="review reveal is-in">
      <span class="review__stars" aria-label="5 z 5 hviezdičiek">★★★★★</span>
      <p>„${esc(r.text)}“</p>
      <footer><span>${esc(r.name.charAt(0))}</span><div><strong>${esc(r.name)}</strong><small>${esc(r.place || '')}</small></div></footer>
    </article>`).join('');
  $('#referencie').hidden = false;
}

/* tlačidlá služieb predvyplnia tému vo formulári */
$$('[data-tema]').forEach((a) => a.addEventListener('click', () => {
  const radio = $(`input[name="tema"][value="${a.dataset.tema}"]`);
  if (radio) radio.checked = true;
}));

/* ---------- formulár ---------- */
const form = $('#contact-form');
const status = $('.form__status', form);

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  status.className = 'form__status';

  const required = $$('[required]', form);
  let ok = true;
  required.forEach((el) => {
    const valid = el.type === 'checkbox' ? el.checked : el.value.trim() !== '';
    el.classList.toggle('is-invalid', !valid);
    if (!valid) ok = false;
  });
  if (!ok) {
    status.textContent = 'Vyplňte prosím meno, telefón a súhlas.';
    status.classList.add('err');
    return;
  }

  const btn = $('button[type="submit"]', form);
  btn.disabled = true;
  status.textContent = 'Odosielam…';
  try {
    const data = Object.fromEntries(new FormData(form));
    if (data.botcheck) throw new Error('spam');
    delete data.botcheck;
    let ok;
    if (WEB3FORMS_KEY) {
      data.access_key = WEB3FORMS_KEY;
      const res = await fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(data),
      });
      ok = (await res.json()).success;
    } else {
      const res = await fetch(`https://formsubmit.co/ajax/${FORM_EMAIL}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ ...data, _subject: data.subject || 'Nový dopyt z webu', _template: 'table', _captcha: 'false' }),
      });
      const json = await res.json();
      ok = json.success === true || json.success === 'true';
    }
    if (!ok) throw new Error('send failed');
    form.reset();
    status.textContent = 'Ďakujem! Ozvem sa vám do 24 hodín.';
    status.classList.add('ok');
  } catch {
    status.textContent = `Niečo sa nepodarilo. Zavolajte mi prosím na ${PHONE}.`;
    status.classList.add('err');
  } finally {
    btn.disabled = false;
  }
});
$$('input', form).forEach((el) => el.addEventListener('input', () => el.classList.remove('is-invalid')));

/* ---------- počítadlá čísel ---------- */
const counters = $$('[data-count]');
const countIO = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (!e.isIntersecting) return;
    countIO.unobserve(e.target);
    const el = e.target;
    const target = +el.dataset.count;
    const suffix = el.dataset.suffix || '';
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const t0 = performance.now();
    const tick = (t) => {
      const k = Math.min(1, (t - t0) / 1400);
      el.textContent = Math.round(target * (1 - Math.pow(1 - k, 3))) + suffix;
      if (k < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  });
}, { threshold: 0.6 });
counters.forEach((c) => countIO.observe(c));

$('#year').textContent = new Date().getFullYear();
