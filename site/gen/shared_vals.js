    // ---------- shared: mega menu, full menu, message widget ----------
    var fsList = [
      { n: '01', label: 'Home', href: 'Creative.dc.html', img: '/_blob/e37702657907eb0bc2e36a82f2212ce8', cap: 'Websites built for your industry' },
      { n: '02', label: 'Work', href: 'Work.dc.html', img: '/_blob/3e90a1e3057c56feda9aa00c4dbcdd5f', cap: '250+ sites · 14 countries' },
      { n: '03', label: 'Services', href: 'Services.dc.html', img: '/_blob/b131e2de14c018247fe2c08587aa79d2', cap: 'WordPress, custom code, SEO' },
      { n: '04', label: 'Process', href: 'Process.dc.html', img: '/_blob/3694c109ea579750e33aef9a769d2f94', cap: 'Audit, staging, verified live' },
      { n: '05', label: 'About', href: 'About.dc.html', img: '/_blob/fbba8323ce2532684276bba580d15600', cap: 'Rakib Hasan · designer + developer' },
      { n: '06', label: 'Reviews', href: 'Reviews.dc.html', img: '/_blob/b5ab7d08d5870755f32a3d0a43e7f82a', cap: '5.0 from 101 Fiverr reviews' },
      { n: '07', label: 'FAQ', href: 'FAQ.dc.html', img: '/_blob/286bece3cd0f08b4ad4ec3f69420675b', cap: 'Cost, timelines, ownership' },
      { n: '08', label: 'Contact', href: 'Contact.dc.html', img: '/_blob/611fb132b1dbd5cec1b65c55e0a4ff7d', cap: 'Replies within about an hour' },
      { n: '09', label: 'Free audit', href: 'Audit.dc.html', img: '/_blob/8bad9500d3d698ebbeff8b1348d8df76', cap: 'Top five fixes, free' }
    ];
    X.fsItems = fsList.map(function (it, i) {
      return {
        n: it.n, label: it.label, href: it.href, cap: it.cap,
        style: 'animation-delay: ' + (0.2 + i * 0.05).toFixed(2) + 's; ' + (i === S.fsIdx ? 'color: #FF5A1F' : ''),
        enter: function () { if (self.state.fsIdx !== i) self.setState({ fsIdx: i }); }
      };
    });
    var cur = fsList[S.fsIdx] || fsList[0];
    X.fsImg = cur.img; X.fsCaption = cur.cap;
    X.mega = S.mega; X.megaOpen = S.mega ? 'true' : 'false';
    X.chevron = 'transition: transform 0.3s; transform: rotate(' + (S.mega ? 180 : 0) + 'deg)';
    X.openMega = function () { if (!self.state.mega) self.setState({ mega: true }); };
    X.closeMega = function () { if (self.state.mega) self.setState({ mega: false }); };
    X.toggleMega = function () { self.setState({ mega: !self.state.mega }); };
    X.full = S.full;
    X.openFull = function () { self.setState({ full: true, mega: false, fsIdx: 0, chatOpen: false }); };
    X.closeFull = function () { self.setState({ full: false }); };
    X.sent = S.sent; X.send = function () { self.setState({ sent: true }); };
    X.noop = function (e) { if (e && e.preventDefault) e.preventDefault(); };

    // Live status from Rakib's local time (Dhaka, UTC+6): online 10:00–23:00.
    var now = new Date(), dk = new Date(now.getTime() + now.getTimezoneOffset() * 60000 + 6 * 3600000);
    var hr = dk.getHours(), mn = dk.getMinutes(), online = hr >= 10 && hr < 23;
    X.dhaka = ((hr % 12) || 12) + ':' + (mn < 10 ? '0' : '') + mn + (hr < 12 ? ' AM' : ' PM');
    X.chatStatus = online ? 'Online' : 'Away';
    X.chatDot = 'background:' + (online ? '#22C55E' : '#B8B2A8') + (online ? ';box-shadow:0 0 0 0 rgba(34,197,94,.5);animation:bd-pulse 2s infinite' : '');
    X.chatPromise = online ? "I'm online now and usually reply within the hour." : "I'm away right now, but I'll reply within a few hours of starting work.";
    X.chatVisible = S.chatShown && !S.chatHidden && !S.full;
    X.chatOpen = S.chatOpen; X.chatSent = S.chatSent; X.chatNotSent = !S.chatSent;
    X.chatEcho = S.chatMsg || (S.chatTopic ? 'I need help with: ' + S.chatTopic : 'Hi Rakib!');
    X.toggleChat = function () { self.setState({ chatOpen: !self.state.chatOpen, mega: false }); };
    X.hideChat = function () { self.setState({ chatHidden: true, chatOpen: false }); };
    X.chatTopics = ['New website', 'Redesign', 'SEO audit', 'Custom plugin'].map(function (t) {
      return { label: t, on: S.chatTopic === t ? 'true' : 'false', pick: function () { self.setState({ chatTopic: self.state.chatTopic === t ? '' : t }); } };
    });
    X.chatInput = function (e) { self._chatMsg = e.target.value; };
    X.chatEmail = function (e) { self._chatEmail = e.target.value; };
    X.chatSend = function () {
      var m = (self._chatMsg || '').trim();
      var topic = self.state.chatTopic;
      self.setState({ chatSent: true, chatMsg: (topic ? topic + ': ' : '') + (m || 'Hi Rakib, I would like to talk about my website.') });
    };
    X.mailLabel = S.mailCopied ? 'Copied' : 'Copy email';
    X.copyMail = function () {
      try { navigator.clipboard.writeText('Support@rakibhasaan.com'); } catch (e) {}
      self.setState({ mailCopied: true });
      clearTimeout(self._mailT); self._mailT = setTimeout(function () { self.setState({ mailCopied: false }); }, 2000);
    };
    X.toTop = function () { window.scrollTo({ top: 0, behavior: 'smooth' }); };
