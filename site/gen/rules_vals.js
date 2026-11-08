    var RULES = [
      { n: '01', title: 'Audit first', when: 'Before any quote', color: '#FF5A1F' },
      { n: '02', title: 'Staging, always', when: 'During the build', color: '#19C7B0' },
      { n: '03', title: 'Verified live', when: 'At launch', color: '#8EA2FF' }
    ];
    var ri = S.rule || 0;
    var rulesList = RULES.map(function (r, i) {
      return { n: r.n, title: r.title, when: r.when, sel: i === ri ? 'true' : 'false', style: '--rc:' + r.color,
        pick: function () { self._rp = 0; self.setState({ rule: i }); } };
    });
    var stageStyle = '--rc:' + RULES[ri].color;
