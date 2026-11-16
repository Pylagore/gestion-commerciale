# Guide personnalisé – TP Gestion commerciale (ISE 2)

Vos paramètres FreeDB (déjà renseignés dans le fichier `.env` du projet) :

| Paramètre | Valeur |
|---|---|
| Hôte | `sql.freedb.tech` |
| Port | `3306` |
| Base | `freedb_UF135mPz` |
| Utilisateur | `u_YSZ5fn` |
| Mot de passe | dans votre `.env` (ne l'écrivez dans aucun fichier du dépôt) |

⚠ Le fichier `.env` est dans `.gitignore` : il ne partira jamais sur GitHub. Ne copiez pas le mot de passe dans le README ni dans le code.

## 1. FreeDB – créer les tables (étapes 1 à 4) ✅ compte et base déjà créés
1. Connectez-vous à https://freedb.tech → ouvrez phpMyAdmin.
2. Cliquez sur la base **freedb_UF135mPz** dans la colonne de gauche (ne faites PAS de CREATE DATABASE).
3. Onglet **SQL** → collez tout le contenu de `schema.sql` → **Exécuter**.
4. Vérifiez : les tables `CATEGORIE_PRODUIT` et `PRODUIT` apparaissent ; `PRODUIT` contient 3 lignes d'exemple (supprimez-les plus tard si vous voulez une base vide pour la démo).

## 2. Test local (étapes 5 à 8)
Dans un terminal, dans le dossier du projet :
```
pip install -r requirements.txt
python app.py
```
Ouvrez http://127.0.0.1:5000, ajoutez une catégorie et un produit, puis vérifiez-les dans phpMyAdmin.
Si la connexion échoue : vérifiez que le Wi-Fi n'ouvre pas le port 3306 en sortie bloqué (essayez un partage de connexion mobile).

## 3. GitHub (étapes 9-10) – vous avez déjà un compte
1. Sur github.com : **New repository** → nom `gestion-commerciale` → Public → ne cochez aucun fichier d'initialisation → Create.
2. Dans le dossier du projet :
```
git init
git add .
git status          # vérifiez que ".env" N'APPARAÎT PAS
git commit -m "Version 1 : catégories et produits"
git branch -M main
git remote add origin https://github.com/VOTRE_PSEUDO/gestion-commerciale.git
git push -u origin main
```
3. Sur la page GitHub du dépôt, confirmez la présence de `app.py`, `templates/`, `schema.sql`, `requirements.txt` et l'absence de `.env`.

## 4. Render (étapes 11-14)
1. https://render.com → **Sign up with GitHub**.
2. **New +** → **Web Service** → sélectionnez `gestion-commerciale`.
3. Réglages : Language **Python 3** · Build Command `pip install -r requirements.txt` · Start Command `gunicorn app:app` · Instance type **Free**.
4. **Environment Variables** (ouvrez votre `.env` pour copier les valeurs) :
   - `DB_HOST` = `sql.freedb.tech`
   - `DB_PORT` = `3306`
   - `DB_NAME` = `freedb_UF135mPz`
   - `DB_USER` = `u_YSZ5fn`
   - `DB_PASSWORD` = (valeur du `.env`)
   - `SECRET_KEY` = (valeur du `.env`)
5. **Create Web Service**, attendez « Live », copiez l'URL `https://….onrender.com`.
   Offre gratuite : mise en veille après ~15 min d'inactivité, réveil ≈ 1 min.

## 5. Test final (étape 15) et démo
1. Ouvrez l'URL publique → ajoutez une catégorie, puis un produit.
2. Vérifiez les lignes dans phpMyAdmin.
3. Sur Render : **Manual Deploy → Restart** puis rechargez : les données doivent toujours être là.
4. Filmez cette séquence (ajout catégorie + produit) : c'est la démo demandée.

## Si ça bloque
- **Erreur 503 / « Base indisponible »** sur Render : une variable d'environnement est mal recopiée, ou FreeDB refuse la connexion distante (vérifiez les limites de l'offre dans votre tableau de bord FreeDB).
- **Lenteur au premier chargement** : normal (réveil du service gratuit).

## Livrables
`MCD_schema_relationnel.png` · `schema.sql` · `app.py` + `templates/` · lien du dépôt GitHub · URL Render · vidéo de démo.
