keybinding = '''
left = document.getElementsByClassName("btn-left")[0];
right = document.getElementsByClassName("btn-right")[0];
back = document.getElementsByClassName("uq-back")[0];


document.addEventListener("keydown", function(e) {
  switch (e.which) {
    case 37: // left
      e.preventDefault();
      left.click();
      break;
    case 38: // up
      break;
    case 39: // right
      e.preventDefault();
      right.click();
      break;
    case 40: // down
      break;
    case 76: // l
      back.click();
      break;
    default:
      return;
  }
});'''