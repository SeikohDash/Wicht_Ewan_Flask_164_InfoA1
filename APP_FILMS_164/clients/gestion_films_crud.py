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
from APP_FILMS_164.clients.gestion_films_wtf_forms import FormWTFUpdateFilm, FormWTFAddFilm, FormWTFDeleteFilm

"""Ajouter un film grâce au formulaire "film_add_wtf.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_add

Test : exemple: cliquer sur le menu "Films/Genres" puis cliquer sur le bouton "ADD" d'un "film"

Paramètres : sans


Remarque :  Dans le champ "nom_film_update_wtf" du formulaire "films/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python dans le fichier ""
            On ne doit pas accepter un champ vide.
"""


@app.route("/Client_Add", methods=['GET', 'POST'])
def film_add_wtf():
    # Objet formulaire pour AJOUTER un film
    form = FormWTFAddFilm()
    if request.method == "POST":
        try:
            if form.validate_on_submit():

                nom_client = form.nom_client_wtf.data
                prenom_client = form.prenom_client_wtf.data
                date_nais_client = form.date_nais_client_wtf.data
                fk_genre_client = form.fk_genre_client_wtf.data
                assu_maladie_client = form.assu_maladie_client_wtf.data





                valeurs_insertion_dictionnaire = {"value_nom_client": nom_client,
                                                  "value_prenom_client": prenom_client,
                                                  "value_date_client": date_nais_client,
                                                  "value_genre_client": fk_genre_client,
                                                  "value_assurance_client": assu_maladie_client
                                                  }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_film = """INSERT INTO t_client (id_client,nom,prenom,date_de_nais,fk_genre,Assu_maladie) 
                                        VALUES (NULL,%(value_nom_client)s,%(value_prenom_client)s,%(value_date_client)s,%(value_genre_client)s,%(value_assurance_client)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_film, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion du nouveau film (id_film_sel=0 => afficher tous les films)
                return redirect(url_for('films_genres_afficher', id_film_sel=0))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{film_add_wtf.__name__} ; "
                                            f"{Exception_genres_ajouter_wtf}")

    return render_template("clients/film_add_wtf.html", form=form)


"""Editer(update) un film qui a été sélectionné dans le formulaire "films_genres_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_update

Test : exemple: cliquer sur le menu "Films/Genres" puis cliquer sur le bouton "EDIT" d'un "film"

Paramètres : sans

But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"

Remarque :  Dans le champ "nom_film_update_wtf" du formulaire "clients/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python.
            On ne doit pas accepter un champ vide.
"""


@app.route("/Client_Update", methods=['GET', 'POST'])
def film_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_client"
    id_client_update = request.values['id_client_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update_client = FormWTFUpdateFilm()
    try:
        print(" on submit ", form_update_client.validate_on_submit())
        if form_update_client.validate_on_submit():
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            nom_client_update = form_update_client.nom_client_update_wtf.data
            prenom_client_update = form_update_client.prenom_client_update_wtf.data
            date_nais_client_update = form_update_client.date_nais_client_update_wtf.data
            fk_genre_client_update = form_update_client.fk_genre_client_update_wtf.data
            assu_maladie_client_update = form_update_client.assu_maladie_client_update_wtf.data

            valeur_update_dictionnaire = {"value_id_client": id_client_update,
                                          "value_nom_client": nom_client_update,
                                          "value_prenom_client": prenom_client_update,
                                          "value_date_client": date_nais_client_update,
                                          "value_genre_client": fk_genre_client_update,
                                          "value_assurance_client": assu_maladie_client_update
                                        }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_nom_film = """UPDATE t_client SET nom = %(value_nom_client)s,
                                                            prenom = %(value_prenom_client)s,
                                                            date_de_nais = %(value_date_client)s,
                                                            fk_genre = %(value_genre_client)s,
                                                            Assu_maladie = %(value_assurance_client)s
                                                            WHERE id_client = %(value_id_client)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_nom_film, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Afficher seulement le film modifié, "ASC" et l'"id_client_update"
            return redirect(url_for('films_genres_afficher', id_film_sel=id_client_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_film" et "intitule_genre" de la "t_genre"
            str_sql_id_film = "SELECT * FROM t_client WHERE id_client = %(value_id_client)s"
            valeur_select_dictionnaire = {"value_id_client": id_client_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_film, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_client = mybd_conn.fetchone()
            print("data_client ", data_client, " type ", type(data_client), " genre ",
                  data_client["nom"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "film_update_wtf.html"
            form_update_client.nom_client_update_wtf.data = data_client["nom"]
            form_update_client.prenom_client_update_wtf.data = data_client["prenom"]
            form_update_client.date_nais_client_update_wtf.data = data_client["date_de_nais"]
            form_update_client.fk_genre_client_update_wtf.data = data_client["fk_genre"]
            form_update_client.assu_maladie_client_update_wtf.data = data_client["Assu_maladie"]

    except Exception as Exception_film_update_wtf:
        raise ExceptionFilmUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{film_update_wtf.__name__} ; "
                                     f"{Exception_film_update_wtf}")

    return render_template("clients/film_update_wtf.html", form_update_client=form_update_client)


"""Effacer(delete) un film qui a été sélectionné dans le formulaire "films_genres_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_delete
    
Test : ex. cliquer sur le menu "film" puis cliquer sur le bouton "DELETE" d'un "film"
    
Paramètres : sans

Remarque :  Dans le champ "nom_film_delete_wtf" du formulaire "clients/film_delete_wtf.html"
            On doit simplement cliquer sur "DELETE"
"""


@app.route("/film_delete", methods=['GET', 'POST'])
def film_delete_wtf():
    # Pour afficher ou cacher les boutons "EFFACER"
    data_client_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_film"
    id_client_delete = request.values['id_genre_btn_delete_html']

    # Objet formulaire pour effacer le film sélectionné.
    form_delete_client = FormWTFDeleteFilm()
    try:
        # Si on clique sur "ANNULER", afficher tous les films.
        if form_delete_client.submit_btn_annuler.data:
            return redirect(url_for("films_genres_afficher", id_film_sel=0))

        if form_delete_client.submit_btn_conf_del_film.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "clients/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            data_client_delete = session['data_client_delete']
            print("data_client_delete ", data_client_delete)

            flash(f"Effacer le client de façon définitive de la BD !!!", "danger")
            # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
            # On affiche le bouton "Effacer client" qui va irrémédiablement EFFACER le client
            btn_submit_del = True

        # L'utilisateur a vraiment décidé d'effacer.
        if form_delete_client.submit_btn_del_film.data:
            valeur_delete_dictionnaire = {"value_id_client": id_client_delete}
            print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

            str_sql_delete_fk_traitement_client = """DELETE FROM t_pers_traitement WHERE fk_client = %(value_id_client)s"""
            str_sql_delete_fk_telephone_client = """DELETE FROM t_pers_telephone WHERE fk_client = %(value_id_client)s"""
            str_sql_delete_fk_mail_client = """DELETE FROM t_pers_mail WHERE fk_client = %(value_id_client)s"""
            str_sql_delete_fk_adresse_client = """DELETE FROM t_pers_adresse WHERE fk_client = %(value_id_client)s"""
            str_sql_delete_fk_achat_client = """DELETE FROM t_pers_achat_client WHERE fk_client = %(value_id_client)s"""
            str_sql_delete_client = """DELETE FROM t_client WHERE id_client = %(value_id_client)s"""
            # Manière brutale d'effacer d'abord la "fk_film", même si elle n'existe pas dans la "t_genre_film"
            # Ensuite on peut effacer le film vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_delete_fk_traitement_client, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_fk_telephone_client, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_fk_mail_client, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_fk_achat_client, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_fk_adresse_client, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_client, valeur_delete_dictionnaire)

            flash(f"Client définitivement effacé !!", "success")
            print(f"Client définitivement effacé !!")

            # afficher les données
            return redirect(url_for('films_genres_afficher', id_film_sel=0))
        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_client": id_client_delete}
            print(id_client_delete, type(id_client_delete))

            # Requête qui affiche le film qui doit être efffacé.
            str_sql_genres_films_delete = """SELECT * FROM t_client WHERE id_client = %(value_id_client)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_client_delete = mydb_conn.fetchall()
                print("data_client_delete...", data_client_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "clients/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_client_delete'] = data_client_delete

            # Le bouton pour l'action "DELETE" dans le form. "film_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_film_delete_wtf:
        raise ExceptionFilmDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{film_delete_wtf.__name__} ; "
                                     f"{Exception_film_delete_wtf}")

    return render_template("clients/film_delete_wtf.html",
                           form_delete_client=form_delete_client,
                           btn_submit_del=btn_submit_del,
                           data_film_del=data_client_delete
                           )
