/*
+-----------------------------------------------------------------------------+
[+] INACTIVITY LOGOUT

Redirect inactive users to /logout after a delay.
+-----------------------------------------------------------------------------+
*/

document.addEventListener("DOMContentLoaded", function () {

    setupInactivityLogout();

});


function setupInactivityLogout() {

    const config = window.SNAKE_ACCESS || {};

    const timeoutMinutes = Number(config.inactivityTimeoutMinutes);
    const logoutUrl = config.logoutUrl;

    /*
    [*] Disabled if the timeout is missing, invalid, or less than or equal to
        zero.
    */
    if (
        !Number.isFinite(timeoutMinutes)
        || timeoutMinutes <= 0
        || !logoutUrl
    ) {
        return;
    }

    const timeoutMilliseconds = timeoutMinutes * 60 * 1000;

    let inactivityTimer = null;
    let logoutStarted = false;

    function logoutInactiveUser() {

        if (logoutStarted) {
            return;
        }

        logoutStarted = true;

        window.location.assign(logoutUrl);

    }

    function resetInactivityTimer() {

        if (logoutStarted) {
            return;
        }

        clearTimeout(inactivityTimer);

        inactivityTimer = setTimeout(
            logoutInactiveUser,
            timeoutMilliseconds,
        );

    }

    [
        "mousemove",
        "mousedown",
        "keydown",
        "touchstart",
        "scroll",
    ].forEach(function (event) {
        document.addEventListener(
            event,
            resetInactivityTimer,
            { passive: true },
        );
    });

    resetInactivityTimer();

}
