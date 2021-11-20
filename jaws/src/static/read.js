function edit() {
  Helpers.redirect('/update/' + Helpers.getCurrentUID());
}

function setupHotkeys() {
  document.addEventListener('keyup', (e) => {
    if (e.keyCode === 69) { // E
      edit();
    }
  });
}

window.addEventListener('DOMContentLoaded', () => {
  setupHotkeys();
});
