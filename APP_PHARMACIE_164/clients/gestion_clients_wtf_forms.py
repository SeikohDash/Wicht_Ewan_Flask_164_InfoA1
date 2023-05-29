"""Gestion des formulaires avec WTF pour les films
Fichier : gestion_films_wtf_forms.py
Auteur : OM 2022.04.11

"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, NumberRange, DataRequired
from wtforms.validators import Regexp
from wtforms.widgets import TextArea


class FormWTFAddClient(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_client_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_client_wtf = StringField("Nom du client", validators=[Length(min=2, max=50, message="min 2 max 50 "),
                                                               Regexp(nom_client_regexp,
                                                                      message="Pas de chiffres, de caractères "
                                                                              "spéciaux, "
                                                                              "d'espace à double, de double "
                                                                              "apostrophe, de double trait union")
                                                               ])
    prenom_client_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    prenom_client_wtf = StringField("Prenom du client", validators=[Length(min=1, max=50, message="min 2 max 50"),
                                                                       Regexp(prenom_client_regexp,
                                                                              message="Pas de chiffres, de caractères "
                                                                                      "spéciaux, "
                                                                                      "d'espace à double, de double "
                                                                                      "apostrophe, de double trait union")
                                                                       ])
    date_nais_client_regexp = "^([0-9]{4})-([0-9]{2})-([0-9]{2})$"
    date_nais_client_wtf = StringField("Date de naissance (format : AAAA-MM-JJ)",
                                       validators=[Length(min=10, max=10, message="Date trop longue/court"),
                                                   Regexp(date_nais_client_regexp,

                                                          message="Le format de la date doit être AAAA-MM-JJ")])


    genres_dropdown_wtf = SelectField('Genres (liste déroulante)',
                                    validators=[DataRequired(message="Sélectionner un genre.")],
                                    validate_choice=False
                                    )



    assu_dropdown_wtf = SelectField('Assurance',
                                    validators=[DataRequired(message="Sélectionner une assurance.")],
                                    validate_choice=False
                                    )

    submit = SubmitField("Enregistrer le client")


class FormWTFUpdateClient(FlaskForm):
    """
        Dans le formulaire "client_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """

    nom_client_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_client_update_wtf = StringField("Nom du client", validators=[Length(min=2, max=50, message="min 2 max 50 "),
                                                              Regexp(nom_client_update_regexp,
                                                                     message="Pas de chiffres, de caractères "
                                                                             "spéciaux, "
                                                                             "d'espace à double, de double "
                                                                             "apostrophe, de double trait union")
                                                              ])
    prenom_client_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    prenom_client_update_wtf = StringField("Prenom du client", validators=[Length(min=1, max=50, message="min 2 max 50"),
                                                                    Regexp(prenom_client_update_regexp,
                                                                           message="Pas de chiffres, de caractères "
                                                                                   "spéciaux, "
                                                                                   "d'espace à double, de double "
                                                                                   "apostrophe, de double trait union")
                                                                    ])
    date_nais_client_update_regexp = "^([0-9]{4})-([0-9]{2})-([0-9]{2})$"
    date_nais_client_update_wtf = StringField("Date de naissance (format : AAAA-MM-JJ)",
                                       validators=[Length(min=10, max=10, message="Date trop longue/court"),
                                                   Regexp(date_nais_client_update_regexp,
                                                          message="Le format de la date doit être AAAA-MM-JJ")])
    genres_dropdown_update_wtf = SelectField('Genres (liste déroulante)',
                                             validators=[DataRequired(message="Sélectionner un genre.")],
                                             validate_choice=False,
                                             coerce=int
                                             )

    assu_maladie_client_update_regexp = ""
    assu_dropdown_update_wtf = SelectField('Genres (liste déroulante)',
                                             validators=[DataRequired(message="Sélectionner un genre.")],
                                             validate_choice=False,
                                             coerce=int
                                             )
    submit = SubmitField("Update Client")


class FormWTFDeleteClient(FlaskForm):
    """
        Dans le formulaire "client_delete_wtf.html"

        nom_film_delete_wtf : Champ qui reçoit la valeur du film, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "film".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_film".
    """
    nom_film_delete_wtf = StringField("Effacer ce client")
    submit_btn_del_film = SubmitField("Effacer client")
    submit_btn_conf_del_film = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
