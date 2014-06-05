#!/usr/bin/env nodejs

process.title = 'tty.js';

var express = require('express');
var tty = require('../');

var app = tty.createServer({
  shell: 'bash',
  shellArgs: ['-c', 'redwood /src/redwood.cfg /Redwood/Filters'],
  port: 8000,
  cwd: "/Redwood/reports/output"
});

app.use("/output", express.directory("/Redwood/reports/output"));
app.use("/output", express.static("/Redwood/reports/output"));

app.listen();
