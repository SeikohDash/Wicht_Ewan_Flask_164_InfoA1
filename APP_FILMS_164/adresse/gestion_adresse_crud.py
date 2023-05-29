"""Gestion des "routes" FLASK et des données pour les genres.
Fichier : gestion_genres_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.adresse.gestion_adresse_wtf_forms import FormWTFAjouterAdresse
from APP_FILMS_164.adresse.gestion_adresse_wtf_forms import FormWTFDeleteAdresse
from APP_FILMS_164.adresse.gestion_adresse_wtf_forms import FormWTFUpdateAdresse

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /adresse_afficher
    
    Test : ex : http://127.0.0.1:5575/adresse_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_adresse_sel = 0 >> tous les genres.
                id_adresse_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/adresse_afficher/<string:order_by>/<int:id_adresse_sel>", methods=['GET', 'POST'])
def adresse_afficher(order_by, id_adresse_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_adresse_sel == 0:
                    strsql_adresse_afficher = """SELECT * from t_adresse"""
                    mc_afficher.execute(strsql_adresse_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_adresse_selected_dictionnaire = {"value_id_adresse_selected": id_adresse_sel}
                    strsql_adresse_afficher = """SELECT * from t_adresse"""

                    mc_afficher.execute(strsql_adresse_afficher, valeur_id_adresse_selected_dictionnaire)
                else:
                    strsql_adresse_afficher = """SELECT * from t_adresse"""

                    mc_afficher.execute(strsql_adresse_afficher)

                data_adresse = mc_afficher.fetchall()

                print("data_adresse ", data_adresse, " Type : ", type(data_adresse))

                # Différencier les messages si la table est vide.
                if not data_adresse and id_adresse_sel == 0:
                    flash("""La table "t_adresse" est vide. !!""", "warning")
                elif not data_adresse and id_adresse_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"L'adresse demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Adresse affichés !!", "success")

        except Exception as Exception_adresse_afficher:
            raise ExceptionadresseAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{adresse_afficher.__name__} ; "
                                          f"{Exception_adresse_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("adresse/adresse_afficher.html", data=data_adresse)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter
    
    Test : ex : http://127.0.0.1:5575/genres_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un film
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "genres/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/adresse_ajouter", methods=['GET', 'POST'])
def adresse_ajouter_wtf():
    form = FormWTFAjouterAdresse()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_rue = form.nom_rue_wtf.data
                NPA = form.NPA_adresse_wtf.data
                localite = form.localite_adresse_wtf.data

                valeurs_insertion_dictionnaire = {"value_nom_rue": nom_rue,
                                                  "value_NPA": NPA,
                                                  "value_localite": localite

                                                  }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_adresse = """INSERT INTO t_adresse (id_adresse,nom_rue,NPA,Localite)
                                        VALUES (NULL,%(value_nom_rue)s,%(value_NPA)s,%(value_localite)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_adresse, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('adresse_afficher', order_by='DESC', id_adresse_sel=0))

        except Exception as Exception_adresse_ajouter_wtf:
            raise ExceptionadresseAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{adresse_ajouter_wtf.__name__} ; "
                                            f"{Exception_adresse_ajouter_wtf}")

    return render_template("adresse/adresse_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update
    
    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "adresse_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "genres/adresse_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/adresse_update", methods=['GET', 'POST'])
def adresse_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_adresse_update = request.values['id_adresse_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateAdresse()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "adresse_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.

            nom_rue_update = form_update.nom_rue_update_wtf.data
            NPA_adresse_update = form_update.NPA_adresse_update_wtf.data
            localite_adresse_update = form_update.localite_adresse_update_wtf.data


            valeur_update_dictionnaire = {"value_id_adresse": id_adresse_update,
                                          "value_nom_rue": nom_rue_update,
                                          "value_npa_adresse": NPA_adresse_update,
                                          "value_localite_adresse": localite_adresse_update

                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_adresse = """UPDATE t_adresse SET nom_rue = %(value_nom_rue)s,
                                                                        NPA = %(value_npa_adresse)s,
                                                                        Localite = %(value_localite_adresse)s,
                                                                        WHERE id_adresse = %(value_id_adresse)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_adresse, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('adresse_afficher', order_by="ASC", id_adresse_sel=id_adresse_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "nom_genre" de la "t_genre"
            str_sql_id_genre = "SELECT id_adresse, nom_rue, NPA, Localite FROM t_adresse " \
                                   "WHERE id_adresse = %(value_id_adresse)s"
            valeur_select_dictionnaire = {"value_id_adresse": id_adresse_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_adresse = mybd_conn.fetchone()
            print("data_nom_rue ", data_nom_adresse, " type ", type(data_nom_adresse), " adresse ",
                  data_nom_adresse["nom_rue"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "adresse_update_wtf.html"
            form_update.nom_rue_update_wtf.data = data_nom_adresse["nom_rue"]
            form_update.NPA_adresse_update_wtf.data = data_nom_adresse["NPA"]
            form_update.localite_adresse_update_wtf.data = data_nom_adresse["Localite"]

    except Exception as Exception_adresse_update_wtf:
        raise ExceptionAdresseUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{adresse_update_wtf.__name__} ; "
                                      f"{Exception_adresse_update_wtf}")

    return render_template("adresse/adresse_update_wtf.html", form_update=form_update)

"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "adresse_afficher.html"
    
    Remarque :  Dans le champ "nom_adresse_delete_wtf" du formulaire "genres/adresse_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/adresse_delete", methods=['GET', 'POST'])
def adresse_delete_wtf():
    data_adresse_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_adresse_delete = request.values['id_adresse_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteAdresse()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("adresse_afficher", order_by="ASC", id_adresse_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "genres/adresse_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_adresse_delete = session['data_adresse_delete']
                print("data_adresse_delete ", data_adresse_delete)

                flash(f"Effacer l'adresse de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_adresse": id_adresse_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_adresse_client = """DELETE FROM t_pers_adresse WHERE fk_adresse = %(value_id_adresse)s"""
                str_sql_delete_adresse = """DELETE FROM t_adresse WHERE id_adresse = %(value_id_adresse)s"""

                # Manière brutale d'effacer d'abord la "fk_adresse", même si elle n'existe pas dans la "t_pers_adresse"
                # Ensuite on peut effacer l'adresse vu qu'il n'est plus "lié" (INNODB) dans la "t_pers_adresse"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_adresse, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_adresse_client, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('adresse_afficher', order_by="ASC", id_adresse_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_adresse": id_adresse_delete}
            print(id_adresse_delete, type(id_adresse_delete))

            # Requête qui affiche tous les client qui ont l'adresse que l'utilisateur veut effacer
            str_sql_adresse_client_delete = """SELECT nom_rue, t_client.nom
                                                FROM t_client
                                                JOIN t_pers_adresse ON id_client = fk_client 
                                                JOIN t_adresse ON id_adresse = fk_adresse
                                            WHERE fk_adresse = %(value_id_adresse)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_adresse_client_delete, valeur_select_dictionnaire)
                data_adresse_delete = mydb_conn.fetchall()
                print("data_adresse_delete...", data_adresse_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "genres/adresse_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_adresse_delete'] = data_adresse_delete

                # Opération sur la BD pour récupérer "id_genre" et "nom_genre" de la "t_genre"
                str_sql_id_adresse = "SELECT id_adresse, nom_rue, NPA, Localite FROM t_adresse WHERE id_adresse = %(value_id_adresse)s"

                mydb_conn.execute(str_sql_id_adresse, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_nom_adresse = mydb_conn.fetchone()
                print("data_nom_rue ", data_nom_adresse, " type ", type(data_nom_adresse), " rue ",
                      data_nom_adresse["nom_rue"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "adresse_delete_wtf.html"
            form_delete.nom_adresse_delete_wtf.data = data_nom_adresse["nom_rue"]

            # Le bouton pour l'action "DELETE" dans le form. "adresse_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_genre_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{adresse_delete_wtf.__name__} ; "
                                      f"{Exception_genre_delete_wtf}")

    return render_template("adresse/adresse_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_client_associes=data_adresse_delete)
