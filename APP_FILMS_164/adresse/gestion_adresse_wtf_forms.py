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


class FormWTFAjouterAdresse(FlaskForm):
    """
        Dans le formulaire "adresse_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_rue_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ' \-]+$"
    nom_rue_wtf = StringField("Clavioter la rue", validators=[
        Length(min=2, max=20, message="min 2 max 20"),
        Regexp(nom_rue_regexp, message="Pas de chiffres, de caractères spéciaux, "
                                              "de double apostrophe ou de double trait union")
    ])

    npa_regexp = "^([0-9])+$"
    NPA_adresse_wtf = StringField("Clavioter le NPA", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(npa_regexp,
                                                                          message="Seulement des chiffres!")
                                                                   ])
    localite_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    localite_adresse_wtf = StringField("Clavioter la localité ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(localite_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    submit = SubmitField("Enregistrer Adresse")


class FormWTFUpdateAdresse(FlaskForm):
    """
        Dans le formulaire "adresse_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_rue_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ' \-]+$"
    nom_rue_update_wtf = StringField("Clavioter la rue", validators=[
        Length(min=2, max=20, message="min 2 max 20"),
        Regexp(nom_rue_update_regexp, message="Pas de chiffres, de caractères spéciaux, "
                                              "de double apostrophe ou de double trait union")
                                                ])

    NPA_adresse_update_regexp = "^([0-9])+$"
    NPA_adresse_update_wtf = StringField("Clavioter le NPA", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                  Regexp(NPA_adresse_update_regexp,
                                                                         message="Seulement des chiffres!")
                                                                  ])

    localite_adresse_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    localite_adresse_update_wtf = StringField("Clavioter la localité ",
                                       validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                   Regexp(localite_adresse_update_regexp,
                                                          message="Pas de chiffres, de caractères "
                                                                  "spéciaux, "
                                                                  "d'espace à double, de double "
                                                                  "apostrophe, de double trait union")
                                                   ])

    submit = SubmitField("Update Adresse")


class FormWTFDeleteAdresse(FlaskForm):
    """
        Dans le formulaire "adresse_delete_wtf.html"

        nom_adresse_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_adresse_delete_wtf = StringField("Effacer cette Adresse")
    submit_btn_del = SubmitField("Effacer Adresse")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
