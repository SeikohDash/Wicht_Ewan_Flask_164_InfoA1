"""Gestion des "routes" FLASK et des données pour les films.
Fichier : gestion_films_crud.py
Auteur : OM 2022.04.11
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.mail.gestion_mail_wtf_forms import FormWTFUpdateMail, FormWTFAddMail, FormWTFDeleteMail

"""Ajouter un film grâce au formulaire "mail_add_wtf.html"
Auteur : OM 2022.04.11
Définition d'une "route" /mail_add

Test : exemple: cliquer sur le menu "Films/Genres" puis cliquer sur le bouton "ADD" d'un "film"

Paramètres : sans


Remarque :  Dans le champ "nom_mail_update_wtf" du formulaire "films/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python dans le fichier ""
            On ne doit pas accepter un champ vide.
"""


@app.route("/mail_add", methods=['GET', 'POST'])
def mail_add_wtf():
    # Objet formulaire pour AJOUTER un film
    form_add_mail = FormWTFAddMail()
    if request.method == "POST":
        try:
            if form_add_mail.validate_on_submit():
                nom_mail_add = form_add_mail.nom_film_add_wtf.data

                valeurs_insertion_dictionnaire = {"value_nom_mail": nom_mail_add}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_mail = """INSERT INTO t_mail (id_mail,nom_mail) VALUES (NULL,%(value_nom_mail)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_mail, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion du nouveau film (id_mail_sel=0 => afficher tous les films)
                return redirect(url_for('mail_pers_afficher', id_mail_sel=0))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{mail_add_wtf.__name__} ; "
                                            f"{Exception_genres_ajouter_wtf}")

    return render_template("mail/mail_add_wtf.html", form_add_mail=form_add_mail)


"""Editer(update) un film qui a été sélectionné dans le formulaire "mail_pers_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_update

Test : exemple: cliquer sur le menu "Films/Genres" puis cliquer sur le bouton "EDIT" d'un "film"

Paramètres : sans

But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"

Remarque :  Dans le champ "nom_mail_update_wtf" du formulaire "films/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python.
            On ne doit pas accepter un champ vide.
"""


@app.route("/mail_update", methods=['GET', 'POST'])
def mail_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_mail"
    id_mail_update = request.values['id_mail_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update_mail = FormWTFUpdateMail()
    try:
        print(" on submit ", form_update_mail.validate_on_submit())
        if form_update_mail.validate_on_submit():
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            nom_mail_update = form_update_mail.nom_mail_update_wtf.data

            

            valeur_update_dictionnaire = {"value_id_mail": id_mail_update,
                                          "value_nom_mail": nom_mail_update
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_nom_mail = """UPDATE t_mail SET nom_mail = %(value_nom_mail)s,
                                                            WHERE id_mail = %(value_id_mail)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_nom_mail, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Afficher seulement le film modifié, "ASC" et l'"id_mail_update"
            return redirect(url_for('mail_pers_afficher', id_mail_sel=id_mail_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_mail" et "nom_genre" de la "t_genre"
            str_sql_id_mail = "SELECT * FROM t_mail WHERE id_mail = %(value_id_mail)s"
            valeur_select_dictionnaire = {"value_id_mail": id_mail_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_mail, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_mail = mybd_conn.fetchone()
            print("data_mail ", data_mail, " type ", type(data_mail), " genre ",
                  data_mail["nom_mail"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "mail_update_wtf.html"
            form_update_mail.nom_mail_update_wtf.data = data_mail["nom_mail"]
            form_update_mail.cover_link_film_update_wtf.data = data_mail["cover_link_mail"]


    except Exception as Exception_film_update_wtf:
        raise ExceptionFilmUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{mail_update_wtf.__name__} ; "
                                     f"{Exception_film_update_wtf}")

    return render_template("mail/mail_update_wtf.html", form_update_mail=form_update_mail)


"""Effacer(delete) un film qui a été sélectionné dans le formulaire "mail_pers_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_delete
    
Test : ex. cliquer sur le menu "film" puis cliquer sur le bouton "DELETE" d'un "film"
    
Paramètres : sans

Remarque :  Dans le champ "nom_film_delete_wtf" du formulaire "films/mail_delete_wtf.html"
            On doit simplement cliquer sur "DELETE"
"""


@app.route("/mail_delete", methods=['GET', 'POST'])
def mail_delete_wtf():
    # Pour afficher ou cacher les boutons "EFFACER"
    data_mail_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_mail"
    id_mail_delete = request.values['id_mail_btn_delete_html']

    # Objet formulaire pour effacer le film sélectionné.
    form_delete_mail = FormWTFDeleteMail()
    try:
        # Si on clique sur "ANNULER", afficher tous les films.
        if form_delete_mail.submit_btn_annuler.data:
            return redirect(url_for("mail_pers_afficher", id_mail_sel=0))

        if form_delete_mail.submit_btn_conf_del_film.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "films/mail_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            data_mail_delete = session['data_mail_delete']
            print("data_mail_delete ", data_mail_delete)

            flash(f"Effacer le film de façon définitive de la BD !!!", "danger")
            # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
            # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
            btn_submit_del = True

        # L'utilisateur a vraiment décidé d'effacer.
        if form_delete_mail.submit_btn_del_film.data:
            valeur_delete_dictionnaire = {"value_id_mail": id_mail_delete}
            print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

            str_sql_delete_fk_film_genre = """DELETE FROM t_pers_mail WHERE fk_mail = %(value_id_mail)s"""
            str_sql_delete_film = """DELETE FROM t_mail WHERE id_mail = %(value_id_mail)s"""
            # Manière brutale d'effacer d'abord la "fk_film", même si elle n'existe pas dans la "t_pers_mail"
            # Ensuite on peut effacer le film vu qu'il n'est plus "lié" (INNODB) dans la "t_pers_mail"
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_delete_fk_film_genre, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_film, valeur_delete_dictionnaire)

            flash(f"Film définitivement effacé !!", "success")
            print(f"Film définitivement effacé !!")

            # afficher les données
            return redirect(url_for('mail_pers_afficher', id_mail_sel=0))
        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_mail": id_mail_delete}
            print(id_mail_delete, type(id_mail_delete))

            # Requête qui affiche le film qui doit être efffacé.
            str_sql_genres_films_delete = """SELECT * FROM t_mail WHERE id_mail = %(value_id_mail)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_mail_delete = mydb_conn.fetchall()
                print("data_mail_delete...", data_mail_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "films/mail_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_mail_delete'] = data_mail_delete

            # Le bouton pour l'action "DELETE" dans le form. "mail_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_film_delete_wtf:
        raise ExceptionFilmDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{mail_delete_wtf.__name__} ; "
                                     f"{Exception_film_delete_wtf}")

    return render_template("films/mail_delete_wtf.html",
                           form_delete_mail=form_delete_mail,
                           btn_submit_del=btn_submit_del,
                           data_film_del=data_mail_delete
                           )
