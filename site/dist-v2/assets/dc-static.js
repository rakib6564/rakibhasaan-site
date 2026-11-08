/* dc-static.js — tiny runtime that renders the exported design pages without the design tool.
   Supports {{holes}} in text and attributes, <sc-for list as>, <sc-if value>, on* event holes,
   and a DCLogic base class with state, setState, renderVals and lifecycle hooks. */
(function () {
  'use strict';
  var EVENTS = { onClick: 'click', onInput: 'input', onChange: 'change', onMouseEnter: 'mouseenter', onMouseLeave: 'mouseleave', onSubmit: 'submit', onKeyDown: 'keydown', onFocus: 'focus', onBlur: 'blur' };
  var LOWER = {}; Object.keys(EVENTS).forEach(function (k) { LOWER[k.toLowerCase()] = EVENTS[k]; });
  var BOOL = { selected: 1, checked: 1, disabled: 1, hidden: 1, open: 1, required: 1, readonly: 1, multiple: 1 };
  var HOLE = /\{\{\s*([^}]+?)\s*\}\}/g;

  function DCLogic(props) { this.props = props || {}; this.state = {}; }
  DCLogic.prototype.setState = function (patch) {
    var prev = Object.assign({}, this.state);
    Object.assign(this.state, typeof patch === 'function' ? patch(this.state, this.props) : patch);
    var self = this;
    if (!self.__queued) {
      self.__queued = true;
      self.__prev = prev;
      Promise.resolve().then(function () {
        self.__queued = false;
        var p = self.__prev; self.__prev = null;
        if (self.__render) self.__render();
        if (self.componentDidUpdate) self.componentDidUpdate(self.props, p);
      });
    }
  };
  window.DCLogic = DCLogic;

  function resolve(expr, scope) {
    expr = expr.trim();
    if (expr === 'true') return true;
    if (expr === 'false') return false;
    if (expr === 'null') return null;
    if (/^-?\d+(\.\d+)?$/.test(expr)) return parseFloat(expr);
    var parts = expr.split('.'), v = scope;
    for (var i = 0; i < parts.length; i++) { if (v == null) return undefined; v = v[parts[i]]; }
    return v;
  }
  function str(v) { return v == null || v === false ? '' : String(v); }
  function truthy(v) { return !!v && v !== 'false' && v !== '0'; }

  // Expand the template into plain nodes for one render pass.
  function expand(src, scope, out, handlers) {
    for (var n = src.firstChild; n; n = n.nextSibling) {
      if (n.nodeType === 3) {
        var t = n.data;
        out.appendChild(document.createTextNode(t.indexOf('{{') < 0 ? t : t.replace(HOLE, function (_, e) { return str(resolve(e, scope)); })));
        continue;
      }
      if (n.nodeType !== 1) continue;
      var tag = n.tagName.toLowerCase();
      if (tag === 'sc-for') {
        var listExpr = (n.getAttribute('list') || '').replace(/^\{\{\s*|\s*\}\}$/g, '');
        var list = resolve(listExpr, scope) || [], as = n.getAttribute('as') || 'item';
        for (var i = 0; i < list.length; i++) {
          var s = Object.create(scope); s[as] = list[i]; s[as + 'Index'] = i;
          expand(n, s, out, handlers);
        }
        continue;
      }
      if (tag === 'sc-if') {
        var cond = (n.getAttribute('value') || '').replace(/^\{\{\s*|\s*\}\}$/g, '');
        if (truthy(resolve(cond, scope))) expand(n, scope, out, handlers);
        continue;
      }
      var el = tag.indexOf('dc-') === 0 ? document.createElement(tag.slice(3)) : document.createElementNS(n.namespaceURI, n.localName);
      for (var a = 0; a < n.attributes.length; a++) {
        var at = n.attributes[a], name = at.name, val = at.value;
        if (name.indexOf('hint-') === 0) continue;
        var ev = LOWER[name.toLowerCase()];
        if (ev && val.indexOf('{{') >= 0) {
          var fn = resolve(val.replace(/^\{\{\s*|\s*\}\}$/g, ''), scope);
          if (typeof fn === 'function') { handlers.push(fn); el.setAttribute('data-dc-' + ev, String(handlers.length - 1)); }
          continue;
        }
        if (val.indexOf('{{') >= 0) {
          var whole = /^\{\{[^}]+\}\}$/.test(val.trim());
          var v = whole ? resolve(val.trim().slice(2, -2), scope) : val.replace(HOLE, function (_, e) { return str(resolve(e, scope)); });
          if (BOOL[name.toLowerCase()]) { if (truthy(v)) el.setAttribute(name, ''); continue; }
          if (v == null || v === false) continue;
          val = String(v);
        }
        el.setAttribute(name, val);
      }
      if (tag === 'template') { el.innerHTML = n.innerHTML; out.appendChild(el); continue; }
      expand(n, scope, el, handlers);
      out.appendChild(el);
    }
  }

  // Patch live DOM toward the new render, leaving changes made by page scripts alone
  // (like React: only attributes/text whose rendered value changed are written).
  function mark(node) {
    node.__dc = true;
    if (node.nodeType === 3) { node.__t = node.data; return; }
    if (node.nodeType !== 1) return;
    node.__a = {};
    for (var i = 0; i < node.attributes.length; i++) node.__a[node.attributes[i].name] = node.attributes[i].value;
    syncProps(node);
    for (var c = node.firstChild; c; c = c.nextSibling) mark(c);
  }
  function syncProps(el) {
    var tag = el.tagName;
    if (tag === 'OPTION') el.selected = el.hasAttribute('selected');
    if (tag === 'INPUT' && (el.type === 'checkbox' || el.type === 'radio')) el.checked = el.hasAttribute('checked');
  }
  function same(a, b) { return a.nodeType === b.nodeType && (a.nodeType !== 1 || a.tagName === b.tagName); }
  function patch(old, nw) {
    if (old.nodeType === 3) {
      if (old.__t !== nw.data) { old.data = nw.data; old.__t = nw.data; }
      return;
    }
    var prev = old.__a || {}, next = {}, changed = false, i, name;
    for (i = 0; i < nw.attributes.length; i++) {
      name = nw.attributes[i].name; var v = nw.attributes[i].value; next[name] = v;
      if (prev[name] !== v) { old.setAttribute(name, v); changed = true; }
    }
    for (name in prev) if (!(name in next)) { old.removeAttribute(name); changed = true; }
    old.__a = next;
    if (changed) syncProps(old);
    patchChildren(old, nw);
  }
  function patchChildren(old, nw) {
    var olds = [], c;
    for (c = old.firstChild; c; c = c.nextSibling) if (c.__dc) olds.push(c);
    var news = Array.prototype.slice.call(nw.childNodes);
    // A node whose template content was replaced by a page script (e.g. textContent) is left to that script.
    if (!olds.length && old.firstChild && news.every(function (x) { return x.nodeType === 3; })) return;
    for (var i = 0; i < news.length; i++) {
      var o = olds[i], n = news[i];
      if (o && same(o, n)) { patch(o, n); continue; }
      mark(n);
      if (o) old.replaceChild(n, o);
      else {
        var after = i > 0 ? olds[i - 1] : null, ref = after ? after.nextSibling : old.firstChild;
        old.insertBefore(n, ref);
      }
      olds[i] = n;
    }
    for (var k = news.length; k < olds.length; k++) if (olds[k].parentNode === old) old.removeChild(olds[k]);
  }

  function boot() {
    var tpl = document.getElementById('dc-tpl'), root = document.getElementById('dc-root');
    var src = document.getElementById('dc-src');
    if (!tpl || !root || !src) return;
    var props = {};
    try { props = JSON.parse(src.getAttribute('data-props') || '{}'); } catch (e) {}
    var Comp = (new Function('DCLogic', src.textContent + '\n;return Component;'))(DCLogic);
    var inst = new Comp(props);
    var handlers = [];
    var render = function () {
      var vals = inst.renderVals ? inst.renderVals() : {};
      var frag = document.createDocumentFragment(), hs = [];
      expand(tpl.content, vals, frag, hs);
      handlers = hs;
      if (!root.__mounted) { while (frag.firstChild) { mark(frag.firstChild); root.appendChild(frag.firstChild); } root.__mounted = true; }
      else patchChildren(root, frag);
    };
    inst.__render = render;
    Object.keys(EVENTS).forEach(function (k) {
      var type = EVENTS[k], capture = type === 'mouseenter' || type === 'mouseleave' || type === 'focus' || type === 'blur';
      root.addEventListener(type, function (e) {
        var el = e.target;
        if (capture) { if (el && el.getAttribute && el.hasAttribute('data-dc-' + type)) { var f = handlers[+el.getAttribute('data-dc-' + type)]; if (f) f(e); } return; }
        while (el && el !== root) {
          if (el.getAttribute && el.hasAttribute('data-dc-' + type)) { var h = handlers[+el.getAttribute('data-dc-' + type)]; if (h) h(e); return; }
          el = el.parentNode;
        }
      }, capture);
    });
    render();
    if (inst.componentDidMount) inst.componentDidMount();
    window.addEventListener('pagehide', function () { if (inst.componentWillUnmount) inst.componentWillUnmount(); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
