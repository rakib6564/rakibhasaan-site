    // ---------- Footer name: variable-weight wave, follows the cursor ----------
    var fword = $('bd-fword');
    if (fword) {
      var fl = Array.prototype.slice.call(fword.querySelectorAll('.bd-fwl'));
      var fx = null, fvis = false, ft0 = performance.now();
      if ('IntersectionObserver' in window) {
        var fio = new IntersectionObserver(function (es) { fvis = es[0].isIntersecting; if (fvis) fword.classList.add('bd-in'); }, { threshold: 0.1 });
        fio.observe(fword); self._off.push(function () { fio.disconnect(); });
      } else { fvis = true; fword.classList.add('bd-in'); }
      on(fword, 'pointermove', function (e) { fx = e.clientX; });
      on(fword, 'pointerleave', function () { fx = null; });
      var paint = function (now) {
        if (!self._alive) return;
        if (fvis && !reduced) {
          var t = (now - ft0) / 1000;
          for (var i = 0; i < fl.length; i++) {
            var el = fl[i], w;
            if (fx !== null) {
              var r = el.getBoundingClientRect(), d = Math.abs(fx - (r.left + r.width / 2));
              var k = Math.max(0, 1 - d / 260); w = 200 + 400 * k * k;
            } else {
              var s2 = 0.5 + 0.5 * Math.sin(t * 1.4 - i * 0.6); w = 200 + 260 * Math.pow(s2, 4);
            }
            el.style.fontWeight = w.toFixed(0);
            el.style.transform = 'translateY(' + (-(w - 200) / 400 * 10).toFixed(1) + 'px)';
            el.style.color = w > 380 ? 'var(--accent)' : '';
          }
        }
        self._fraf = requestAnimationFrame(paint);
      };
      self._fraf = requestAnimationFrame(paint);
      self._off.push(function () { cancelAnimationFrame(self._fraf); });
    }

    // ---------- Message widget: peek once, then rotate the status line on hover ----------
    var peekT = setTimeout(function () {
      var c = $('bd-chat'); if (!c) return;
      c.classList.add('bd-peek');
      var u = setTimeout(function () { c.classList.remove('bd-peek'); }, 5200);
      self._off.push(function () { clearTimeout(u); });
    }, 5200);
    self._off.push(function () { clearTimeout(peekT); });
    var lineI = 0;
    var lineT = setInterval(function () {
      var c = $('bd-chat'), ln = $('bd-chat-line');
      if (!c || !ln) return;
      var open = c.classList.contains('bd-peek') || c.matches(':hover') || c.matches(':focus-within');
      if (!open) return;
      var st = ln.getAttribute('data-status') || 'Online', tm = ln.getAttribute('data-time') || '';
      var lines = [st + ' · avg. reply 1 hour', "It's " + tm + ' in Dhaka', 'Ask me about your website', '250+ sites · 14 countries'];
      lineI = (lineI + 1) % lines.length;
      ln.classList.remove('bd-line-in'); void ln.offsetWidth;
      ln.textContent = lines[lineI]; ln.classList.add('bd-line-in');
    }, 2400);
    self._off.push(function () { clearInterval(lineT); });
