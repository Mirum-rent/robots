/* Plays recorded synthetic events only. No API, Python or trading calls. */
(() => {
  'use strict';
  const el = id => document.getElementById(id);
  let cursor = 0, timer = null;
  const names = {
    intent_saved:'Намерение сохранено до отправки', send_attempt:'Отправка в имитатор',
    response_unknown:'Ответ неизвестен', process_restart:'Восстановление после перезапуска',
    reconciliation_started:'Начата сверка', receipt_found:'Результат найден по ключу',
    receipt_absent:'Результат не найден', state_confirmed:'Состояние подтверждено',
    duplicate_ignored:'Повтор события пропущен', conflict_detected:'Обнаружен конфликт',
    fail_closed:'Действие заблокировано', recovery_started:'Начато восстановление'
  };
  const data = () => window.DEMO_RECORDING || {};
  const getScenario = () => (data().scenarios || []).find(s=>s.id === el('scenario').value);
  function reset() {
    clearTimeout(timer); timer=null; cursor=0; el('trace').replaceChildren();
    el('play').disabled=false; el('play').textContent='Воспроизвести запись ▶';
    el('playback-result').textContent='Выберите сценарий и воспроизведите события.';
  }
  function tick() {
    const scenario=getScenario();
    if(!scenario) {el('playback-result').textContent='Запись ещё не подготовлена. Запуск и отчёт описаны в demo/README.md.';return;}
    const events=scenario.events || [];
    if(cursor>=events.length) {
      el('playback-result').textContent=scenario.result || 'Сценарий завершён. Подробности — в отчёте Python-демо.';
      el('play').disabled=false; el('play').textContent='Воспроизвести заново ↻';timer=null;return;
    }
    const entry=events[cursor++],li=document.createElement('li'),seq=document.createElement('span'),body=document.createElement('div'),title=document.createElement('b'),detail=document.createElement('code');
    seq.className='seq';seq.textContent=String(cursor).padStart(2,'0');
    title.textContent=entry.label || names[entry.event] || entry.event;
    detail.textContent=entry.description || [entry.event,entry.state,entry.intent_id].filter(Boolean).join(' · ');
    body.append(title,detail);li.append(seq,body);el('trace').append(li);el('trace').scrollTop=el('trace').scrollHeight;
    timer=setTimeout(tick,matchMedia('(prefers-reduced-motion: reduce)').matches?80:650);
  }
  el('play').addEventListener('click',()=>{reset();el('play').disabled=true;el('play').textContent='Воспроизведение…';tick();});
  el('reset').addEventListener('click',reset);el('scenario').addEventListener('change',reset);
  const m=data().metrics;
  if(m){el('demo-metrics').replaceChildren();for(const item of m){const s=document.createElement('span'),b=document.createElement('b');b.textContent=item.value;s.append(b,document.createTextNode(item.label));el('demo-metrics').append(s);}}
})();
