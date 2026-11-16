-- ============================================================
-- TP Gestion commerciale (secteur informel) - ISE 2 ENSAE
-- Script de création des tables (version 1 : 2 tables)
-- Sur FreeDB, la base existe déjà : ne PAS exécuter CREATE DATABASE,
-- sélectionnez simplement votre base puis lancez les CREATE TABLE.
-- ============================================================

CREATE TABLE IF NOT EXISTS CATEGORIE_PRODUIT (
    id_categorie INT          NOT NULL AUTO_INCREMENT,
    libelle      VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_categorie),
    UNIQUE KEY uq_categorie_libelle (libelle)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS PRODUIT (
    id_produit   INT           NOT NULL AUTO_INCREMENT,
    designation  VARCHAR(150)  NOT NULL,
    prix_vente   DECIMAL(12,2) NOT NULL CHECK (prix_vente >= 0),
    id_categorie INT           NOT NULL,
    PRIMARY KEY (id_produit),
    CONSTRAINT fk_produit_categorie
        FOREIGN KEY (id_categorie)
        REFERENCES CATEGORIE_PRODUIT (id_categorie)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Données d'exemple (facultatif)
INSERT INTO CATEGORIE_PRODUIT (libelle) VALUES ('Boissons'), ('Céréales'), ('Produits d''hygiène');
INSERT INTO PRODUIT (designation, prix_vente, id_categorie) VALUES
    ('Sachet de lait en poudre', 250, 1),
    ('Riz brisé 1 kg', 500, 2),
    ('Savon de ménage', 300, 3);
