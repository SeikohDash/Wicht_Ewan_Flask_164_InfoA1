"""Gestion des formulaires avec WTF pour les films
Fichier : gestion_films_wtf_forms.py
Auteur : OM 2022.04.11

"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, NumberRange, DataRequired
from wtforms.validators import Regexp
from wtforms.widgets import TextArea


class FormWTFAddObjets(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_objets_regexp = ""
    nom_objets_wtf = StringField("Nom de l'objets ", validators=[Length(min=2, max=2000, message="min 2 max 20"),
                                                               Regexp(nom_objets_regexp,
                                                                      message="Pas de chiffres, de caractères "
                                                                              "spéciaux, "
                                                                              "d'espace à double, de double "
                                                                              "apostrophe, de double trait union")
                                                               ])
    cb_ean_regexp = ""
    cb_ean_wtf = StringField("Code Barre ", validators=[Length(min=2, max=2000, message="min 2 max 20"),
                                                             Regexp(cb_ean_regexp,
                                                                    message="Pas de chiffres, de caractères "
                                                                            "spéciaux, "
                                                                            "d'espace à double, de double "
                                                                            "apostrophe, de double trait union")
                                                             ])
    prix_regexp = ""
    prix_wtf = StringField("Prix ", validators=[Length(min=2, max=2000, message="min 2 max 20"),
                                                             Regexp(prix_regexp,
                                                                    message="Pas de chiffres, de caractères "
                                                                            "spéciaux, "
                                                                            "d'espace à double, de double "
                                                                            "apostrophe, de double trait union")
                                                             ])


    submit = SubmitField("Enregistrer Objets")


class FormWTFUpdateObjets(FlaskForm):
    """
        Dans le formulaire "film_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """

    nom_objets_update = StringField("Clavioter le nom de l'objets", widget=TextArea())
    cb_ean_update_wtf = StringField("Clavioter le nom de l'objets", widget=TextArea())
    prix_update_wtf = StringField("Clavioter le nom de l'objets", widget=TextArea())
    submit = SubmitField("Update film")


class FormWTFDeleteFilm(FlaskForm):
    """
        Dans le formulaire "film_delete_wtf.html"

        nom_film_delete_wtf : Champ qui reçoit la valeur du film, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "film".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_film".
    """
    nom_film_delete_wtf = StringField("Effacer ce film")
    submit_btn_del_film = SubmitField("Effacer film")
    submit_btn_conf_del_film = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
