"""Gestion des "routes" FLASK et des données pour les genres.
Fichier : gestion_genres_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_PHARMACIE_164 import app
from APP_PHARMACIE_164.database.database_tools import DBconnection
from APP_PHARMACIE_164.erreurs.exceptions import *
from APP_PHARMACIE_164.mail.gestion_mail_wtf_forms import FormWTFAjouterMail
from APP_PHARMACIE_164.mail.gestion_mail_wtf_forms import FormWTFDeleteMail
from APP_PHARMACIE_164.mail.gestion_mail_wtf_forms import FormWTFUpdateMail

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /mail_afficher
    
    Test : ex : http://127.0.0.1:5575/mail_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_mail_sel = 0 >> tous les genres.
                id_mail_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/mail_afficher/<string:order_by>/<int:id_mail_sel>", methods=['GET', 'POST'])
def mail_afficher(order_by, id_mail_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_mail_sel == 0:
                    strsql_mail_afficher = """SELECT * from t_mail"""
                    mc_afficher.execute(strsql_mail_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_mail_selected_dictionnaire = {"value_id_mail_selected": id_mail_sel}
                    strsql_mail_afficher = """SELECT * from t_mail"""

                    mc_afficher.execute(strsql_mail_afficher, valeur_id_mail_selected_dictionnaire)
                else:
                    strsql_mail_afficher = """SELECT * from t_mail"""

                    mc_afficher.execute(strsql_mail_afficher)

                data_mail = mc_afficher.fetchall()

                print("data_mail ", data_mail, " Type : ", type(data_mail))

                # Différencier les messages si la table est vide.
                if not data_mail and id_mail_sel == 0:
                    flash("""La table "t_mail" est vide. !!""", "warning")
                elif not data_mail and id_mail_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"Le mail demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_mail" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données mail affichés !!", "success")

        except Exception as Exception_mail_afficher:
            raise ExceptionMailAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{mail_afficher.__name__} ; "
                                          f"{Exception_mail_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("mail/mail_afficher.html", data=data_mail)


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


@app.route("/mail_ajouter", methods=['GET', 'POST'])
def mail_ajouter_wtf():
    form = FormWTFAjouterMail()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_mail_wtf = form.nom_mail_wtf.data
                nom_mail = nom_mail_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_nom_mail": nom_mail}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_mail = """INSERT INTO t_mail (id_mail,nom_mail) VALUES (NULL,%(value_nom_mail)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_mail, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('mail_afficher', order_by='DESC', id_mail_sel=0))

        except Exception as Exception_mail_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{mail_ajouter_wtf.__name__} ; "
                                            f"{Exception_mail_ajouter_wtf}")

    return render_template("mail/mail_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /mail_update
    
    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "mail_afficher.html"
    
    Remarque :  Dans le champ "nom_mail_update_wtf" du formulaire "genres/mail_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/mail_update", methods=['GET', 'POST'])
def mail_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_mail_update = request.values['id_mail_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateMail()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "mail_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            nom_mail_update = form_update.nom_mail_update_wtf.data
            nom_mail_update = nom_mail_update.lower()


            valeur_update_dictionnaire = {"value_id_mail": id_mail_update,
                                          "value_nom_mail": nom_mail_update}
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_mail = """UPDATE t_mail SET nom_mail = %(value_nom_mail)s 
            WHERE id_mail = %(value_id_mail)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_mail, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_mail_update"
            return redirect(url_for('mail_afficher', order_by="ASC", id_mail_sel=id_mail_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "nom_genre" de la "t_genre"
            str_sql_id_mail = "SELECT id_mail, nom_mail FROM t_mail " \
                               "WHERE id_mail = %(value_id_mail)s"
            valeur_select_dictionnaire = {"value_id_mail": id_mail_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_mail, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_mail = mybd_conn.fetchone()
            print("data_nom_mail ", data_nom_mail, " type ", type(data_nom_mail), " genre ",
                  data_nom_mail["nom_mail"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "mail_update_wtf.html"
            form_update.nom_mail_update_wtf.data = data_nom_mail["nom_mail"]


    except Exception as Exception_mail_update_wtf:
        raise ExceptionMailUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{mail_update_wtf.__name__} ; "
                                      f"{Exception_mail_update_wtf}")

    return render_template("mail/mail_update_wtf.html", form_update=form_update)

"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /mail_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "mail_afficher.html"
    
    Remarque :  Dans le champ "nom_mail_delete_wtf" du formulaire "genres/mail_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/mail_delete", methods=['GET', 'POST'])
def mail_delete_wtf():
    data_client_attribue_mail_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_mail_delete = request.values['id_mail_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteMail()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("mail_afficher", order_by="ASC", id_mail_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "mail/mail_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_client_attribue_mail_delete = session['data_client_attribue_mail_delete']
                print("data_client_attribue_mail_delete ", data_client_attribue_mail_delete)

                flash(f"Effacer le genre de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_mail": id_mail_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_client_mail = """DELETE FROM t_pers_mail WHERE fk_mail = %(value_id_mail)s"""
                str_sql_delete_mail = """DELETE FROM t_mail WHERE id_mail = %(value_id_mail)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_pers_mail"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_pers_mail"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_client_mail, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_mail, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('mail_afficher', order_by="ASC", id_mail_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_mail": id_mail_delete}
            print(id_mail_delete, type(id_mail_delete))

            # Requête qui affiche tous les films_genres qui ont le genre que l'utilisateur veut effacer
            str_sql_mail_client_delete = """SELECT nom_mail, t_client.nom
                                                FROM t_client
                                                JOIN t_pers_mail ON id_client = fk_client 
                                                JOIN t_mail ON id_mail = fk_mail
                                            WHERE fk_mail = %(value_id_mail)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_mail_client_delete, valeur_select_dictionnaire)
                data_client_attribue_mail_delete = mydb_conn.fetchall()
                print("data_client_attribue_mail_delete...", data_client_attribue_mail_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "genres/mail_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_client_attribue_mail_delete'] = data_client_attribue_mail_delete

                # Opération sur la BD pour récupérer "id_genre" et "nom_genre" de la "t_genre"
                str_sql_id_mail = "SELECT id_mail, nom_mail FROM t_mail WHERE id_mail = %(value_id_mail)s"

                mydb_conn.execute(str_sql_id_mail, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_nom_mail = mydb_conn.fetchone()
                print("data_nom_mail ", data_nom_mail, " type ", type(data_nom_mail), " genre ",
                      data_nom_mail["nom_mail"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "mail_delete_wtf.html"
            form_delete.nom_mail_delete_wtf.data = data_nom_mail["nom_mail"]

            # Le bouton pour l'action "DELETE" dans le form. "mail_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_mail_delete_wtf:
        raise ExceptionMailDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{mail_delete_wtf.__name__} ; "
                                      f"{Exception_mail_delete_wtf}")

    return render_template("mail/mail_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_mailclient_associes=data_client_attribue_mail_delete)
