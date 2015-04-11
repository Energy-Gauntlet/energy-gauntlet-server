(function loop() {
  $.get('/raw').then(function(res) {
    $('#raw').text(res);
    setTimeout(loop, 100);
  });
})();

(function loop() {
  $.get('/what-should-i-do?').then(function(res) {
    $('#commands').text(res);
    setTimeout(loop, 100);
  });
})();

