const languageMenu = document.querySelector('.lang-menu');
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && languageMenu.open) {
    languageMenu.open = false;
    languageMenu.querySelector('summary').focus();
  }
});
document.addEventListener('click', event => {
  if (!languageMenu.contains(event.target)) languageMenu.open = false;
});
