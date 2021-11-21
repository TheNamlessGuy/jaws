window.addEventListener('load', () => {
  const searchInput = document.getElementById('search-page-search-input');
  searchInput.addEventListener('keyup', (e) => {
    if (e.keyCode === 13) { // Enter
      Helpers.search(searchInput.value);
    }
  });

  document.getElementById('search-page-search-button').addEventListener('click', () => Helpers.search(searchInput.value));
});
