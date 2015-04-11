(function loop() {
  $.get('/raw').then(function(res) {
    res = JSON.stringify(res, undefined, 2);
    $('#raw').text(res);
    setTimeout(loop, 20);
  }).fail(function(err) {
    $('#error').text(JSON.stringify(err, undefined, 2));
    setTimeout(loop, 20);
  });
})();

(function loop() {
  $.get('/what-should-i-do?').then(function(res) {
    res = JSON.stringify(res, undefined, 2);
    $('#commands').text(res);
    setTimeout(loop, 20);
  }).fail(function(err) {
    $('#error').text(JSON.stringify(err, undefined, 2));
    setTimeout(loop, 20);
  });
})();

