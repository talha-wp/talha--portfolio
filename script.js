const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#main-nav');
function closeMenu() {
  toggle.setAttribute('aria-expanded', 'false');
  toggle.setAttribute('aria-label', 'Open navigation');
  nav.classList.remove('open');
}
toggle.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') !== 'true';
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  nav.classList.toggle('open', open);
});
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    toggle.focus();
  }
});
document.addEventListener('click', event => {
  if (!event.target.closest('.site-header')) closeMenu();
});
document.querySelectorAll('[data-service]').forEach(link => {
  link.addEventListener('click', () => {
    const input = [...document.querySelectorAll('input[name="service"]')].find(input => input.value === link.dataset.service);
    if (input) input.checked = true;
  });
});
document.querySelector('#year').textContent = new Date().getFullYear();
document.querySelector('#project-form').addEventListener('submit', event => {
  event.preventDefault();
  const data = new FormData(event.currentTarget);
  const services = data.getAll('service').join(', ') || 'A new project';
  const body = `Hi Talha,\n\n${data.get('message')}\n\nInterested in: ${services}\n\nName: ${data.get('name')}\nEmail: ${data.get('email')}`;
  const emailUrl = `mailto:hello@talha-ali.com?subject=${encodeURIComponent('Project enquiry: ' + services)}&body=${encodeURIComponent(body)}`;
  const status = document.querySelector('#form-status');
  status.textContent = 'Your email draft is ready. Review it in your email app and send when you’re ready. ';
  const retry = document.createElement('a');
  retry.href = emailUrl;
  retry.textContent = 'Open email draft';
  status.appendChild(retry);
  window.location.href = emailUrl;
});
