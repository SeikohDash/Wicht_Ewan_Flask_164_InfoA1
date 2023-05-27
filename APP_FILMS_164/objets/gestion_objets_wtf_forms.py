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

    nom_objets_regexp = "^[a-zA-Z]+$"
    nom_objets_wtf = StringField("Nom de l'objet ", validators=[
        Length(min=2, max=45, message="min 2 max 45"),
        DataRequired(message="Ce champ est obligatoire."),
        Regexp(nom_objets_regexp, message="Veuillez saisir uniquement des lettres.")
    ])

    cb_ean_regexp = "^[01]+$"
    cb_ean_wtf = StringField("Code Barre ", validators=[
        Length(min=2, max=500, message="min 2 max 500"),
        DataRequired(message="Ce champ est obligatoire."),
        Regexp(cb_ean_regexp, message="Veuillez saisir uniquement des caractères '0' ou '1'.")
    ])

    prix_regexp = "^\d+\.-$"
    prix_wtf = StringField("Prix ", validators=[
        Length(min=1, max=7, message="min 1 max 7"),
        DataRequired(message="Ce champ est obligatoire."),
        Regexp(prix_regexp, message="Veuillez saisir un prix valide se terminant par un point tiret '.-'")
    ])


    submit = SubmitField("Enregistrer Objets")


class FormWTFUpdateObjets(FlaskForm):
    """
        Dans le formulaire "film_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """

    nom_objets_update_regexp = "^[a-zA-Z]+$"
    nom_objets_update = StringField("Nom de l'objet ", validators=[
        Length(min=2, max=45, message="min 2 max 45"),
        DataRequired(message="Ce champ est obligatoire."),
        Regexp(nom_objets_update_regexp, message="Veuillez saisir uniquement des lettres.")
                                                                ])

    cb_ean_update_regexp = "^[01]+$"
    cb_ean_update_wtf = StringField("Code Barre ", validators=[
        Length(min=2, max=500, message="min 2 max 500"),
        DataRequired(message="Ce champ est obligatoire."),
        Regexp(cb_ean_update_regexp, message="Veuillez saisir uniquement des caractères '0' ou '1'.")
                                                                 ])

    prix_update_regexp = "^\d+\.-$"
    prix_update_wtf = StringField("Prix ", validators=[
        Length(min=1, max=5, message="min 1 max 5"),
        DataRequired(message="Ce champ est obligatoire."),
        Regexp(prix_update_regexp, message="Veuillez saisir un prix valide se terminant par un point tiret '.-'")
                                                             ])

    submit = SubmitField("Update Objets")


class FormWTFDeleteFilm(FlaskForm):
    """
        Dans le formulaire "objets_delete_wtf.html"

        nom_film_delete_wtf : Champ qui reçoit la valeur du film, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "film".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_film".
    """
    nom_film_delete_wtf = StringField("Effacer cette objets")
    submit_btn_del_film = SubmitField("Effacer objets")
    submit_btn_conf_del_film = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
