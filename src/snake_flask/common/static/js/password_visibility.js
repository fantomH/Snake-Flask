/*
+-----------------------------------------------------------------------------+
[+] PASSWORD VISIBILITY

Show / hide a password input.
+-----------------------------------------------------------------------------+
*/

document.addEventListener("DOMContentLoaded", function () {

    document
        .querySelectorAll("[data-toggle-password]")
        .forEach(setupPasswordToggle);

});


function setupPasswordToggle(button) {

    const inputId = button.dataset.passwordInput;
    const input = document.getElementById(inputId);

    if (!input) {
        return;
    }

    button.addEventListener("click", function () {

        const icon = button.querySelector(
            ".material-symbols-outlined"
        );

        if (input.type === "password") {
            input.type = "text";

            if (icon) {
                icon.textContent = "visibility_off";
            }

        } else {
            input.type = "password";

            if (icon) {
                icon.textContent = "visibility";
            }
        }

    });

}
