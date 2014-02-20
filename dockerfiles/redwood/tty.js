#!/usr/bin/env nodejs

process.title = 'tty.js';

var tty = require('../');

var app = tty.createServer({
  shell: 'bash',
  shellArgs: ['-c', 'redwood /src/redwood.cfg'],
  port: 8000,
  cwd: "/Redwood"
});

app.listen();
