// (function loop() {
//   $.get('/raw').then(function(res) {
//     res = JSON.stringify(res, undefined, 2);
//     $('#raw').text(res);
//     setTimeout(loop, 20);
//   }).fail(function(err) {
//     $('#error').text(JSON.stringify(err, undefined, 2));
//     setTimeout(loop, 20);
//   });
// })();

// (function loop() {
//   $.get('/what-should-i-do?').then(function(res) {
//     res = JSON.stringify(res, undefined, 2);
//     $('#commands').text(res);
//     setTimeout(loop, 20);
//   }).fail(function(err) {
//     $('#error').text(JSON.stringify(err, undefined, 2));
//     setTimeout(loop, 20);
//   });
// })();

var wsRaw = new WebSocket('ws://' + location.host + '/ws/raw');

wsRaw.onmessage = function(event) {
  var str = JSON.stringify(JSON.parse(event.data), undefined, 2);
  $('#raw').text(str);
};

wsRaw.onerror = function(event) {
  var str = JSON.stringify(JSON.parse(event.data), undefined, 2);
  $('#error').text(str);
}

var wsCommands = new WebSocket('ws://' + location.host + '/ws/commands');

wsCommands.onmessage = function(event) {
  var str = JSON.stringify(JSON.parse(event.data), undefined, 2);
  $('#commands').text(str);
};

wsCommands.onerror = function(event) {
  var str = JSON.stringify(JSON.parse(event.data), undefined, 2);
  $('#error').text(str);
}
