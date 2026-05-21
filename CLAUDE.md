# Atelier BUHO — Site vitrine

Site vitrine pour l'Atelier BUHO, atelier de tapisserie décorateur situé au 58 rue
Trousseau, 75011 Paris. Fondatrice : Lirayen Rojas-Diaz. Cible : particuliers et
professionnels (architectes d'intérieur, décorateurs).

## État actuel

Prototype statique sur une seule page (`index.html`), 100% autonome (HTML + CSS +
SVG inline, aucune dépendance de build). Les images sont dans `images/`. Le but de
cette phase est d'itérer sur le design, le contenu et les variations.

Phase suivante envisagée (pas encore faite) : migration vers Astro + déploiement
Vercel ou Netlify, avec découpage en pages (Notre histoire, Réalisations, fiches
Prestations). Ne pas migrer sans validation explicite.

## Règles d'écriture (IMPÉRATIF)

Ces règles s'appliquent à TOUT le contenu rédactionnel du site, sans exception :

1. **JAMAIS de tiret cadratin (—) ni demi-cadratin (–).** Utiliser une virgule, un
   deux-points, un point, ou une parenthèse à la place.
2. **JAMAIS d'esperluette (&).** Toujours écrire « et ».
3. Français comme langue principale. Ton sobre, artisanal, haut de gamme, sans
   superlatifs creux.

## Charte graphique

Polices (substituts web des polices propriétaires de la charte) :
- **Display / serif** : Fraunces (variable). Remplace « Nave ».
- **Sans / corps et capitales** : Manrope. Remplace « Bilo » et « Sackers Gothic ».
- Les deux sont chargées via Google Fonts dans le `<head>`.

Couleurs (définies en variables CSS dans `:root`) :
- `--sage` #5f6559 — vert sauge, fond principal
- `--sage-deep` #4a4f44 — sauge foncé, sections contrastées et formulaire
- `--olive-black` #333322 — quasi-noir olive, hero et footer
- `--cream` #ded8c6 — crème, texte sur fond foncé
- `--cream-light` #ece6d4 — crème clair
- `--olive` #bcb794 — olive clair, accents et eyebrows
- `--sage-light` #85918a — sauge clair
- `--tan` #b58f60 — brun chaud, seul accent « chaud » (marqueur carte, hovers)

Logos (PNG transparents, dans `images/logos/`) :
- `buho-logo-nav.png` — version SANS baseline, pour la nav (petite taille)
- `buho-logo-full.png` — version AVEC baseline « TAPISSIER DÉCORATEUR », pour le footer

## Architecture de la page

Ordre des sections (l'ordre du menu doit toujours rester cohérent avec le contenu) :

| Menu              | Ancre           | Contenu                                            |
|-------------------|-----------------|----------------------------------------------------|
| (hero)            | `#top`          | Photo léopard, titre, 2 CTA                        |
| Nos engagements   | `#engagements`  | Manifeste (citation + texte)                       |
| Prestations       | `#prestations`  | 3 savoir-faire (réfection / création / couture)    |
| Réalisations      | `#realisations` | Galerie mosaïque                                   |
| Notre histoire    | `#histoire`     | Portrait de Lirayen                                |
| L'atelier         | `#atelier`      | Infos pratiques (gauche) + carte de Paris (droite) |
| (CTA rendez-vous) | `#contact`      | Formulaire de contact, section dédiée              |

## Informations de contact (factuelles, ne pas inventer)

- Adresse : 58 rue Trousseau, 75011 Paris
- Métro : Ledru-Rollin, Faidherbe-Chaligny
- Horaires : du lundi au samedi, 9h - 18h
- Téléphone : 06 09 26 27 59
- Email : atelier.buho@gmail.com
- SIREN : 937 684 736
- Coordonnées GPS : 48.8538, 2.3795

## Détails techniques notables

- **Typographie responsive** : les classes `.display-*` utilisent `font-variation-settings`
  pour l'axe optical-size (`opsz`) de Fraunces. Sur desktop l'opsz est élevé (120-144,
  calibré grandes tailles). Un media query mobile en FIN de feuille de style réduit
  l'opsz (~32-48) pour que les graisses restent nettes aux petites tailles. Si tu touches
  à la typo, garde cette logique : opsz doit suivre la taille de rendu réelle.

- **Carte de Paris** : SVG inline dans la section `#atelier`. Dessine la silhouette du
  périphérique, les frontières d'arrondissements, la Seine, et surligne le 11e en `--tan`
  avec un marqueur animé sur l'atelier. Style inspiré des cartes minimalistes type « Alfred ».
  Couleurs codées en dur (hex) dans le SVG car les variables CSS ne sont pas toujours
  fiables dans les attributs SVG selon le contexte.

- **Alignement carte** : le bas de la carte est aligné avec le trait sous l'email via
  `align-self: stretch` sur `.atelier-map` + `.info-list { margin-bottom: 0 }`.

- **SEO / GEO** : un bloc JSON-LD `LocalBusiness` est présent dans le `<head>` (Schema.org).
  À maintenir à jour si les infos changent. Le site vise un bon référencement classique
  ET une bonne lisibilité par les moteurs génératifs (LLM).

- **Pas de framework, pas de build** : tout est dans `index.html`. On peut l'ouvrir
  directement dans un navigateur, ou le servir en local (voir README).

## Conventions pour les variations

Quand on me demande des variations de design :
- Créer une copie nommée explicitement (ex. `index-variation-dark.html`,
  `index-hero-b.html`) plutôt qu'écraser `index.html`.
- Toujours respecter les couleurs de la charte et les règles d'écriture.
- Tester le rendu desktop ET mobile (les deux doivent rester nets).
