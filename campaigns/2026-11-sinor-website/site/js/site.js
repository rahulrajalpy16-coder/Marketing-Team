/* Shared behaviour: header Menu disclosure and the Contact form (not connected to anything).
   Nothing here sends data anywhere. No network calls, no storage, no cookies. */
(function () {
  'use strict';

  /* ---------- Menu (below 1024 px) ---------- */
  var btn = document.getElementById('menu-btn');
  var nav = document.getElementById('main-nav');
  if (btn && nav) {
    var setOpen = function (open) {
      nav.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    };
    btn.addEventListener('click', function () {
      setOpen(btn.getAttribute('aria-expanded') !== 'true');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' || btn.getAttribute('aria-expanded') !== 'true') return;
      var inside = nav.contains(document.activeElement);
      if (inside || document.activeElement === btn) {
        setOpen(false);
        btn.focus();
      }
    });
  }

  /* ---------- Contact form ---------- */
  var form = document.getElementById('enquiry-form');
  if (!form) return;

  var TOPICS = ['general', 'dynamic-positioning', 'reference-systems', 'electrical-automation', 'propulsion-thrusters', 'integration', 'upgrades', 'service-support'];
  var topic = form.elements.topic;
  var submit = document.getElementById('submit-btn');
  var summary = document.getElementById('error-summary');
  var summaryList = summary.querySelector('ul');
  var status = document.getElementById('status-panel');
  var message = form.elements.message;
  var counter = document.getElementById('message-count');
  var live = document.getElementById('message-live');
  var submitted = false;
  var wasHigh = false;

  /* Topic from ?topic=, unknown values fall back to General enquiry with no error. */
  var wanted = '';
  try { wanted = new URLSearchParams(window.location.search).get('topic') || ''; } catch (e) { wanted = ''; }
  topic.value = TOPICS.indexOf(wanted) > -1 ? wanted : 'general';

  /* JavaScript has taken over, so the button works (it stays switched off without JavaScript). */
  submit.disabled = false;
  var nojs = document.getElementById('nojs-note');
  if (nojs) nojs.hidden = true;

  var rules = {
    name: function (v) { return v.trim().length >= 2 ? '' : 'Error: Enter your name, at least 2 characters.'; },
    email: function (v) {
      v = v.trim();
      if (!v) return 'Error: Enter your email address.';
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? '' : 'Error: This does not look like an email address. Use the format name@example.com.';
    },
    phone: function (v) {
      v = v.trim();
      if (!v) return '';
      return /^[0-9 +\-()\[\]]{6,20}$/.test(v) ? '' : 'Error: Use only digits, spaces, plus, hyphen and brackets, 6 to 20 characters.';
    },
    message: function (v) {
      if (v.length > 2000) return 'Error: The message is too long. The limit is 2000 characters.';
      return v.trim().length >= 10 ? '' : 'Error: Enter a message of at least 10 characters.';
    }
  };
  var order = ['name', 'email', 'phone', 'message'];

  function describe(el, errId, on) {
    var ids = (el.getAttribute('data-hint') || '').split(' ').filter(Boolean);
    if (on) ids.push(errId);
    el.setAttribute('aria-describedby', ids.join(' '));
  }
  function check(key) {
    var el = form.elements[key];
    var err = document.getElementById(key + '-error');
    var msg = rules[key](el.value);
    if (msg) {
      el.setAttribute('aria-invalid', 'true');
      err.textContent = msg;
      err.hidden = false;
      describe(el, err.id, true);
    } else {
      el.removeAttribute('aria-invalid');
      err.textContent = '';
      err.hidden = true;
      describe(el, err.id, false);
    }
    return msg;
  }

  /* While a pointer is pressed on Send enquiry, blur and change checks are skipped so the layout cannot move
     between mouse down and mouse up (a moved button loses the click). The submit itself still validates everything. */
  var pressing = false;
  var release = function () { pressing = false; };
  submit.addEventListener('pointerdown', function () { pressing = true; });
  submit.addEventListener('mousedown', function () { pressing = true; });
  document.addEventListener('pointerup', release);
  document.addEventListener('pointercancel', release);
  document.addEventListener('mouseup', release);
  order.forEach(function (key) {
    var el = form.elements[key];
    el.addEventListener('blur', function () { if (submitted && !pressing) check(key); });
    el.addEventListener('change', function () { if (submitted && !pressing) check(key); });
  });

  /* Counter: visible from 1800 characters. The live region only speaks when 1800 is crossed and at the limit. */
  message.addEventListener('input', function () {
    var left = Math.max(0, 2000 - message.value.length);
    var high = message.value.length >= 1800;
    counter.hidden = !high;
    counter.textContent = high ? left + ' characters remaining' : '';
    if (high && !wasHigh) live.textContent = left + ' characters remaining';
    if (left === 0) live.textContent = '0 characters remaining';
    if (!high && wasHigh) live.textContent = '';
    wasHigh = high;
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    submitted = true;
    if (TOPICS.indexOf(topic.value) === -1) topic.value = 'general';
    status.hidden = true;
    var problems = [];
    order.forEach(function (key) {
      var msg = check(key);
      if (msg) problems.push({ key: key, msg: msg });
    });
    if (problems.length) {
      summaryList.textContent = '';
      problems.forEach(function (pr) {
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.href = '#' + pr.key;
        a.textContent = pr.msg;
        li.appendChild(a);
        summaryList.appendChild(li);
      });
      summary.hidden = false;
      summary.focus();
      return;
    }
    /* Valid: nothing is sent. Values stay in the fields. Focus moves to the Not sent panel. */
    summary.hidden = true;
    status.hidden = false;
    status.focus();
  });
}());
