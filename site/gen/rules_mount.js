    // ---------- Three rules: auto-advance while visible, pause on hover ----------
    var rulesEl = $('bd-rules'), ruleVis = false, ruleHold = false;
    self._rp = 0;
    if (rulesEl && !reduced) {
      if ('IntersectionObserver' in window) {
        var rio2 = new IntersectionObserver(function (es) { ruleVis = es[0].isIntersecting; }, { threshold: 0.35 });
        rio2.observe(rulesEl); this._off.push(function () { rio2.disconnect(); });
      } else { ruleVis = true; }
      on(rulesEl, 'pointerenter', function () { ruleHold = true; });
      on(rulesEl, 'pointerleave', function () { ruleHold = false; });
      var ruleT = setInterval(function () {
        if (!ruleVis || ruleHold) return;
        self._rp += 80 / 6500;
        var bar = document.querySelector('#bd-rules .bd-rl[aria-selected="true"] .bd-rl-bar i');
        if (bar) bar.style.transform = 'scaleX(' + Math.min(1, self._rp).toFixed(3) + ')';
        if (self._rp >= 1) { self._rp = 0; self.setState({ rule: ((self.state.rule || 0) + 1) % 3 }); }
      }, 80);
      this._off.push(function () { clearInterval(ruleT); });
    }
