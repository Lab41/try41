#!/usr/bin/env nodejs

process.title = 'tty.js';

var tty = require('../');

var app = tty.createServer({
  shell: 'bash',
  shellArgs: ['-c', 'top'],
  port: 8000
});

app.listen();
