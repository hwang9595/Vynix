const csrf = document.querySelector('meta[name="csrf"]').content;
const $ = (sel) => document.querySelector(sel);

/* ================= ПЛЕЕР ================= */
const audio = new Audio();
audio.volume = 0.8;
let queue = [];      // список треков, которые сейчас по порядку играют
let current = -1;    // индекс текущего трека в очереди

const ui = {
  title: $('#p-title'), artist: $('#p-artist'), cover: $('#p-cover'),
  play: $('#p-play'), prev: $('#p-prev'), next: $('#p-next'),
  seek: $('#p-seek'), time: $('#p-time'), vol: $('#p-vol'),
};

function fmt(sec) {
  sec = Math.floor(sec || 0);
  return Math.floor(sec / 60) + ':' + String(sec % 60).padStart(2, '0');
}

function playAt(i) {
  if (i < 0 || i >= queue.length) return;
  current = i;
  const t = queue[i];
  audio.src = t.audio;
  audio.play().catch(() => {});
  ui.title.textContent = t.title;
  ui.artist.textContent = t.artist;
  ui.cover.src = t.cover || '';
  document.querySelectorAll('.track-card').forEach((c) =>
    c.classList.toggle('playing', c.dataset.id === t.id)
  );
}

ui.play.onclick = () => {
  if (!audio.src) return;
  audio.paused ? audio.play() : audio.pause();
};
ui.next.onclick = () => playAt(current + 1);
ui.prev.onclick = () => playAt(current - 1);
ui.vol.oninput = () => (audio.volume = ui.vol.value);
ui.seek.oninput = () => {
  if (audio.duration) audio.currentTime = (ui.seek.value / 100) * audio.duration;
};

audio.onplay = () => (ui.play.textContent = '⏸');
audio.onpause = () => (ui.play.textContent = '▶');
audio.onended = () => playAt(current + 1);     // автопереход к следующему
audio.ontimeupdate = () => {
  if (!audio.duration) return;
  ui.seek.value = (audio.currentTime / audio.duration) * 100;
  ui.time.textContent = fmt(audio.currentTime);
};

// Клик по карточке = играть. Очередь = все карточки из этого же контейнера.
document.addEventListener('click', (e) => {
  const card = e.target.closest('.track-card');
  if (!card || e.target.closest('.add-btn, .remove-form')) return;
  const cards = [...card.parentElement.querySelectorAll(':scope > .track-card')];
  queue = cards.map((c) => ({ ...c.dataset }));
  playAt(cards.indexOf(card));
});

/* ================= СЛАЙДЕР ================= */
document.querySelectorAll('.slider').forEach((slider) => {
  const track = slider.querySelector('.slider-track');
  slider.querySelector('.prev').onclick = () =>
    track.scrollBy({ left: -600, behavior: 'smooth' });
  slider.querySelector('.next').onclick = () =>
    track.scrollBy({ left: 600, behavior: 'smooth' });
});

/* ================= ПОИСК ================= */
const input = $('#search-input');
const results = $('#search-results');
let timer;

function esc(s) {   // защита от XSS: данные приходят из внешнего API
  return String(s ?? '').replace(/[&<>"']/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[c]));
}

function cardHTML(t) {
  const addBtn = input.dataset.addUrl
    ? '<button class="add-btn" title="В плейлист">+</button>' : '';
  return `
    <div class="track-card" data-id="${esc(t.id)}" data-title="${esc(t.title)}"
         data-artist="${esc(t.artist)}" data-album="${esc(t.album)}"
         data-cover="${esc(t.cover)}" data-audio="${esc(t.audio)}"
         data-duration="${esc(t.duration)}">
      <img src="${esc(t.cover)}" alt="" loading="lazy">
      <div class="info"><b>${esc(t.title)}</b><span>${esc(t.artist)}</span></div>
      ${addBtn}
    </div>`;
}

async function search(q) {
  if (q.length < 2) { results.innerHTML = ''; return; }
  results.innerHTML = '<p class="muted">Ищем…</p>';
  try {
    const res = await fetch(input.dataset.url + '?q=' + encodeURIComponent(q));
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Ошибка');
    results.innerHTML = data.results.length
      ? data.results.map(cardHTML).join('')
      : '<p class="muted">Ничего не найдено</p>';
  } catch (err) {
    results.innerHTML = `<p class="muted">Ошибка: ${esc(err.message)}</p>`;
  }
}

if (input) {
  input.addEventListener('input', () => {
    clearTimeout(timer);                    // debounce: ждём паузу в наборе
    timer = setTimeout(() => search(input.value.trim()), 400);
  });
}

/* ========== ДОБАВИТЬ ТРЕК В ПЛЕЙЛИСТ ========== */
document.addEventListener('click', async (e) => {
  const btn = e.target.closest('.add-btn');
  if (!btn) return;
  const track = { ...btn.closest('.track-card').dataset };
  const res = await fetch(input.dataset.addUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
    body: JSON.stringify(track),
  });
  btn.textContent = res.ok ? '✓' : '!';
});