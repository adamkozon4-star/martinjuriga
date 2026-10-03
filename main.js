// Dopyty z formulára posiela serverová funkcia api/contact.js cez Resend.
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
  if (mobileBar) mobileBar.classList.toggle('is-visible', y > window.innerHeight * 0.7);
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

/* ---------- rozbaľovacie menu Služby ---------- */
$$('.nav__drop').forEach((drop) => {
  const toggle = $('.nav__toggle', drop);
  const setOpen = (open) => {
    drop.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', open);
  };
  toggle.addEventListener('click', (e) => {
    e.stopPropagation();
    setOpen(!drop.classList.contains('is-open'));
  });
  document.addEventListener('click', (e) => { if (!drop.contains(e.target)) setOpen(false); });
  drop.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    setOpen(false);
    toggle.focus();
  });
});

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
const road = $('.road');
const roadTiles = $$('.road__tile');
const wideSteps = matchMedia('(min-width: 901px)');
const updateSteps = () => {
  if (!steps) return;
  const r = steps.getBoundingClientRect();
  const vh = window.innerHeight;
  const p = Math.min(1, Math.max(0, (vh * 0.75 - r.top) / (r.height + vh * 0.25)));
  steps.style.setProperty('--p', `${12 + p * 76}%`);
  const active = Math.ceil(p * stepItems.length + 0.2);
  stepItems.forEach((s, i) => s.classList.toggle('is-active', i < active && p > 0));
  // 3D cesta sa vyfarbuje podľa vlastnej polohy: vrch dosky od 80 % po 30 % výšky obrazovky
  if (road && road.offsetParent) {
    const rr = road.getBoundingClientRect();
    const pr = Math.min(1, Math.max(0, (vh * 0.8 - rr.top) / (vh * 0.5)));
    road.style.setProperty('--p', pr.toFixed(3));
    const on = Math.ceil(pr * roadTiles.length + 0.15);
    roadTiles.forEach((t, i) => t.classList.toggle('is-active', i < on && pr > 0));
    // karty krokov pod cestou svietia spolu so svojou dlaždicou
    // na desktope sú pod doskou karty napojené na dlaždice, na mobile sa kroky rozsvecujú postupne samy
    if (wideSteps.matches) stepItems.forEach((st, i) => st.classList.toggle('is-active', i < on && pr > 0));
  }
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
inputs.rate?.addEventListener('input', () => {
  const match = profiles.find((b) => +b.dataset.rate === +inputs.rate.value);
  profiles.forEach((b) => {
    b.classList.toggle('is-active', b === match);
    b.setAttribute('aria-checked', b === match);
  });
  if (match) setAlloc(+match.dataset.stocks);
});
if (inputs.amount) {
  Object.values(inputs).forEach((el) => el.addEventListener('input', calc));
  calc();
}

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
const status = form && $('.form__status', form);

form?.addEventListener('submit', async (e) => {
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
    data.stranka = location.pathname;
    const res = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(data),
    });
    const ok = res.ok && (await res.json()).ok === true;
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
if (form) $$('input', form).forEach((el) => el.addEventListener('input', () => el.classList.remove('is-invalid')));

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

/* ---------- úvod: paralaxa a svetlo za kurzorom ---------- */
const hero = $('.hero');
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
if (hero && !reduced && matchMedia('(pointer: fine)').matches) {
  const layers = [['.hero__circle', 14], ['.hero__ring', 22], ['.hero__person', 8], ['.years-badge', 34], ['.h-card--chart', 40], ['.h-card--badge', 30], ['.hero__round', 26]]
    .map(([sel, d]) => [$(sel, hero), d]).filter(([el]) => el);
  let raf2;
  hero.addEventListener('mousemove', (e) => {
    cancelAnimationFrame(raf2);
    raf2 = requestAnimationFrame(() => {
      const r = hero.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - 0.5;
      const y = (e.clientY - r.top) / r.height - 0.5;
      layers.forEach(([el, d]) => { el.style.translate = `${(-x * d).toFixed(1)}px ${(-y * d).toFixed(1)}px`; });
      hero.style.setProperty('--mx', `${e.clientX - r.left}px`);
      hero.style.setProperty('--my', `${e.clientY - r.top}px`);
    });
  });
  hero.addEventListener('mouseleave', () => layers.forEach(([el]) => { el.style.translate = ''; }));
}

/* ---------- pozadie s horami: pri scrollovaní sa pomaly posúva až po koniec obrázka ---------- */
const pageBg = $('.page-bg');
if (pageBg) {
  let bgRaf;
  const updBg = () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    pageBg.style.setProperty('--bp', max > 0 ? Math.min(1, scrollY / max).toFixed(4) : 0);
  };
  window.addEventListener('scroll', () => { cancelAnimationFrame(bgRaf); bgRaf = requestAnimationFrame(updBg); }, { passive: true });
  window.addEventListener('resize', updBg);
  updBg();
}

/* ---------- niť medzi výsledkami a sľubom ---------- */
const thread = $('.promise__thread');
if (thread) {
  const upd = () => {
    const r = thread.getBoundingClientRect();
    const vh = window.innerHeight;
    const p = Math.min(1, Math.max(0, (vh * 0.9 - r.top) / (r.height + vh * 0.25)));
    thread.style.setProperty('--p', reduced ? 1 : p.toFixed(3));
  };
  window.addEventListener('scroll', upd, { passive: true });
  upd();
}

const yearEl = $('#year');
if (yearEl) yearEl.textContent = new Date().getFullYear();
