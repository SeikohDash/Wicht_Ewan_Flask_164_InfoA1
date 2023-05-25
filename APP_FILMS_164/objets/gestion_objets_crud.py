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
from APP_FILMS_164.objets.gestion_objets_wtf_forms import FormWTFUpdateObjets, FormWTFAddObjets, FormWTFDeleteFilm

"""Ajouter un film grâce au formulaire "objets_add_wtf.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_add

Test : exemple: cliquer sur le menu "Films/Genres" puis cliquer sur le bouton "ADD" d'un "film"

Paramètres : sans


Remarque :  Dans le champ "nom_film_update_wtf" du formulaire "films/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python dans le fichier ""
            On ne doit pas accepter un champ vide.
"""


@app.route("/film_add", methods=['GET', 'POST'])
def objets_add_wtf():
    # Objet formulaire pour AJOUTER un film
    form_add_objets = FormWTFAddObjets()
    if request.method == "POST":
        try:
            if form_add_objets.validate_on_submit():
                nom_objets = form_add_objets.nom_objets_wtf.data
                cb_ean = form_add_objets.cb_ean_wtf.data
                prix = form_add_objets.prix_wtf.data


                valeurs_insertion_dictionnaire = {"value_nom_objets": nom_objets,
                                                  "value_cb_ean": cb_ean,
                                                  "value_prix": prix
                                                  }

                strsql_insert_objets = """INSERT INTO t_objets (id_objets,nom_objets,cb_ean,prix)  
                                    VALUES (NULL,%(value_nom_objets)s,%(value_cb_ean)s,%(value_prix)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_objets, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion du nouveau film (id_objets_sel=0 => afficher tous les films)
                return redirect(url_for('objets_reception_fourn_afficher', id_objets_sel=0))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{objets_add_wtf.__name__} ; "
                                            f"{Exception_genres_ajouter_wtf}")

    return render_template("objets/objets_add_wtf.html", form_add_objets=form_add_objets)


"""Editer(update) un film qui a été sélectionné dans le formulaire "objets_reception_fourn_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_update

Test : exemple: cliquer sur le menu "Films/Genres" puis cliquer sur le bouton "EDIT" d'un "film"

Paramètres : sans

But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"

Remarque :  Dans le champ "nom_film_update_wtf" du formulaire "films/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python.
            On ne doit pas accepter un champ vide.
"""


@app.route("/film_update", methods=['GET', 'POST'])
def Objets_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_film"
    id_objets_update = request.values['id_objets_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update_objets = FormWTFUpdateObjets()
    try:
        print(" on submit ", form_update_objets.validate_on_submit())
        if form_update_objets.validate_on_submit():
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            nom_objets = form_update_objets.nom_objets_update.data
            cb_ean = form_update_objets.cb_ean_update_wtf.data
            prix = form_update_objets.prix_update_wtf.data

            valeur_update_dictionnaire = {"value_id_objets": id_objets_update,
                                          "value_nom_objets_update": nom_objets,
                                          "value_cb_ean_update": cb_ean,
                                          "value_prix_update": prix
                                          }
            
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_nom_film = """UPDATE t_objets SET nom_objets = %(value_nom_objets_update)s,
                                                            cb_ean = %(value_cb_ean_update)s,
                                                            prix = %(value_prix_update)s
                                                            WHERE id_objets = %(value_id_objets)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_nom_film, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Afficher seulement le film modifié, "ASC" et l'"id_film_update"
            return redirect(url_for('objets_reception_fourn_afficher', id_objets_sel=id_objets_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_film" et "intitule_genre" de la "t_genre"
            str_sql_id_objets = "SELECT * FROM t_objets WHERE id_objets = %(value_id_objets)s"
            valeur_select_dictionnaire = {"value_id_objets": id_objets_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_objets, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_film = mybd_conn.fetchone()
            print("data_objets ", data_film, " type ", type(data_film), " genre ",
                  data_film["nom_objets"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "film_update_wtf.html"
            form_update_objets.nom_objets_update.data = data_film["nom_objets"]
            form_update_objets.cb_ean_update_wtf.data = data_film["cb_ean"]
            form_update_objets.prix_update_wtf.data = data_film["prix"]

    except Exception as Exception_film_update_wtf:
        raise ExceptionFilmUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{Objets_update_wtf.__name__} ; "
                                     f"{Exception_film_update_wtf}")

    return render_template("objets/objets_update_wtf.html", form_update_objets=form_update_objets)


"""Effacer(delete) un film qui a été sélectionné dans le formulaire "objets_reception_fourn_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_delete
    
Test : ex. cliquer sur le menu "film" puis cliquer sur le bouton "DELETE" d'un "film"
    
Paramètres : sans

Remarque :  Dans le champ "nom_film_delete_wtf" du formulaire "films/film_delete_wtf.html"
            On doit simplement cliquer sur "DELETE"
"""


@app.route("/film_delete", methods=['GET', 'POST'])
def film_delete_wtf():
    # Pour afficher ou cacher les boutons "EFFACER"
    data_film_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_film"
    id_film_delete = request.values['id_film_btn_delete_html']

    # Objet formulaire pour effacer le film sélectionné.
    form_delete_film = FormWTFDeleteFilm()
    try:
        # Si on clique sur "ANNULER", afficher tous les films.
        if form_delete_film.submit_btn_annuler.data:
            return redirect(url_for("objets_reception_fourn_afficher", id_objets_sel=0))

        if form_delete_film.submit_btn_conf_del_film.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            data_film_delete = session['data_film_delete']
            print("data_film_delete ", data_film_delete)

            flash(f"Effacer le film de façon définitive de la BD !!!", "danger")
            # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
            # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
            btn_submit_del = True

        # L'utilisateur a vraiment décidé d'effacer.
        if form_delete_film.submit_btn_del_film.data:
            valeur_delete_dictionnaire = {"value_id_objets": id_film_delete}
            print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

            str_sql_delete_fk_film_genre = """DELETE FROM t_reception_objets_four WHERE fk_film = %(value_id_objets)s"""
            str_sql_delete_film = """DELETE FROM t_film WHERE id_film = %(value_id_objets)s"""
            # Manière brutale d'effacer d'abord la "fk_film", même si elle n'existe pas dans la "t_reception_objets_four"
            # Ensuite on peut effacer le film vu qu'il n'est plus "lié" (INNODB) dans la "t_reception_objets_four"
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_delete_fk_film_genre, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_film, valeur_delete_dictionnaire)

            flash(f"Film définitivement effacé !!", "success")
            print(f"Film définitivement effacé !!")

            # afficher les données
            return redirect(url_for('objets_reception_fourn_afficher', id_objets_sel=0))
        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_objets": id_film_delete}
            print(id_film_delete, type(id_film_delete))

            # Requête qui affiche le film qui doit être efffacé.
            str_sql_genres_films_delete = """SELECT * FROM t_film WHERE id_film = %(value_id_objets)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_film_delete = mydb_conn.fetchall()
                print("data_film_delete...", data_film_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_film_delete'] = data_film_delete

            # Le bouton pour l'action "DELETE" dans le form. "film_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_film_delete_wtf:
        raise ExceptionFilmDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{film_delete_wtf.__name__} ; "
                                     f"{Exception_film_delete_wtf}")

    return render_template("films/film_delete_wtf.html",
                           form_delete_film=form_delete_film,
                           btn_submit_del=btn_submit_del,
                           data_film_del=data_film_delete
                           )
