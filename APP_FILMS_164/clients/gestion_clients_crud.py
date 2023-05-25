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
from APP_FILMS_164.clients.gestion_clients_wtf_forms import FormWTFUpdateClient, FormWTFAddClient, FormWTFDeleteClient

"""Ajouter un film grâce au formulaire "client_add_wtf.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_add

Test : exemple: cliquer sur le menu "Films/Genres" puis cliquer sur le bouton "ADD" d'un "film"

Paramètres : sans


Remarque :  Dans le champ "nom_mail_update_wtf" du formulaire "films/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python dans le fichier ""
            On ne doit pas accepter un champ vide.
"""
@app.route("/clients_afficher/<int:id_client_sel>", methods=['GET', 'POST'])
def clients_afficher(id_client_sel):
    print(" clients_afficher id_client_sel ", id_client_sel)
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_client_afficher_data = """SELECT id_client, nom, prenom, date_de_nais,nom_genre,nom_assu FROM t_client 
                                            INNER JOIN t_genre ON t_genre.id_genre = t_client.fk_genre
                                            INNER JOIN t_assurance on t_assurance.id_assu = t_client.fk_assu"""
                if id_client_sel == 0:
                    # le paramètre 0 permet d'afficher tous les clients
                    # Sinon le paramètre représente la valeur de l'id du film
                    mc_afficher.execute(strsql_client_afficher_data)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    valeur_id_film_selected_dictionnaire = {"value_id_client_selected": id_client_sel}
                    # En MySql l'instruction HAVING fonctionne comme un WHERE... mais doit être associée à un GROUP BY
                    # L'opérateur += permet de concaténer une nouvelle valeur à la valeur de gauche préalablement définie.
                    strsql_client_afficher_data += """ HAVING id_client= %(value_id_client_selected)s"""

                    mc_afficher.execute(strsql_client_afficher_data, valeur_id_film_selected_dictionnaire)

                # Récupère les données de la requête.
                data_client_afficher = mc_afficher.fetchall()
                print("data_client ", data_client_afficher, " Type : ", type(data_client_afficher))

                # Différencier les messages.
                if not data_client_afficher and id_client_sel == 0:
                    flash("""La table "t_client" est vide. !""", "warning")
                elif not data_client_afficher and id_client_sel > 0:
                    # Si l'utilisateur change l'id_mail dans l'URL et qu'il ne correspond à aucun film
                    flash(f"Le client {id_client_sel} demandé n'existe pas !!", "warning")
                else:
                    flash(f"Données client affichés !!", "success")

        except Exception as Exception_films_genres_afficher:
            raise ExceptionFilmsGenresAfficher(f"fichier : {Path(__file__).name}  ;  {clients_afficher.__name__} ;"
                                               f"{Exception_films_genres_afficher}")

    print("clients_afficher  ", data_client_afficher)
    # Envoie la page "HTML" au serveur.
    return render_template("clients/clients_afficher.html", data=data_client_afficher)


@app.route("/client_add_wtf", methods=['GET', 'POST'])
def client_add_wtf():
    # Objet formulaire pour AJOUTER un client
    form = FormWTFAddClient()
    print(" on submit FormWTFAddClient ", form.submit.data, " req ", request.method)
    try:
        if request.method == "POST" and form.submit.data:
            # Récuperer les données du formulaire défini dans APP_FILMS_164/clients/gestion_clients_wtf_forms.py
            nom_client = form.nom_client_wtf.data
            prenom_client = form.prenom_client_wtf.data
            date_nais_client = form.date_nais_client_wtf.data
            genre_selectionne = form.genres_dropdown_wtf.data
            assurance_selectionne = form.assu_dropdown_wtf.data

            valeurs_insertion_dictionnaire = {"value_nom_client": nom_client,
                                              "value_prenom_client": prenom_client,
                                              "value_date_client": date_nais_client,
                                              "value_genre_val_list_dropdown": genre_selectionne,
                                              "value_assu_val_list_dropdown": assurance_selectionne
                                              }
            print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

            strsql_insert_client = """INSERT INTO t_client (id_client,nom,prenom,date_de_nais,fk_genre,fk_assu)
                                    VALUES (NULL,%(value_nom_client)s,%(value_prenom_client)s,%(value_date_client)s,%(value_genre_val_list_dropdown)s,%(value_assu_val_list_dropdown)s) """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(strsql_insert_client, valeurs_insertion_dictionnaire)

            flash(f"Données insérées !!", "success")
            print(f"Données insérées !!")

            # Pour afficher et constater l'insertion du nouveau film (id_client_sel=0 => afficher tous les films)
            return redirect(url_for('clients_afficher', id_client_sel=0))

        if request.method == "GET":
            with DBconnection() as mc_afficher:
                strsql_genres_afficher = """SELECT id_genre, nom_genre FROM t_genre ORDER BY id_genre ASC"""
                mc_afficher.execute(strsql_genres_afficher)

            data_genres = mc_afficher.fetchall()
            print("demo_select_wtf data_genres ", data_genres, " Type : ", type(data_genres))

            """
                Préparer les valeurs pour la liste déroulante de l'objet "FormWTFAddClient"
                la liste déroulante est définie dans le "APP_FILMS_164/clients/gestion_clients_wtf_forms.py" 
                le formulaire qui utilise la liste déroulante "APP_FILMS_164/templates/clients/client_add_wtf.html"
            """
            genre_val_list_dropdown = []
            for i in data_genres:
                genre_val_list_dropdown = [(i["id_genre"], i["nom_genre"]) for i in data_genres]

            print("genre_val_list_dropdown ", genre_val_list_dropdown)
            # Les valeurs sont chargées dans la liste déroulante
            form.genres_dropdown_wtf.choices = genre_val_list_dropdown


            with DBconnection() as mc_afficher:
                strsql_assu_afficher = """SELECT id_assu, nom_assu FROM t_assurance ORDER BY id_assu ASC"""
                mc_afficher.execute(strsql_assu_afficher)

            data_assu = mc_afficher.fetchall()
            print("demo_select_wtf data_assu ", data_assu, " Type : ", type(data_assu))

            """
                Préparer les valeurs pour la liste déroulante de l'objet "FormWTFAddClient"
                la liste déroulante est définie dans le "APP_FILMS_164/clients/gestion_clients_wtf_forms.py" 
                le formulaire qui utilise la liste déroulante "APP_FILMS_164/templates/clients/client_add_wtf.html"
            """
            assu_val_list_dropdown = []
            for i in data_assu:
                assu_val_list_dropdown = [(i["id_assu"], i["nom_assu"]) for i in data_assu]

            print("assu_dropdown_wtf ", assu_val_list_dropdown)
            # Les valeurs sont chargées dans la liste déroulante
            form.assu_dropdown_wtf.choices = assu_val_list_dropdown

    except Exception as Exception_client_ajouter_wtf:
        raise ExceptionClientsAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                        f"{client_add_wtf.__name__} ; "
                                        f"{ExceptionClientsAjouterWtf}")

    return render_template("clients/client_add_wtf.html", form=form)




"""Editer(update) un film qui a été sélectionné dans le formulaire "clients_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_update

Test : exemple: cliquer sur le menu "Films/Genres" puis cliquer sur le bouton "EDIT" d'un "film"

Paramètres : sans

But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"

Remarque :  Dans le champ "nom_mail_update_wtf" du formulaire "clients/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python.
            On ne doit pas accepter un champ vide.
"""


@app.route("/client_update_wtf", methods=['GET', 'POST'])
def client_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_client"
    id_client_update = request.values['id_client_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update_client = FormWTFUpdateClient()
    try:

        if request.method == "POST" and form_update_client.submit.data:
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            nom_client_update = form_update_client.nom_client_update_wtf.data
            prenom_client_update = form_update_client.prenom_client_update_wtf.data
            date_nais_client_update = form_update_client.date_nais_client_update_wtf.data
            genre_client_update = form_update_client.genres_dropdown_update_wtf.data
            fk_assu_client_update = form_update_client.assu_dropdown_update_wtf.data

            valeur_update_dictionnaire = {"value_id_client": id_client_update,
                                          "value_nom_client": nom_client_update,
                                          "value_prenom_client": prenom_client_update,
                                          "value_date_client": date_nais_client_update,
                                          "value_genre_update_val_list_dropdown": genre_client_update,
                                          "value_assurance_client": fk_assu_client_update
                                        }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_nom_mail = """UPDATE t_client SET nom = %(value_nom_client)s,
                                                            prenom = %(value_prenom_client)s,
                                                            date_de_nais = %(value_date_client)s,
                                                            fk_genre = %(value_genre_update_val_list_dropdown)s,
                                                            fk_assu = %(value_assurance_client)s
                                                            WHERE id_client = %(value_id_client)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_nom_mail, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Afficher seulement le film modifié, "ASC" et l'"id_client_update"
            return redirect(url_for('clients_afficher', id_client_sel=id_client_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_mail" et "nom_genre" de la "t_genre"
            str_sql_id_mail = "SELECT * FROM t_client WHERE id_client = %(value_id_client)s"
            valeur_select_dictionnaire = {"value_id_client": id_client_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_mail, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_client = mybd_conn.fetchone()
            print("data_client ", data_client, " type ", type(data_client), " genre ",
                  data_client["nom"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "client_update_wtf.html"
            form_update_client.nom_client_update_wtf.data = data_client["nom"]
            form_update_client.prenom_client_update_wtf.data = data_client["prenom"]
            form_update_client.date_nais_client_update_wtf.data = data_client["date_de_nais"]
            form_update_client.genres_dropdown_update_wtf.data = data_client["fk_genre"]
            form_update_client.assu_dropdown_update_wtf.data = data_client["fk_assu"]

        if request.method == "GET":
            with DBconnection() as mc_afficher:
                strsql_genres_afficher = """SELECT id_genre, nom_genre FROM t_genre ORDER BY id_genre ASC"""
                mc_afficher.execute(strsql_genres_afficher)

            data_genres = mc_afficher.fetchall()
            print("demo_select_wtf data_genres ", data_genres, " Type : ", type(data_genres))

            """
                Préparer les valeurs pour la liste déroulante de l'objet "FormWTFAddClient"
                la liste déroulante est définie dans le "APP_FILMS_164/clients/gestion_clients_wtf_forms.py" 
                le formulaire qui utilise la liste déroulante "APP_FILMS_164/templates/clients/client_add_wtf.html"
            """
            genre_update_val_list_dropdown = []
            for i in data_genres:

                genre_update_val_list_dropdown = [(i["id_genre"], i["nom_genre"]) for i in data_genres]
            print("genre_update_val_list_dropdown ", genre_update_val_list_dropdown)
            # Les valeurs sont chargées dans la liste déroulante
            form_update_client.genres_dropdown_update_wtf.choices = genre_update_val_list_dropdown


            with DBconnection() as mc_afficher:
                strsql_assu_afficher = """SELECT id_assu, nom_assu FROM t_assurance ORDER BY id_assu ASC"""
                mc_afficher.execute(strsql_assu_afficher)

            data_assu = mc_afficher.fetchall()
            print("demo_select_wtf data_assu ", data_assu, " Type : ", type(data_assu))

            """
                Préparer les valeurs pour la liste déroulante de l'objet "FormWTFAddClient"
                la liste déroulante est définie dans le "APP_FILMS_164/clients/gestion_clients_wtf_forms.py" 
                le formulaire qui utilise la liste déroulante "APP_FILMS_164/templates/clients/client_add_wtf.html"
            """
            assu_update_val_list_dropdown = []
            for i in data_assu:
                assu_update_val_list_dropdown = [(i["id_assu"], i["nom_assu"]) for i in data_assu]

            print("assu_update_val_list_dropdown ", assu_update_val_list_dropdown)
            # Les valeurs sont chargées dans la liste déroulante
            form_update_client.assu_dropdown_update_wtf.choices = assu_update_val_list_dropdown

    except Exception as ExceptionClientsUpdateWtf:
        raise ExceptionFilmUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{client_update_wtf.__name__} ; "
                                     f"{ExceptionClientsUpdateWtf}")

    return render_template("clients/client_update_wtf.html", form_update_client=form_update_client)


"""Effacer(delete) un film qui a été sélectionné dans le formulaire "clients_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_delete
    
Test : ex. cliquer sur le menu "film" puis cliquer sur le bouton "DELETE" d'un "film"
    
Paramètres : sans

Remarque :  Dans le champ "nom_film_delete_wtf" du formulaire "clients/client_delete_wtf.html"
            On doit simplement cliquer sur "DELETE"
"""


@app.route("/client_delete", methods=['GET', 'POST'])
def client_delete_wtf():
    # Pour afficher ou cacher les boutons "EFFACER"
    data_client_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_mail"
    id_client_delete = request.values['id_genre_btn_delete_html']

    # Objet formulaire pour effacer le film sélectionné.
    form_delete_client = FormWTFDeleteClient()
    try:
        # Si on clique sur "ANNULER", afficher tous les films.
        if form_delete_client.submit_btn_annuler.data:
            return redirect(url_for("clients_afficher", id_client_sel=0))

        if form_delete_client.submit_btn_conf_del_film.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "clients/client_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
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
            # Manière brutale d'effacer d'abord la "fk_film", même si elle n'existe pas dans la "t_pers_mail"
            # Ensuite on peut effacer le film vu qu'il n'est plus "lié" (INNODB) dans la "t_pers_mail"
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
            return redirect(url_for('clients_afficher', id_client_sel=0))
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
                # le formulaire "clients/client_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_client_delete'] = data_client_delete

            # Le bouton pour l'action "DELETE" dans le form. "client_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_film_delete_wtf:
        raise ExceptionFilmDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{client_delete_wtf.__name__} ; "
                                     f"{Exception_film_delete_wtf}")

    return render_template("clients/client_delete_wtf.html",
                           form_delete_client=form_delete_client,
                           btn_submit_del=btn_submit_del,
                           data_film_del=data_client_delete
                           )
