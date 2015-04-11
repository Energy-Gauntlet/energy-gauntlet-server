var makeWsListener = function(path, selector) {
  var ws = new WebSocket('ws://' + location.host + path);

  ws.onmessage = function(event) {
    var str = JSON.stringify(JSON.parse(event.data), undefined, 2);
    $(selector).text(str);
  };

  ws.onerror = function(event) {
    var str = JSON.stringify(JSON.parse(event.data), undefined, 2);
    $('#error').text(str);
  }

  return ws;
};

makeWsListener('/ws/raw', '#raw');
makeWsListener('/ws/commands', '#commands');
