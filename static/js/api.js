var listeners = [];

//
// function to create web socket listeners
//

var makeWsListener = function(path, selector) {
  var ws;

  var last = 0;

  var status = undefined;

  var messageHandler = function(event) {
    var now  = Date.now();
    var data = JSON.parse(event.data);
    var diff = now - last;
    last     = now;
    var str  = JSON.stringify(data, undefined, 2);
    $(selector).text(str);
    $('.latency' + selector.replace('#', '-')).text(diff.toFixed());
    status = true;
  };

  var erorrHandler = function(event) {
    var str = JSON.stringify(JSON.parse(event.data), undefined, 2);
    $('#error').text(str);
    status = false;
  };

  var closeHandler = function(event) {
    createWs();
    status = false;
  };

  function createWs() {
    ws = new WebSocket('ws://' + location.host + path);
    ws.onmessage = messageHandler;
    ws.onerror   = erorrHandler;
    ws.onclose   = closeHandler;
  };

  createWs();

  var listener = {
    status: function() { return status; },
    type:   'socket'
  };

  listeners.push(listener);

  return listener;
};

var wsRaw      = makeWsListener('/ws/raw', '#raw');
// var wsCommands = makeWsListener('/ws/commands', '#commands');

//
// function to create http listeners
//

var makeHttpListener = function(path, selector) {
  var last = 0;
  var diff = 0;

  var status = undefined;

  (function loop() {
    $.ajax({
      url: path,
      success: function(res) {
        status = true;
        if (selector) { $(selector).text(JSON.stringify(res, undefined, 2)); }
        setTimeout(loop, 200);
      },
      error: function(res) {
        status = false;
        setTimeout(loop, 200);
      }
    })
  })();

  var listener = {
    status: function() { return status; },
    type:   'http'
  };

  listeners.push(listener);

  return listener;
};

var httpRaw      = makeHttpListener('/raw');
var httpCommands = makeHttpListener('/what-should-i-do?', '#commands');

var updateIndicator = function(id, failed, unknown) {
  document.getElementById(id).className = 'status-indicator';
  if      (failed > 0)        { $('#' + id).addClass('api-status-fail'); }
  else if (failed == unknown) { $('#' + id).addClass('api-status-success'); }
};

setInterval(function() {
  var failed  = 0;
  var unknown = 0;

  var failedTyped  = { http: 0, socket: 0 };
  var unknownTyped = { http: 0, socket: 0 };
  for (var i in listeners) {
    var listener = listeners[i];
    if      (listener.status() === false)     { failed++;  failedTyped[listener.type]++;  }
    else if (listener.status() === undefined) { unknown++; unknownTyped[listener.type]++; }
  }

  updateIndicator('api-status',    failed, unknown);
  updateIndicator('http-status',   failedTyped.http, unknownTyped.http);
  updateIndicator('socket-status', failedTyped.socket, unknownTyped.socket);

}, 200);
