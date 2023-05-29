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
from APP_FILMS_164.assurance.gestion_assu_wtf_forms import FormWTFAjouterAssu
from APP_FILMS_164.assurance.gestion_assu_wtf_forms import FormWTFDeleteAssu
from APP_FILMS_164.assurance.gestion_assu_wtf_forms import FormWTFUpdateAssu

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /assu_afficher
    
    Test : ex : http://127.0.0.1:5575/genres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_assu_sel = 0 >> tous les genres.
                id_assu_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/assu_afficher/<string:order_by>/<int:id_assu_sel>", methods=['GET', 'POST'])
def assu_afficher(order_by, id_assu_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_assu_sel == 0:
                    strsql_assu_afficher = """SELECT * from t_assurance"""
                    mc_afficher.execute(strsql_assu_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_assurance_selected_dictionnaire = {"value_id_assu_selected": id_assu_sel}
                    strsql_assu_afficher = """SELECT * from t_assurance"""

                    mc_afficher.execute(strsql_assu_afficher, valeur_id_assurance_selected_dictionnaire)
                else:
                    strsql_assu_afficher = """SELECT * from t_assurance"""

                    mc_afficher.execute(strsql_assu_afficher)

                data_assu = mc_afficher.fetchall()

                print("data_assu ", data_assu, " Type : ", type(data_assu))

                # Différencier les messages si la table est vide.
                if not data_assu and id_assu_sel == 0:
                    flash("""La table "t_assurance" est vide. !!""", "warning")
                elif not data_assu and id_assu_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"L'assurance demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données assurance affichés !!", "success")

        except Exception as Exception_assu_afficher:
            raise ExceptionAssuranceAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{assu_afficher.__name__} ; "
                                          f"{Exception_assu_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("assurance/assu_afficher.html", data=data_assu)


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


@app.route("/assu_ajouter", methods=['GET', 'POST'])
def assu_ajouter_wtf():
    form = FormWTFAjouterAssu()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                name_assu_wtf = form.nom_assu_wtf.data
                name_assu = name_assu_wtf.lower()
                valeurs_insertion_dictionnaire = {"value_nom_assu": name_assu}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_assurance = """INSERT INTO t_assurance (id_assu,nom_assu) VALUES (NULL,%(value_nom_assu)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_assurance, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('assu_afficher', order_by='DESC', id_assu_sel=0))

        except Exception as Exception_assu_ajouter_wtf:
            raise ExceptionAssuranceAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{assu_ajouter_wtf.__name__} ; "
                                            f"{Exception_assu_ajouter_wtf}")

    return render_template("assurance/assu_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update
    
    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
    
    Remarque :  Dans le champ "nom_assu_update_wtf" du formulaire "genres/genre_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/assu_update", methods=['GET', 'POST'])
def assu_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_assu_update = request.values['id_assu_btn_edit_htlm']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateAssu()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_assu_update = form_update.nom_assu_update_wtf.data
            name_assu_update = name_assu_update.lower()


            valeur_update_dictionnaire = {"value_id_assu": id_assu_update,
                                          "value_name_assu": name_assu_update}
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_assurance = """UPDATE t_assurance SET nom_assu = %(value_name_assu)s 
            WHERE id_assu = %(value_id_assu)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_assurance, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_assu_update"
            return redirect(url_for('assu_afficher', order_by="ASC", id_assu_sel=id_assu_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "nom_genre" de la "t_genre"
            str_sql_id_assurance = "SELECT id_assu, nom_assu FROM t_assurance " \
                               "WHERE id_assu = %(value_id_assu)s"
            valeur_select_dictionnaire = {"value_id_assu": id_assu_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_assurance, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_assu = mybd_conn.fetchone()
            print("data_nom_assu ", data_nom_assu, " type ", type(data_nom_assu), " genre ",
                  data_nom_assu["nom_assu"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "genre_update_wtf.html"
            form_update.nom_assu_update_wtf.data = data_nom_assu["nom_assu"]


    except Exception as Exception_assu_update_wtf:
        raise ExceptionAssuranceUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{assu_update_wtf.__name__} ; "
                                      f"{Exception_assu_update_wtf}")

    return render_template("assurance/assu_update_wtf.html", form_update=form_update)

"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
    
    Remarque :  Dans le champ "nom_assu_delete_wtf" du formulaire "genres/assu_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/assu_delete", methods=['GET', 'POST'])
def assu_delete_wtf():
    data_assu_attribue_client_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_assu_delete = request.values['id_assu_btn_delete_htlm']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteAssu()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("assu_afficher", order_by="ASC", id_assu_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "genres/assu_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_assu_attribue_client_delete = session['data_assu_attribue_client_delete']
                print("data_assu_attribue_client_delete ", data_assu_attribue_client_delete)

                flash(f"Effacer le genre de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_assu": id_assu_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_client_assu = """DELETE FROM t_client WHERE fk_assu = %(value_id_assu)s"""
                str_sql_delete_assurance = """DELETE FROM t_assurance WHERE id_assu = %(value_id_assu)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_pers_mail"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_pers_mail"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_client_assu, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_assurance, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('assu_afficher', order_by="ASC", id_assu_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_assu": id_assu_delete}
            print(id_assu_delete, type(id_assu_delete))

            # Requête qui affiche tous les films_genres qui ont le genre que l'utilisateur veut effacer
            str_sql_assurance_client_delete = """SELECT id_client, nom, id_assu, nom_assu FROM t_client 
                                            INNER JOIN t_assurance ON t_assurance.id_assu = t_client.fk_assu
                                            WHERE fk_assu = %(value_id_assu)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_assurance_client_delete, valeur_select_dictionnaire)
                data_assu_attribue_client_delete = mydb_conn.fetchall()
                print("data_assu_attribue_client_delete...", data_assu_attribue_client_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "genres/assu_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_assu_attribue_client_delete'] = data_assu_attribue_client_delete

                # Opération sur la BD pour récupérer "id_genre" et "nom_genre" de la "t_genre"
                str_sql_id_assu = "SELECT id_assu, nom_assu FROM t_assurance WHERE id_assu = %(value_id_assu)s"

                mydb_conn.execute(str_sql_id_assu, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_nom_assu = mydb_conn.fetchone()
                print("data_nom_assu ", data_nom_assu, " type ", type(data_nom_assu), " genre ",
                      data_nom_assu["nom_assu"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "assu_delete_wtf.html"
            form_delete.nom_assu_delete_wtf.data = data_nom_assu["nom_assu"]

            # Le bouton pour l'action "DELETE" dans le form. "assu_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_assu_delete_wtf:
        raise ExceptionAdresseDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{assu_delete_wtf.__name__} ; "
                                      f"{Exception_assu_delete_wtf}")

    return render_template("assurance/assu_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_client_associes=data_assu_attribue_client_delete)
