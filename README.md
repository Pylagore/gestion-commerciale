# Gestion commerciale – secteur informel (ISE 2 ENSAE)

Application Flask + MySQL pour gérer des catégories de produits et des produits.

## Schéma relationnel
- CATEGORIE_PRODUIT(**id_categorie**, libelle)
- PRODUIT(**id_produit**, designation, prix_vente, #id_categorie)  → FK vers CATEGORIE_PRODUIT

Une catégorie regroupe 0..n produits ; un produit appartient à exactement 1 catégorie. Voir `MCD_schema_relationnel.png` et `schema.sql`.

## Lancer en local
```
pip install -r requirements.txt
cp .env.example .env      # puis remplir avec les paramètres FreeDB
python app.py
```

## Déploiement (Render)
- Build command : `pip install -r requirements.txt`
- Start command : `gunicorn app:app`
- Variables d'environnement : `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `SECRET_KEY`

Aucun mot de passe n'est stocké dans le dépôt (`.env` est dans `.gitignore`).
