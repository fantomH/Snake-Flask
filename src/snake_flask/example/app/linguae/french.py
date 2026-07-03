# +-------------------------------------------------------------------- INFO -+
# | [Snake-Flask/src/snake_flask/example/app/linguae/french.py]               |
# |                                                                           |
# | Author      : Pascal Malouin (https://github.com/fantomH)                 |
# | Created     : 2026-06-11 21:26:26 UTC                                     |
# | Updated     : 2026-07-01 18:49:37 UTC                                     |
# | Description : French dictionary.                                          |
# +---------------------------------------------------------------------------+

from markupsafe import Markup

EXAMPLE = {
    "BUTTON-save": "Sauvegarder",
    "HOME-title": "Bienvenu",
    "HOME-h1": "Bienvenu",
    "LOGIN-title": "Connexion",
    "LOGIN-h1": "Connexion",
    "LOGIN-user": "Utilisateur",
    "LOGIN-user_placeholder": "Entrez votre nom d'utilisateur",
    "LOGIN-password": "Mot de passe",
    "LOGIN-password_placeholder": "Entrez votre mot de passe",
    "LOGIN-login": "Connexion",
    "LOGIN-wrong_password": "Le nom d'utilisateur ou le mot de passe est incorrect.",
    "MYACCOUNT-title": "Mon compte",
    "MYACCOUNT-h1": "Mon compte ",
    "MYACCOUNT-firstname_label": "Prénom",
    "MYACCOUNT-lastname_label": "Nom",
    "MYACCOUNT-email_label": "Courriel",
    "MYACCOUNT-change_your_password": "Modification du mot de passe",
    "MYACCOUNT-current_password_label": "Mot de passe courant",
    "MYACCOUNT-current_password_placeholder": "Saisir votre mot de pass",
    "MYACCOUNT-new_password_label": "Nouveau mot de passe",
    "MYACCOUNT-new_password_placeholder": "Saisir le nouveau mot de passe",
    "MYACCOUNT-confirm_password_label": "Confirmation du mot de passe",
    "MYACCOUNT-confirm_password_placeholder": "Confirmer votre nouveau mot de passe",
    "SIGNUP-title": "Inscription",
    "SIGNUP-h1": "Inscription",
    "SIGNUP-message": Markup("Message<br/>Message"),
    "SIGNUP-cannot_be_empty": "ne peut être vide!",
    "SIGNUP-firstname": "Prénom",
    "SIGNUP-firstname_placeholder": "Entrer votre prénom",
    "SIGNUP-lastname": "Nom",
    "SIGNUP-lastname_placeholder": "Entrer votre nom de famille",
    "SIGNUP-user": "Utilisateur",
    "SIGNUP-user_already_exists": "L'utilisateur existe déjà!",
    "SIGNUP-user_placeholder": "Choisir un nom d'utilisateur",
    "SIGNUP-email": "Courriel",
    "SIGNUP-email_already_exists": "Ce courriel est déjà utilisé!",
    "SIGNUP-email_placeholder": "Entrer votre courriel",
    "SIGNUP-password1": "Mot de passe",
    "SIGNUP-password1_placeholder": "Choisir un mot de passe",
    "SIGNUP-invalid_password": Markup(
                                      """
                                      <strong>Exigences du mot de passe&nbsp;:</strong>
                                      <ul class="mb-0">
                                          <li>Au moins 8 caractères</li>
                                          <li>Une lettre minuscule</li>
                                          <li>Une lettre majuscule</li>
                                          <li>Un chiffre</li>
                                          <li>Un caractère spécial</li>
                                      </ul>
                                      """
                               ),
    "SIGNUP-password2": "Confirmation du mot de passe",
    "SIGNUP-password2_placeholder": "Confirmer votre mot de passe",
    "SIGNUP-submit_button": "Soumettre",
    "SIGNUP-passwords_dont_match": "Les mots de passe ne concordent pas!",
    "ADMIN-USERS-h1": "Utilisateurs",
    "USER-ACCOUNT-title": "Compte utilisateur",
    "USER-ACCOUNT-h1": "Compte utilisateur ",
    "USER-ACCOUNT-firstname_label": "Prénom",
    "USER-ACCOUNT-lastname_label": "Nom",
    "USER-ACCOUNT-email_label": "Courriel",
    "USER-ACCOUNT-change_password": "Modification du mot de passe",
    "USER-ACCOUNT-new_password_label": "Nouveau mot de passe",
    "USER-ACCOUNT-new_password_placeholder": "Saisir le nouveau mot de passe",
    "USER-ACCOUNT-confirm_password_label": "Confirmation du mot de passe",
    "USER-ACCOUNT-confirm_password_placeholder": "Confirmer le nouveau mot de passe",
    "USER-ACCOUNT-cannot_be_empty": "ne peut être vide",
}
