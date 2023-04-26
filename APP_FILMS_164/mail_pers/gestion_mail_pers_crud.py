"""
    Fichier : gestion_films_genres_crud.py
    Auteur : OM 2021.05.01
    Gestions des "routes" FLASK et des données pour l'association entre les films et les genres.
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *

"""
    Nom : mail_pers_afficher
    Auteur : OM 2021.05.01
    Définition d'une "route" /mail_pers_afficher
    
    But : Afficher les films avec les genres associés pour chaque film.
    
    Paramètres : id_genre_sel = 0 >> tous les films.
                 id_genre_sel = "n" affiche le film dont l'id est "n"
                 
"""


@app.route("/mail_pers_afficher/<int:id_mail_sel>", methods=['GET', 'POST'])
def mail_pers_afficher(id_mail_sel):
    print(" mail_pers_afficher id_mail_sel ", id_mail_sel)
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_mail_pers_afficher_data = """SELECT id_mail, nom_mail,
                                                            GROUP_CONCAT(nom) as clientmail FROM t_pers_mail
                                                            RIGHT JOIN t_mail ON t_mail.id_mail = t_pers_mail.fk_mail
                                                            LEFT JOIN t_client ON t_client.id_client = t_pers_mail.fk_client
                                                            GROUP BY id_mail"""
                if id_mail_sel == 0:
                    # le paramètre 0 permet d'afficher tous les films
                    # Sinon le paramètre représente la valeur de l'id du film
                    mc_afficher.execute(strsql_mail_pers_afficher_data)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    valeur_id_film_selected_dictionnaire = {"value_id_mail_selected": id_mail_sel}
                    # En MySql l'instruction HAVING fonctionne comme un WHERE... mais doit être associée à un GROUP BY
                    # L'opérateur += permet de concaténer une nouvelle valeur à la valeur de gauche préalablement définie.
                    strsql_mail_pers_afficher_data += """ HAVING id_mail= %(value_id_mail_selected)s"""

                    mc_afficher.execute(strsql_mail_pers_afficher_data, valeur_id_film_selected_dictionnaire)

                # Récupère les données de la requête.
                data_mail_pers_afficher = mc_afficher.fetchall()
                print("data_genres ", data_mail_pers_afficher, " Type : ", type(data_mail_pers_afficher))

                # Différencier les messages.
                if not data_mail_pers_afficher and id_mail_sel == 0:
                    flash("""La table "t_mail" est vide. !""", "warning")
                elif not data_mail_pers_afficher and id_mail_sel > 0:
                    # Si l'utilisateur change l'id_mail dans l'URL et qu'il ne correspond à aucun film
                    flash(f"Le mail{id_mail_sel} demandé n'existe pas !!", "warning")
                else:
                    flash(f"Données mail et client affichés !!", "success")

        except Exception as Exception_films_genres_afficher:
            raise ExceptionFilmsGenresAfficher(f"fichier : {Path(__file__).name}  ;  {mail_pers_afficher.__name__} ;"
                                               f"{Exception_films_genres_afficher}")

    print("mail_pers_afficher  ", data_mail_pers_afficher)
    # Envoie la page "HTML" au serveur.
    return render_template("mail_pers/mail_pers_afficher.html", data=data_mail_pers_afficher)


"""
    nom: edit_pers_mail_selected
    On obtient un objet "objet_dumpbd"

    Récupère la liste de tous les genres du film sélectionné par le bouton "MODIFIER" de "mail_pers_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les genres contenus dans la "t_genre".
    2) Les genres attribués au film selectionné.
    3) Les genres non-attribués au film sélectionné.

    On signale les erreurs importantes

"""


@app.route("/edit_pers_mail_selected", methods=['GET', 'POST'])
def edit_pers_mail_selected():
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_client_afficher = """SELECT id_mail, nom_mail FROM t_mail ORDER BY id_mail ASC"""
                mc_afficher.execute(strsql_client_afficher)
            data_genres_all = mc_afficher.fetchall()
            print("dans edit_pers_mail_selected ---> data_genres_all", data_genres_all)

            # Récupère la valeur de "id_mail" du formulaire html "mail_pers_afficher.html"
            # l'utilisateur clique sur le bouton "Modifier" et on récupère la valeur de "id_mail"
            # grâce à la variable "id_pers_mail_edit_html" dans le fichier "mail_pers_afficher.html"
            # href="{{ url_for('edit_pers_mail_selected', id_pers_mail_edit_html=row.id_mail) }}"
            id_pers_mail_edit = request.values['id_pers_mail_edit_html']

            # Mémorise l'id du film dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_id_pers_mail_edit'] = id_pers_mail_edit

            # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
            valeur_id_film_selected_dictionnaire = {"value_id_mail_selected": id_pers_mail_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la fonction genres_films_afficher_data
            # 1) Sélection du film choisi
            # 2) Sélection des genres "déjà" attribués pour le film.
            # 3) Sélection des genres "pas encore" attribués pour le film choisi.
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "genres_films_afficher_data"
            data_pers_mail_selected, data_genres_films_non_attribues, data_genres_films_attribues = \
                genres_films_afficher_data(valeur_id_film_selected_dictionnaire)

            print(data_pers_mail_selected)
            lst_data_film_selected = [item['id_client'] for item in data_pers_mail_selected]
            print("lst_data_film_selected  ", lst_data_film_selected,
                  type(lst_data_film_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les genres qui ne sont pas encore sélectionnés.
            lst_data_genres_films_non_attribues = [item['id_client'] for item in data_genres_films_non_attribues]
            session['session_lst_data_genres_films_non_attribues'] = lst_data_genres_films_non_attribues
            print("lst_data_genres_films_non_attribues  ", lst_data_genres_films_non_attribues,
                  type(lst_data_genres_films_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les genres qui sont déjà sélectionnés.
            lst_data_genres_films_old_attribues = [item['id_client'] for item in data_genres_films_attribues]
            session['session_lst_data_genres_films_old_attribues'] = lst_data_genres_films_old_attribues
            print("lst_data_genres_films_old_attribues  ", lst_data_genres_films_old_attribues,
                  type(lst_data_genres_films_old_attribues))

            print(" data data_pers_mail_selected", data_pers_mail_selected, "type ", type(data_pers_mail_selected))
            print(" data data_genres_films_non_attribues ", data_genres_films_non_attribues, "type ",
                  type(data_genres_films_non_attribues))
            print(" data_genres_films_attribues ", data_genres_films_attribues, "type ",
                  type(data_genres_films_attribues))

            # Extrait les valeurs contenues dans la table "t_genres", colonne "nom_genre"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'id_genre
            lst_data_genres_films_non_attribues = [item['nom'] for item in data_genres_films_non_attribues]
            print("lst_all_genres gf_edit_genre_film_selected ", lst_data_genres_films_non_attribues,
                  type(lst_data_genres_films_non_attribues))

        except Exception as Exception_edit_genre_film_selected:
            raise ExceptionEditGenreFilmSelected(f"fichier : {Path(__file__).name}  ;  "
                                                 f"{edit_pers_mail_selected.__name__} ; "
                                                 f"{Exception_edit_genre_film_selected}")

    return render_template("mail_pers/films_genres_modifier_tags_dropbox.html",
                           data_genres=data_genres_all,
                           data_film_selected=data_pers_mail_selected,
                           data_genres_attribues=data_genres_films_attribues,
                           data_genres_non_attribues=data_genres_films_non_attribues)


"""
    nom: update_mail_pers_selected

    Récupère la liste de tous les genres du film sélectionné par le bouton "MODIFIER" de "mail_pers_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les genres contenus dans la "t_genre".
    2) Les genres attribués au film selectionné.
    3) Les genres non-attribués au film sélectionné.

    On signale les erreurs importantes
"""


@app.route("/update_mail_pers_selected", methods=['GET', 'POST'])
def update_mail_pers_selected():
    if request.method == "POST":
        try:
            # Récupère l'id du film sélectionné
            id_film_selected = session['session_id_pers_mail_edit']
            print("session['session_id_pers_mail_edit'] ", session['session_id_pers_mail_edit'])

            # Récupère la liste des genres qui ne sont pas associés au film sélectionné.
            old_lst_data_genres_films_non_attribues = session['session_lst_data_genres_films_non_attribues']
            print("old_lst_data_genres_films_non_attribues ", old_lst_data_genres_films_non_attribues)

            # Récupère la liste des genres qui sont associés au film sélectionné.
            old_lst_data_genres_films_attribues = session['session_lst_data_genres_films_old_attribues']
            print("old_lst_data_genres_films_old_attribues ", old_lst_data_genres_films_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme genres dans le composant "tags-selector-tagselect"
            # dans le fichier "genres_films_modifier_tags_dropbox.html"
            new_lst_str_genres_films = request.form.getlist('name_select_tags')
            print("new_lst_str_genres_films ", new_lst_str_genres_films)

            # OM 2021.05.02 Exemple : Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_genre_film_old = list(map(int, new_lst_str_genres_films))
            print("new_lst_genre_film ", new_lst_int_genre_film_old, "type new_lst_genre_film ",
                  type(new_lst_int_genre_film_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # OM 2021.05.02 Une liste de "id_genre" qui doivent être effacés de la table intermédiaire "t_pers_mail".
            lst_diff_genres_delete_b = list(set(old_lst_data_genres_films_attribues) -
                                            set(new_lst_int_genre_film_old))
            print("lst_diff_genres_delete_b ", lst_diff_genres_delete_b)

            # Une liste de "id_genre" qui doivent être ajoutés à la "t_pers_mail"
            lst_diff_genres_insert_a = list(
                set(new_lst_int_genre_film_old) - set(old_lst_data_genres_films_attribues))
            print("lst_diff_genres_insert_a ", lst_diff_genres_insert_a)

            # SQL pour insérer une nouvelle association entre
            # "fk_film"/"id_mail" et "fk_genre"/"id_genre" dans la "t_pers_mail"
            strsql_insert_genre_film = """INSERT INTO t_pers_mail (id_genre_film, fk_genre, fk_film)
                                                    VALUES (NULL, %(value_fk_genre)s, %(value_fk_film)s)"""

            # SQL pour effacer une (des) association(s) existantes entre "id_mail" et "id_genre" dans la "t_pers_mail"
            strsql_delete_genre_film = """DELETE FROM t_pers_mail WHERE fk_genre = %(value_fk_genre)s AND fk_film = %(value_fk_film)s"""

            with DBconnection() as mconn_bd:
                # Pour le film sélectionné, parcourir la liste des genres à INSÉRER dans la "t_pers_mail".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_genre_ins in lst_diff_genres_insert_a:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    # et "id_genre_ins" (l'id du genre dans la liste) associé à une variable.
                    valeurs_film_sel_genre_sel_dictionnaire = {"value_fk_film": id_film_selected,
                                                               "value_fk_genre": id_genre_ins}

                    mconn_bd.execute(strsql_insert_genre_film, valeurs_film_sel_genre_sel_dictionnaire)

                # Pour le film sélectionné, parcourir la liste des genres à EFFACER dans la "t_pers_mail".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_genre_del in lst_diff_genres_delete_b:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    # et "id_genre_del" (l'id du genre dans la liste) associé à une variable.
                    valeurs_film_sel_genre_sel_dictionnaire = {"value_fk_film": id_film_selected,
                                                               "value_fk_genre": id_genre_del}

                    # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                    # la subtilité consiste à avoir une méthode "execute" dans la classe "DBconnection"
                    # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "DBconnection"
                    # sera interprété, ainsi on fera automatiquement un commit
                    mconn_bd.execute(strsql_delete_genre_film, valeurs_film_sel_genre_sel_dictionnaire)

        except Exception as Exception_update_genre_film_selected:
            raise ExceptionUpdateGenreFilmSelected(f"fichier : {Path(__file__).name}  ;  "
                                                   f"{update_mail_pers_selected.__name__} ; "
                                                   f"{Exception_update_genre_film_selected}")

    # Après cette mise à jour de la table intermédiaire "t_pers_mail",
    # on affiche les films et le(urs) genre(s) associé(s).
    return redirect(url_for('mail_pers_afficher', id_mail_sel=id_film_selected))


"""
    nom: genres_films_afficher_data

    Récupère la liste de tous les genres du film sélectionné par le bouton "MODIFIER" de "mail_pers_afficher.html"
    Nécessaire pour afficher tous les "TAGS" des genres, ainsi l'utilisateur voit les genres à disposition

    On signale les erreurs importantes
"""


def genres_films_afficher_data(valeur_id_film_selected_dict):
    print("valeur_id_film_selected_dict...", valeur_id_film_selected_dict)
    try:

        strsql_film_selected = """SELECT id_mail,nom_mail, GROUP_CONCAT(id_client) as persmail FROM t_pers_mail
                                        INNER JOIN t_client ON t_client.id_client = t_pers_mail.id_pers_mail
                                        INNER JOIN t_mail ON t_mail.id_mail = t_pers_mail.fk_mail
                                        WHERE id_mail = %(value_id_mail_selected)s"""

        strsql_genres_films_non_attribues = """SELECT id_client,nom FROM t_client WHERE id_client not in(SELECT id_client as persmail FROM t_pers_mail
                                                INNER JOIN t_client ON t_client.id_client = t_pers_mail.fk_client
                                                INNER JOIN t_mail ON t_mail.id_mail = t_pers_mail.fk_mail
                                                    WHERE id_mail = %(value_id_mail_selected)s)"""

        strsql_genres_films_attribues = """SELECT id_mail, id_client, nom FROM t_pers_mail
                                            INNER JOIN t_client ON t_client.id_client = t_pers_mail.fk_client
                                            INNER JOIN t_mail ON t_mail.id_mail = t_pers_mail.fk_mail
                                            WHERE id_mail = %(value_id_mail_selected)s"""

        # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
        with DBconnection() as mc_afficher:
            # Envoi de la commande MySql
            mc_afficher.execute(strsql_genres_films_non_attribues, valeur_id_film_selected_dict)
            # Récupère les données de la requête.
            data_genres_films_non_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("genres_films_afficher_data ----> data_genres_films_non_attribues ", data_genres_films_non_attribues,
                  " Type : ",
                  type(data_genres_films_non_attribues))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_film_selected, valeur_id_film_selected_dict)
            # Récupère les données de la requête.
            data_film_selected = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_film_selected  ", data_film_selected, " Type : ", type(data_film_selected))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_genres_films_attribues, valeur_id_film_selected_dict)
            # Récupère les données de la requête.
            data_genres_films_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_genres_films_attribues ", data_genres_films_attribues, " Type : ",
                  type(data_genres_films_attribues))

            # Retourne les données des "SELECT"
            return data_film_selected, data_genres_films_non_attribues, data_genres_films_attribues

    except Exception as Exception_genres_films_afficher_data:
        raise ExceptionGenresFilmsAfficherData(f"fichier : {Path(__file__).name}  ;  "
                                               f"{genres_films_afficher_data.__name__} ; "
                                               f"{Exception_genres_films_afficher_data}")
