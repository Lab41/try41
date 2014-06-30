#!/usr/bin/env nodejs

process.title = 'tty.js';

var express = require('express');
var tty = require('../');

var app = tty.createServer({
  shell: 'rbash',
  port: 8000,
  cwd: "/Hemlock"
});

//app.use("/data", express.directory("/Hemlock/data"));
//app.use("/data", express.static("/Hemlock/data"));
app.use("/kibana", express.directory("/kibana/src"));
app.use("/kibana", express.static("/kibana/src"));

app.listen();
