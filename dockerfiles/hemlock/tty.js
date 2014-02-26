#!/usr/bin/env nodejs

process.title = 'tty.js';

var tty = require('../');

var app = tty.createServer({
  shell: 'rbash',
  port: 8000,
  cwd: "/Hemlock"
});

app.listen();
