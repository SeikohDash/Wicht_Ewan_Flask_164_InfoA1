"""
    Fichier : gestion_genres_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp
from wtforms.validators import Email

class FormWTFAjouterMail(FlaskForm):
    """
        Dans le formulaire "mail_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_mail_regexp = ""
    nom_mail_wtf = StringField("Clavioter le mail ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                  Email(message="Adresse e-mail invalide")
                                                                   ])
    submit = SubmitField("Enregistrer mail")


class FormWTFUpdateMail(FlaskForm):
    """
        Dans le formulaire "mail_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_mail_update_regexp = ""
    nom_mail_update_wtf = StringField("Clavioter le mail ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Email(message="Adresse e-mail invalide")
                                                                          ])

    submit = SubmitField("Update mail")


class FormWTFDeleteMail(FlaskForm):
    """
        Dans le formulaire "mail_delete_wtf.html"

        nom_mail_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_mail_delete_wtf = StringField("Effacer ce mail")
    submit_btn_del = SubmitField("Effacer mail")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
