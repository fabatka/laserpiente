// https://stackoverflow.com/a/25621277

$('textarea#answer').each(function () {
  this.style.height = this.scrollHeight + 'px;overflow-y:hidden;'
}).on('input', function () {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
});
