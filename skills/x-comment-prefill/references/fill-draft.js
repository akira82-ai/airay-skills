/* Page-context helpers for locating and verifying X's reply editor.
 * Run inside page.evaluate() (paste the file body into the callback).
 * Writing is delegated to ego lite's real keyboard path:
 * click the box, then one keyboard.paste() / keyboard.insertText().
 */

var XCP_EDITOR_SELECTORS = [
  'div[data-testid="tweetTextarea_0"][role="textbox"]',
  'div[role="dialog"] [contenteditable="true"][role="textbox"]',
  '[contenteditable="true"][role="textbox"][aria-label*="Reply"]',
  '[contenteditable="true"][role="textbox"][aria-label*="回复"]'
];

function xcpNormalize(value) {
  return String(value == null ? '' : value).replace(/\r\n?/g, '\n');
}

function xcpVisibleEditable(el) {
  if (!el || el.getAttribute('aria-disabled') === 'true' ||
      el.getAttribute('contenteditable') !== 'true') return false;
  return el.offsetParent !== null && el.getClientRects().length > 0;
}

function xcpEditors() {
  var seen = [];
  XCP_EDITOR_SELECTORS.forEach(function (selector) {
    document.querySelectorAll(selector).forEach(function (el) {
      if (seen.indexOf(el) === -1 && xcpVisibleEditable(el)) seen.push(el);
    });
  });
  return seen;
}

function xcpEditor() {
  var editors = xcpEditors();
  return editors.length === 1 ? editors[0] : null;
}

function xcpReadState() {
  var editors = xcpEditors();
  if (editors.length !== 1) {
    return JSON.stringify({ ok: false, reason: editors.length ? 'ambiguous_editor' : 'no_editor', count: editors.length });
  }
  var el = editors[0];
  return JSON.stringify({
    ok: true,
    selector: el.getAttribute('data-testid') === 'tweetTextarea_0'
      ? 'div[data-testid="tweetTextarea_0"][role="textbox"]'
      : 'dialog-or-accessible-textbox',
    text: xcpNormalize(el.innerText),
    contenteditable: el.getAttribute('contenteditable'),
    ariaDisabled: el.getAttribute('aria-disabled') || 'false'
  });
}

function xcpIsEmpty(el) {
  // X renders a placeholder line ("…") inside an empty editor: innerText can
  // be "\n" while textContent is empty and no real text node exists.
  var text = (el.textContent || '').replace(/\s+/g, '');
  var hasFragment = !!el.querySelector('[data-text-fragment]');
  return text === '' && !hasFragment;
}

function xcpPrepare(expected) {
  if (typeof expected !== 'string' || expected.length === 0) {
    return JSON.stringify({ ok: false, reason: 'empty_draft' });
  }
  var state = JSON.parse(xcpReadState());
  if (!state.ok) return JSON.stringify(state);
  var el = xcpEditor();
  var empty = el ? xcpIsEmpty(el) : false;
  var text = xcpNormalize(state.text);
  var target = xcpNormalize(expected);
  return JSON.stringify({
    ok: true,
    decision: empty ? 'empty' :
      (text === target ? 'already_correct' : 'prefill_conflict'),
    state: state
  });
}

function xcpVerify(expected) {
  var state = JSON.parse(xcpReadState());
  if (!state.ok) return JSON.stringify(state);
  var target = xcpNormalize(expected);
  return JSON.stringify({ ok: true, exact: state.text === target, text: state.text, expected: target });
}
