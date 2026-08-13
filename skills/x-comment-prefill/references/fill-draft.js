/*
 * fill-draft.js — reusable Draft.js fill + verify for x-comment-prefill.
 *
 * X's reply box is a Draft.js contenteditable. `bsk fill` (value) and
 * `document.execCommand('insertText')` both desync it (gray button / duplicate
 * text / uneditable box). The only reliable path is a synthetic `textInput`
 * event with a capture-phase preventDefault guard so React/Draft.js applies the
 * edit while the native DOM insertion is cancelled.
 *
 * Usage (inline, because `bsk evaluate` may lack `--file`):
 *   bsk evaluate "$(cat references/fill-draft.js; echo '; xcpFill("DRAFT")')" \
 *       --session <sid> --tab-id <tab>
 *   bsk wait-ms 2000
 *   bsk evaluate "$(cat references/fill-draft.js; echo '; xcpVerify()')" \
 *       --session <sid> --tab-id <tab>
 *
 * Clear step needs a REAL key (Draft.js ignores synthetic deletion), so:
 *   bsk evaluate "$(cat references/fill-draft.js; echo '; xcpSelectAll()')" ...
 *   bsk press 'Backspace' --session <sid> --tab-id <tab>
 *   bsk evaluate "$(cat references/fill-draft.js; echo '; xcpInsert("DRAFT")')" ...
 *
 * All functions return JSON strings so they print cleanly from `bsk evaluate`.
 */

var XCP_SEL = 'div[data-testid="tweetTextarea_0"]';

function xcpEl() {
  return document.querySelector(XCP_SEL);
}

// Focus editor and select all contents (caller follows with a real Backspace).
function xcpSelectAll() {
  var el = xcpEl();
  if (!el) return JSON.stringify({ ok: false, reason: 'no_editor' });
  el.focus();
  var r = document.createRange();
  r.selectNodeContents(el);
  var s = window.getSelection();
  s.removeAllRanges();
  s.addRange(r);
  return JSON.stringify({ ok: true, selected: s.toString().length });
}

// Insert DRAFT through Draft.js only (native insertion cancelled by guard).
function xcpInsert(draft) {
  var el = xcpEl();
  if (!el) return JSON.stringify({ ok: false, reason: 'no_editor' });
  if (typeof draft !== 'string' || draft.length === 0) {
    return JSON.stringify({ ok: false, reason: 'empty_draft' });
  }
  var guard = function (e) { e.preventDefault(); };
  el.addEventListener('textInput', guard, true);
  try {
    var ev = document.createEvent('TextEvent');
    ev.initTextEvent('textInput', true, true, window, draft, 0, 'en-US');
    el.dispatchEvent(ev);
  } finally {
    el.removeEventListener('textInput', guard, true);
  }
  return JSON.stringify({ ok: true, dispatched: draft.length });
}

// Combined clear + insert. Caller must still send a real Backspace after this
// returns ok:true (the selectAll primes the editor for that key).
function xcpFill(draft) {
  var sel = JSON.parse(xcpSelectAll());
  if (!sel.ok) return JSON.stringify(sel);
  return JSON.stringify({ ok: true, step: 'clear_then_press_backspace_then_xcpInsert', sel: sel });
}

// Verify after a ~2s wait for the React re-render. Require ALL THREE.
function xcpVerify() {
  var el = xcpEl();
  if (!el) return JSON.stringify({ ok: false, reason: 'no_editor' });
  var placeholder = document.querySelectorAll('.public-DraftEditorPlaceholder-root').length;
  var btn = document.querySelector('button[data-testid="tweetButtonInline"]');
  var out = {
    ok: true,
    innerText: el.innerText,
    placeholderCount: placeholder,
    buttonDisabled: btn ? btn.disabled : 'no_button',
  };
  out.pass = (out.innerText.trim() !== '' && placeholder === 0 && out.buttonDisabled === false);
  return JSON.stringify(out);
}
