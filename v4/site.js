// Atelier BUHO · V4 · script commun à toutes les pages

// Menu mobile : un panneau plein écran, la page ne défile plus dessous tant qu'il est ouvert
const header = document.getElementById('site-header');
const toggle = document.getElementById('menu-toggle');
function setMenu(open) {
  header.classList.toggle('open', open);
  document.documentElement.classList.toggle('menu-open', open);
  toggle.setAttribute('aria-expanded', String(open));
  toggle.textContent = open ? 'Fermer' : 'Menu';
}
toggle.addEventListener('click', () => setMenu(!header.classList.contains('open')));
document.querySelectorAll('#nav a').forEach(link => link.addEventListener('click', () => setMenu(false)));
document.addEventListener('keydown', event => { if (event.key === 'Escape') setMenu(false); });
// Si la fenêtre repasse en grand format, le menu mobile se referme
window.matchMedia('(min-width: 901px)').addEventListener('change', event => { if (event.matches) setMenu(false); });

// Barre fixe sur mobile (numéro et bouton de devis)
// Elle ne s'affiche que si aucune zone de la page ne propose déjà le bouton et le numéro :
// l'ouverture de l'accueil en haut, le bandeau sombre en bas de chaque page.
const callBar = document.getElementById('call-bar');
if (callBar && 'IntersectionObserver' in window) {
  const zones = document.querySelectorAll('[data-cta-zone]');
  const onScreen = new Set();
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => entry.isIntersecting ? onScreen.add(entry.target) : onScreen.delete(entry.target));
    callBar.classList.toggle('is-visible', onScreen.size === 0);
  }, { rootMargin: '-64px 0px -64px 0px' });
  zones.forEach(zone => observer.observe(zone));
  if (!zones.length) callBar.classList.add('is-visible');
}

// Formulaire de devis (contact.html)
// Deux modes, selon l'attribut data-endpoint du formulaire :
//   - vide (aujourd'hui) : on prépare un email dans la messagerie du visiteur.
//     Les photos ne peuvent pas y être jointes automatiquement, on le lui dit.
//   - renseigné avec l'adresse d'un service de formulaire (Formspree, Web3Forms ou autre) :
//     la demande et les photos partent directement, sans quitter la page.
function mailtoFromForm(form) {
  const data = new FormData(form);
  const photos = form.photos ? form.photos.files.length : 0;
  const body = [
    'Nom : ' + data.get('nom'),
    'Téléphone : ' + (data.get('telephone') || 'non renseigné'),
    'Email : ' + data.get('email'),
    'Type de projet : ' + data.get('projet'),
    '',
    data.get('message')
  ];
  if (photos) body.push('', 'Photos à joindre : ' + photos);
  const subject = 'Demande de devis : ' + data.get('projet');
  return 'mailto:atelier.buho@gmail.com'
    + '?subject=' + encodeURIComponent(subject)
    + '&body=' + encodeURIComponent(body.join('\n'));
}

const form = document.getElementById('quote-form');
if (form) {
  const status = document.getElementById('form-status');
  const say = text => { status.textContent = text; status.hidden = false; };
  form.addEventListener('submit', async event => {
    event.preventDefault();
    const endpoint = form.dataset.endpoint;
    if (endpoint) {
      try {
        const response = await fetch(endpoint, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
        if (!response.ok) throw new Error('envoi refusé');
        form.reset();
        say('Merci, votre demande est bien partie. Nous revenons vers vous sous 48 h ouvrées.');
      } catch (error) {
        say("L'envoi n'a pas abouti. Vous pouvez nous écrire à atelier.buho@gmail.com ou appeler le 06 09 26 27 59.");
      }
      return;
    }
    const photos = form.photos.files.length;
    window.location.href = mailtoFromForm(form);
    say(photos
      ? "Votre messagerie s'ouvre avec la demande déjà rédigée. Ajoutez-y vos photos en pièce jointe avant d'envoyer."
      : "Votre messagerie s'ouvre avec la demande déjà rédigée : il ne reste qu'à l'envoyer.");
  });
}
