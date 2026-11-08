    // ---------- Message widget: appear after a short scroll or 3s, refresh status each minute ----------
    var showChat = function () { if (!self.state.chatShown) self.setState({ chatShown: true }); };
    var chatT = setTimeout(showChat, 3000);
    this._off.push(function () { clearTimeout(chatT); });
    on(window, 'scroll', function () { if (window.scrollY > 320) showChat(); }, { passive: true });
    var tickT = setInterval(function () { self.setState({ tick: (self.state.tick || 0) + 1 }); }, 60000);
    this._off.push(function () { clearInterval(tickT); });
    on(document, 'keydown', function (e) { if (e.key === 'Escape') { if (self.state.chatOpen) self.setState({ chatOpen: false }); if (self.state.mega) self.setState({ mega: false }); if (self.state.full) self.setState({ full: false }); } });
