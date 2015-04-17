[

  'Hello',
  'Come at me bro!',
  'Rocky, I love you',
  'I am Gilligan',
  'The last boat I was on got shipwrecked',
  'Gee whiz, Professor!',
  'I am the droid you are looking for',

  'Kirkland robotics team',
  'Nice to meet you',

  'Energy Gauntlet',
  'I am controlled with a glove'

].forEach(function(text) {
  $('#say-body').append('<form action="/say" method="post"> <input type="text" name="say" value="' + text + '"> <button type="submit">Submit</button></form>');
});
