document.addEventListener('DOMContentLoaded', function() {
  const toggler = document.getElementById('navbarToggler');
  const navMenu = document.getElementById('navMenu');
  const overlay = document.getElementById('navOverlay');
  const navLinks = navMenu.querySelectorAll('a');

  function toggleMenu() {
    toggler.classList.toggle('active');
    navMenu.classList.toggle('active');
    overlay.classList.toggle('active');
    document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
  }

  function closeMenu() {
    toggler.classList.remove('active');
    navMenu.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  toggler.addEventListener('click', toggleMenu);
  overlay.addEventListener('click', closeMenu);

  navLinks.forEach(link => {
    link.addEventListener('click', closeMenu);
  });

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && navMenu.classList.contains('active')) {
      closeMenu();
    }
  });
});
