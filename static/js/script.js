(function loop() {
  $.get('/raw').then(function(res) {
    res = JSON.stringify(res, undefined, 2);
    $('#raw').text(res);
    setTimeout(loop, 20);
  }).fail(function(err) {
    console.error.apply(console, JSON.stringify(arguments));
    $('#error').text(err);
    setTimeout(loop, 20);
  });
})();

(function loop() {
  $.get('/what-should-i-do?').then(function(res) {
    res = JSON.stringify(res, undefined, 2);
    $('#commands').text(res);
    setTimeout(loop, 20);
  }).fail(function(err) {
    console.error.apply(console, JSON.stringify(arguments));
    $('#error').text(err);
    setTimeout(loop, 20);
  });
})();

