// Atelier BUHO · V4 · script commun à toutes les pages

// Menu mobile
const header = document.getElementById('site-header');
const toggle = document.getElementById('menu-toggle');
function closeMenu() {
  header.classList.remove('open');
  toggle.setAttribute('aria-expanded', 'false');
  toggle.textContent = 'Menu';
}
toggle.addEventListener('click', () => {
  const open = header.classList.toggle('open');
  toggle.setAttribute('aria-expanded', String(open));
  toggle.textContent = open ? 'Fermer' : 'Menu';
});
document.querySelectorAll('#nav a').forEach(link => link.addEventListener('click', closeMenu));

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
