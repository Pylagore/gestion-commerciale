"""Application de gestion commerciale - catégories et produits (Flask + MySQL)."""
import os

import pymysql
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from pymysql.cursors import DictCursor

load_dotenv()  # lit le fichier .env en local (ignoré sur Render)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")


def get_db():
    """Ouvre une connexion MySQL à partir des variables d'environnement."""
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=True,
        connect_timeout=10,
    )


def query(sql, params=(), one=False, write=False):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            if write:
                return cur.rowcount
            return cur.fetchone() if one else cur.fetchall()
    finally:
        conn.close()


@app.route("/")
def index():
    return redirect(url_for("produits"))


# ---------------------------- CATEGORIES ----------------------------
@app.route("/categories")
def categories():
    rows = query(
        """SELECT c.id_categorie, c.libelle, COUNT(p.id_produit) AS nb_produits
           FROM CATEGORIE_PRODUIT c
           LEFT JOIN PRODUIT p ON p.id_categorie = c.id_categorie
           GROUP BY c.id_categorie, c.libelle
           ORDER BY c.libelle"""
    )
    return render_template("categories.html", categories=rows)


@app.route("/categories/ajouter", methods=["GET", "POST"])
def categorie_ajouter():
    if request.method == "POST":
        libelle = request.form.get("libelle", "").strip()
        if not libelle:
            flash("Le libellé est obligatoire.", "danger")
        else:
            try:
                query("INSERT INTO CATEGORIE_PRODUIT (libelle) VALUES (%s)", (libelle,), write=True)
                flash("Catégorie ajoutée.", "success")
                return redirect(url_for("categories"))
            except pymysql.err.IntegrityError:
                flash("Cette catégorie existe déjà.", "danger")
    return render_template("categorie_form.html", categorie=None)


@app.route("/categories/<int:id_categorie>/modifier", methods=["GET", "POST"])
def categorie_modifier(id_categorie):
    cat = query("SELECT * FROM CATEGORIE_PRODUIT WHERE id_categorie=%s", (id_categorie,), one=True)
    if not cat:
        flash("Catégorie introuvable.", "danger")
        return redirect(url_for("categories"))
    if request.method == "POST":
        libelle = request.form.get("libelle", "").strip()
        if not libelle:
            flash("Le libellé est obligatoire.", "danger")
        else:
            try:
                query("UPDATE CATEGORIE_PRODUIT SET libelle=%s WHERE id_categorie=%s",
                      (libelle, id_categorie), write=True)
                flash("Catégorie modifiée.", "success")
                return redirect(url_for("categories"))
            except pymysql.err.IntegrityError:
                flash("Ce libellé existe déjà.", "danger")
    return render_template("categorie_form.html", categorie=cat)


@app.route("/categories/<int:id_categorie>/supprimer", methods=["POST"])
def categorie_supprimer(id_categorie):
    try:
        query("DELETE FROM CATEGORIE_PRODUIT WHERE id_categorie=%s", (id_categorie,), write=True)
        flash("Catégorie supprimée.", "success")
    except pymysql.err.IntegrityError:
        flash("Suppression impossible : des produits appartiennent à cette catégorie.", "danger")
    return redirect(url_for("categories"))


# ----------------------------- PRODUITS -----------------------------
@app.route("/produits")
def produits():
    rows = query(
        """SELECT p.id_produit, p.designation, p.prix_vente, c.libelle AS categorie
           FROM PRODUIT p
           JOIN CATEGORIE_PRODUIT c ON c.id_categorie = p.id_categorie
           ORDER BY p.designation"""
    )
    return render_template("produits.html", produits=rows)


def _lire_produit_form():
    designation = request.form.get("designation", "").strip()
    id_categorie = request.form.get("id_categorie", "")
    try:
        prix = float(request.form.get("prix_vente", "").replace(",", "."))
    except ValueError:
        prix = None
    if not designation or prix is None or prix < 0 or not id_categorie.isdigit():
        return None
    return designation, prix, int(id_categorie)


@app.route("/produits/ajouter", methods=["GET", "POST"])
def produit_ajouter():
    cats = query("SELECT * FROM CATEGORIE_PRODUIT ORDER BY libelle")
    if request.method == "POST":
        data = _lire_produit_form()
        if not data:
            flash("Désignation, prix (≥ 0) et catégorie sont obligatoires.", "danger")
        else:
            query("INSERT INTO PRODUIT (designation, prix_vente, id_categorie) VALUES (%s,%s,%s)",
                  data, write=True)
            flash("Produit ajouté.", "success")
            return redirect(url_for("produits"))
    return render_template("produit_form.html", produit=None, categories=cats)


@app.route("/produits/<int:id_produit>/modifier", methods=["GET", "POST"])
def produit_modifier(id_produit):
    prod = query("SELECT * FROM PRODUIT WHERE id_produit=%s", (id_produit,), one=True)
    if not prod:
        flash("Produit introuvable.", "danger")
        return redirect(url_for("produits"))
    cats = query("SELECT * FROM CATEGORIE_PRODUIT ORDER BY libelle")
    if request.method == "POST":
        data = _lire_produit_form()
        if not data:
            flash("Désignation, prix (≥ 0) et catégorie sont obligatoires.", "danger")
        else:
            query("""UPDATE PRODUIT SET designation=%s, prix_vente=%s, id_categorie=%s
                     WHERE id_produit=%s""", data + (id_produit,), write=True)
            flash("Produit modifié.", "success")
            return redirect(url_for("produits"))
    return render_template("produit_form.html", produit=prod, categories=cats)


@app.route("/produits/<int:id_produit>/supprimer", methods=["POST"])
def produit_supprimer(id_produit):
    query("DELETE FROM PRODUIT WHERE id_produit=%s", (id_produit,), write=True)
    flash("Produit supprimé.", "success")
    return redirect(url_for("produits"))


@app.errorhandler(pymysql.err.OperationalError)
def db_indisponible(_err):
    return render_template("base.html", erreur_db=True), 503


if __name__ == "__main__":
    app.run(debug=True)
