var makeWsListener = function(path, selector) {
  var ws = new WebSocket('ws://' + location.host + path);

  var last = 0;
  var diff = 0;

  ws.onmessage = function(event) {
    var now = window.performance.now();
    diff    = now - last;
    last    = now;
    var str = JSON.stringify(JSON.parse(event.data), undefined, 2);
    $(selector).text(str);
    $(selector).parent().parent().find('.latency').text(diff.toFixed(2));
  };

  ws.onerror = function(event) {
    var str = JSON.stringify(JSON.parse(event.data), undefined, 2);
    $('#error').text(str);
  }

  return ws;
};

makeWsListener('/ws/raw', '#raw');
makeWsListener('/ws/commands', '#commands');
