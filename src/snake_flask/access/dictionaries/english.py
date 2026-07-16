# +---------------------------------------------------------------------------+
# [+] INFO
# +---------------------------------------------------------------------------+
# [Snake-Flask/src/snake_flask/access/dictionaries/english.py]
# 
# Author      : Pascal Malouin (https://github.com/fantomH)
# Created     : 2026-07-06 12:07:22 UTC
# Updated     : 2026-07-15 11:04:11 UTC
# Description : SnakeAccess English dictionary.
# +---------------------------------------------------------------------------+

from markupsafe import Markup

SNAKE_ACCESS = {
    "SNAKE_ACCESS-MFA-setup_expired": "MFA setup expired. Please try again.",
    "SNAKE_ACCESS-MFA-configured_successfully": "MFA configured successfully.",
    "SNAKE_ACCESS-MFA-invalid_code": "Invalid MFA code.",
    "SNAKE_ACCESS-MFA-invalid_authentication_code": "Invalid authentication code.",
    "SNAKE_ACCESS-MFA-configure_mfa": "Configure MFA",
    "SNAKE_ACCESS-MFA-scan_qr_code": "Scan this QR code with Google Authenticator, Microsoft Authenticator,
            Authy, or another TOTP app."),
    "SNAKE_ACCESS-MFA-manual_secret": "Manual secret:",
    "SNAKE_ACCESS-MFA-enter_6_digit": "Enter the 6-digit code",
    "SNAKE_ACCESS-MFA-confirm_mfa": "Confirm MFA",
    "SNAKE_ACCESS-MFA-multifactor_authentication": "Multi-factor Authentication",
    "SNAKE_ACCESS-MFA-enter_6_digit_code_from_app": "Enter the 6-digit code from your authenticator application.",
    "SNAKE_ACCESS-MFA-authentication_code": "Authentication Code",
    "SNAKE_ACCESS-MFA-verify": "Verify",
    "SNAKE_ACCESS-wrong_password": "Wrong password.",
    "SNAKE_ACCESS-confirm_password": "Confirm password.",
    "SNAKE_ACCESS-enter_your_password": "Enter your password",
    "SNAKE_ACCESS-confirm": "Confirm",
    "BUTTON-save": "Save",
    "HOME-title": "Welcome",
    "HOME-h1": "Welcome",
    "LOGIN-title": "Log In",
    "LOGIN-h1": "Log In",
    "LOGIN-user": "User",
    "LOGIN-user_placeholder": "Enter your username",
    "LOGIN-password": "Password",
    "LOGIN-password_placeholder": "Enter your password",
    "LOGIN-login": "Log In",
    "LOGIN-wrong_password": "Username or password is incorrect.",
    "LOGIN-account_not_active": "Your account must be activated. Contact your administrator.",
    "LOGIN-please_sign_up": Markup(
        f'This account does not exist. '
        f'Please sign up '
        f'<a href="../sign-up/">here</a>'),
    "MYACCOUNT-title": "My Account",
    "MYACCOUNT-h1": "My Account ",
    "MYACCOUNT-firstname_label": "First Name",
    "MYACCOUNT-lastname_label": "Last Name",
    "MYACCOUNT-email_label": "Email",
    "MYACCOUNT-change_your_password": "Change your password",
    "MYACCOUNT-current_password_label": "Current password",
    "MYACCOUNT-current_password_placeholder": "Enter you current password",
    "MYACCOUNT-new_password_label": "New password",
    "MYACCOUNT-new_password_placeholder": "Enter your new password",
    "MYACCOUNT-confirm_password_label": "Confirmation of new password",
    "MYACCOUNT-confirm_password_placeholder": "Confirm your new password",
    "SIGNUP-title": "Sign Up",
    "SIGNUP-h1": "Sign Up",
    "SIGNUP-message": Markup("Message<br/>Message"),
    "SIGNUP-cannot_be_empty": "cannot be empty!",
    "SIGNUP-firstname": "First Name",
    "SIGNUP-firstname_placeholder": "Enter your first name",
    "SIGNUP-lastname": "Last Name",
    "SIGNUP-lastname_placeholder": "Enter your last name",
    "SIGNUP-user": "Username",
    "SIGNUP-user_already_exists": "User already exists!",
    "SIGNUP-user_placeholder": "Choose a username",
    "SIGNUP-email": "Email",
    "SIGNUP-email_already_exists": "Email already exists!",
    "SIGNUP-email_placeholder": "Enter your email",
    "SIGNUP-password1": "Password",
    "SIGNUP-password1_placeholder": "Choose a password",
    "SIGNUP-invalid_password": Markup(
                               """
                               <strong>Password requirements:</strong>
                               <ul class="mb-0">
                                   <li>At least 8 characters</li>
                                   <li>One lowercase letter</li>
                                   <li>One uppercase letter</li>
                                   <li>One number</li>
                                   <li>One special character</li>
                               </ul>
                               """
                               ),
    "SIGNUP-password2": "Password Confirmation",
    "SIGNUP-password2_placeholder": "Confirm your password",
    "SIGNUP-submit_button": "Submit",
    "SIGNUP-passwords_dont_match": "Passwords don't match!",
    "SIGNUP-Account-created.": "Account created.",
    "ADMIN-USERS-h1": "Users",
    "USER-ACCOUNT-title": "User Account",
    "USER-ACCOUNT-h1": "User Account ",
    "USER-ACCOUNT-firstname_label": "First Name",
    "USER-ACCOUNT-lastname_label": "Last Name",
    "USER-ACCOUNT-email_label": "Email",
    "USER-ACCOUNT-change_password": "Change password",
    "USER-ACCOUNT-new_password_label": "New password",
    "USER-ACCOUNT-new_password_placeholder": "Enter new password",
    "USER-ACCOUNT-confirm_password_label": "Confirmation of new password",
    "USER-ACCOUNT-confirm_password_placeholder": "Confirm new password",
    "USER-ACCOUNT-cannot_be_empty": "cannot be empty",
    "USER-ACCOUNT-username-already-exists": "Username already exists.",
    "USER-ACCOUNT-email-already-exists": "Email already exists.",
    "USER-ACCOUNT-username": "Username",
    "USER-ACCOUNT-invalid-password": "Invalid password",
    "USER-ACCOUNT-passwords-dont-match": "Passwords don't match",
}
