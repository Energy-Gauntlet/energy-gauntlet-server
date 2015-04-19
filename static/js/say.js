[

  'Hello',

  'My name is gil a gan',
  'I am controled using the energy gauntlet',

  'Come at me bro!',
  'Rocky, I love you',
  'I am gil a gan',
  'The last boat I was on, got shipwrecked',
  'We were stranded for what seemed like three seasons',
  'Gee whiz, Professor!',
  'I am the droid you are looking for',

  'Kirkland robotics team',
  'Nice to meet you',

  'Energy Gauntlet',
  'I am controled with a glove'

].forEach(function(text) {
  $('#say-body').append('<form action="/say" method="post"> <input type="text" name="say" value="' + text + '"> <button type="submit">Submit</button></form>');
});
