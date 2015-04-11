(function loop() {
  $.get('/raw').then(function(res) {
    res = JSON.stringify(res, undefined, 2);
    $('#raw').text(res);
    setTimeout(loop, 200);
  }).fail(function(err) {
    console.error.apply(console, arguments);
    $('#error').text(err);
    setTimeout(loop, 200);
  });
})();

(function loop() {
  $.get('/what-should-i-do?').then(function(res) {
    res = JSON.stringify(res, undefined, 2);
    $('#commands').text(res);
    setTimeout(loop, 200);
  }).fail(function(err) {
    console.error.apply(console, arguments);
    $('#error').text(err);
    setTimeout(loop, 200);
  });
})();

