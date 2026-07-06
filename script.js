const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.main-nav');
if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.textContent = open ? 'Close' : 'Menu';
  });
  nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.textContent = 'Menu';
  }));
}

document.querySelectorAll('[data-newsletter-form]').forEach(form => {
  form.addEventListener('submit', event => {
    event.preventDefault();
    const status = form.parentElement.querySelector('.form-status');
    if (status) status.textContent = 'The FORO Letter is opening soon. Your address has not been stored.';
    form.reset();
  });
});

const contactForm = document.querySelector('[data-contact-form]');
if (contactForm) {
  contactForm.addEventListener('submit', event => {
    event.preventDefault();
    const data = new FormData(contactForm);
    const subject = encodeURIComponent(`[by.foro] ${data.get('topic')} enquiry from ${data.get('name')}`);
    const body = encodeURIComponent(`Name: ${data.get('name')}\nEmail: ${data.get('email')}\nCompany: ${data.get('company') || 'Not provided'}\n\n${data.get('message')}`);
    window.location.href = `mailto:hello@byforo.com?subject=${subject}&body=${body}`;
    const status = contactForm.querySelector('.form-status');
    if (status) status.textContent = 'Your email app should open now. Replace hello@byforo.com in script.js if you use another address.';
  });
}

document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
