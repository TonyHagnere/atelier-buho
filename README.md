# Atelier BUHO — site vitrine

Prototype statique d'une page. HTML + CSS + SVG, sans dépendances.

## Voir le site

Le plus simple : double-cliquer sur `index.html` pour l'ouvrir dans ton navigateur.

Pour un rendu plus fidèle (certaines fonctions se comportent mieux via un serveur),
lance un petit serveur local depuis ce dossier :

```bash
# Avec Python (présent par défaut sur Mac)
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

```bash
# Ou avec Node, si installé
npx serve .
```

## Structure

```
buho-site/
├── CLAUDE.md          # Contexte projet, charte, règles (lu par Claude Code)
├── README.md          # Ce fichier
├── index.html         # Le site (tout est dedans : HTML + CSS + SVG)
└── images/
    ├── logos/         # Logos PNG transparents (nav + footer)
    └── optimized/     # Photos (réalisations, portraits, atelier)
```

## Travailler avec Claude Code

Depuis ce dossier, lance `claude` puis demande tes modifications en langage naturel.
Quelques exemples :

- « Crée une variation du hero avec un fond plus sombre, dans index-hero-dark.html »
- « Ajoute une page Réalisations avec une galerie filtrable par type de projet »
- « La carte de Paris : déplace le marqueur de l'atelier, il est légèrement trop au sud »
- « Prépare la migration vers Astro et déploie sur Vercel »

Claude Code lit `CLAUDE.md` automatiquement : il connaît déjà la charte, les règles
d'écriture (jamais de — ni de &) et l'architecture.
