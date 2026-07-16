/*
+---------------------------------------------------------------------- INFO -+
| [Snake-Flask/src/snake_flask/common/static/snake-common.js]                 |
|                                                                             |
| Author      : Pascal Malouin (https://github.com/fantomH)                   |
| Created     : 2026-07-03 11:36:26 UTC                                       |
| Updated     : 2026-07-03 12:00:01 UTC                                       |
| Description : Snake-Flask javascript.                                       |
+-----------------------------------------------------------------------------+
*/

/*
 * +--------------------------------------------------------------------------+
 * [+] INITIALIZATION                                                         |
 * |                                                                          |
 * | Run all common Snake-Flask JavaScript initializers once the DOM is ready.|
 * +--------------------------------------------------------------------------+
 */
document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".snake-list").forEach(setupSnakeList);

    document
        .querySelectorAll("[data-toggle-password]")
        .forEach(setupPasswordToggle);

    setupSubNavbar();
    setupAutoDismissAlerts();
    setupInactivityLogout();

});

/*
 * +--------------------------------------------------------------------------+
 * [+] AJAX PAGINATION                                                        |
 * |                                                                          |
 * | Generic AJAX search + pagination helper.                                 |
 * |                                                                          |
 * | Used by Snake-List and reusable by Snake-Table or other components.       |
 * +--------------------------------------------------------------------------+
 */

/*
 * setupAjaxPagination(options)
 *
 * Generic AJAX pagination engine.
 *
 * Responsibilities:
 *  - Search with debounce.
 *  - Page-size changes.
 *  - Previous / next pagination.
 *  - Abort stale fetch requests.
 *  - Replace the component body with server-rendered HTML.
 *  - Sync pagination state from the returned HTML fragment.
 */
function setupAjaxPagination(options) {

    const root = options.root;
    const dataUrl = root.dataset.url;

    const searchInput = root.querySelector(options.searchSelector);
    const pageSizeSelect = root.querySelector(options.pageSizeSelector);
    const body = root.querySelector(options.bodySelector);
    const previousButton = root.querySelector(options.previousSelector);
    const nextButton = root.querySelector(options.nextSelector);
    const info = root.querySelector(options.infoSelector);

    let page = 1;
    let timer = null;
    let controller = null;

    /*
     * Stop silently if the component is missing required elements.
     *
     * This keeps snake-common.js safe on pages where only part of the
     * JavaScript feature set is used.
     */
    if (
        !dataUrl ||
        !searchInput ||
        !pageSizeSelect ||
        !body ||
        !previousButton ||
        !nextButton ||
        !info
    ) {
        return;
    }

    /*
     * getBodyData()
     *
     * Return the hidden/state element inside the refreshed HTML fragment.
     *
     * The server should return an element matching options.dataSelector
     * with pagination data stored in data-* attributes.
     */
    function getBodyData() {
        return body.querySelector(options.dataSelector);
    }

    /*
     * syncFromBody()
     *
     * Read pagination metadata from the HTML fragment and update the UI.
     */
    function syncFromBody() {

        const data = getBodyData();

        if (!data) {
            return;
        }

        page = parseInt(data.dataset.page || "1", 10);

        const totalPages = parseInt(data.dataset.totalPages || "1", 10);
        const totalItems = parseInt(data.dataset.totalItems || "0", 10);
        const hasPrevious = data.dataset.hasPrevious === "true";
        const hasNext = data.dataset.hasNext === "true";

        previousButton.disabled = !hasPrevious;
        nextButton.disabled = !hasNext;

        info.textContent =
            `Page ${page} of ${totalPages} — ${totalItems} result${totalItems === 1 ? "" : "s"}`;

    }

    /*
     * buildUrl()
     *
     * Build the AJAX URL using the current search, page and page size.
     */
    function buildUrl() {

        const params = new URLSearchParams();

        params.set("q", searchInput.value);
        params.set("page", page);
        params.set("page_size", pageSizeSelect.value);

        return `${dataUrl}?${params.toString()}`;

    }

    /*
     * load()
     *
     * Fetch a new HTML fragment and replace the component body.
     *
     * If another request is already running, abort it so old responses
     * cannot overwrite newer results.
     */
    function load() {

        if (controller) {
            controller.abort();
        }

        controller = new AbortController();

        fetch(buildUrl(), {
            headers: {
                "X-Snake-Ajax-Pagination": "1",
                "X-Snake-List": "1",
            },
            signal: controller.signal,
        })
            .then(function (response) {
                return response.text();
            })
            .then(function (html) {
                body.innerHTML = html;
                syncFromBody();
            })
            .catch(function (error) {

                if (error.name !== "AbortError") {
                    console.error(error);
                }

            });

    }

    /*
     * debouncedLoad()
     *
     * Wait briefly before searching so we do not fetch on every keystroke.
     */
    function debouncedLoad() {

        clearTimeout(timer);

        timer = setTimeout(function () {
            page = 1;
            load();
        }, 300);

    }

    searchInput.addEventListener("input", debouncedLoad);

    pageSizeSelect.addEventListener("change", function () {
        page = 1;
        load();
    });

    previousButton.addEventListener("click", function () {

        if (page > 1) {
            page -= 1;
            load();
        }

    });

    nextButton.addEventListener("click", function () {
        page += 1;
        load();
    });

    syncFromBody();

}


/*
 * +--------------------------------------------------------------------------+
 * [+] SNAKE LIST                                                             |
 * |                                                                          |
 * | Snake-List initializer.                                                  |
 * +--------------------------------------------------------------------------+
 */

/*
 * setupSnakeList(list)
 *
 * Initialize one Snake-List component.
 *
 * Most of the work is delegated to setupAjaxPagination(), making the same
 * pagination engine reusable by Snake-Table later.
 */
function setupSnakeList(list) {

    setupAjaxPagination({
        root: list,
        bodySelector: ".snake-list-body",
        searchSelector: ".snake-list-search",
        pageSizeSelector: ".snake-list-page-size",
        previousSelector: ".snake-list-prev",
        nextSelector: ".snake-list-next",
        infoSelector: ".snake-list-info",
        dataSelector: ".snake-list-data",
    });

}


/*
 * +--------------------------------------------------------------------------+
 * [+] SNAKE TABLE                                                            |
 * |                                                                          |
 * | Optional Snake-Table initializer using the same AJAX pagination engine.   |
 * +--------------------------------------------------------------------------+
 */

/*
 * setupSnakeTable(table)
 *
 * Placeholder for Snake-Table.
 *
 * This function is intentionally not auto-called yet unless your templates
 * add ".snake-table" containers compatible with these selectors.
 */
function setupSnakeTable(table) {

    setupAjaxPagination({
        root: table,
        bodySelector: ".snake-table-body",
        searchSelector: ".snake-table-search",
        pageSizeSelector: ".snake-table-page-size",
        previousSelector: ".snake-table-prev",
        nextSelector: ".snake-table-next",
        infoSelector: ".snake-table-info",
        dataSelector: ".snake-table-data",
    });

}


/*
 * +--------------------------------------------------------------------------+
 * [+] SUB NAVBAR                                                             |
 * |                                                                          |
 * | Offset a sub-navbar so it sits below the parent navbar.                   |
 * +--------------------------------------------------------------------------+
 */

/*
 * setupSubNavbar()
 *
 * Detect the main navbar height and store it in a CSS variable.
 *
 * CSS can then use:
 *
 *     var(--sc-parent-navbar-height)
 */
function setupSubNavbar() {

    const parentNavbar = document.querySelector(".sc-main-navbar, body > nav.navbar");
    const subNavbar = document.querySelector(".sc-sub-navbar");

    if (!parentNavbar || !subNavbar) {
        return;
    }

    function setSubNavbarOffset() {

        const height = parentNavbar.offsetHeight;

        document.documentElement.style.setProperty(
            "--sc-parent-navbar-height",
            height + "px"
        );

    }

    setSubNavbarOffset();
    window.addEventListener("resize", setSubNavbarOffset);

}


/*
 * +--------------------------------------------------------------------------+
 * [+] AUTO DISMISS ALERTS                                                    |
 * |                                                                          |
 * | Automatically hide and remove Bootstrap-style alerts.                     |
 * +--------------------------------------------------------------------------+
 */

/*
 * setupAutoDismissAlerts()
 *
 * Hide every element with .auto-dismiss after 5 seconds.
 */
function setupAutoDismissAlerts() {

    const alerts = document.querySelectorAll(".auto-dismiss");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            alert.classList.remove("show");

            setTimeout(function () {
                alert.remove();
            }, 150);

        }, 5000);

    });

}


/*
 * +--------------------------------------------------------------------------+
 * [+] INACTIVITY LOGOUT                                                      |
 * |                                                                          |
 * | Redirect inactive users to /logout after a delay.                         |
 * +--------------------------------------------------------------------------+
 */

/*
 * setupInactivityLogout()
 *
 * Reset the inactivity timer whenever the user interacts with the page.
 */
function setupInactivityLogout() {

    let inactivityTimer;

    function resetInactivityTimer() {

        clearTimeout(inactivityTimer);

        inactivityTimer = setTimeout(function () {
            window.location.href = "authentication/logout";
        }, 60 * 60 * 1000); // 60 minutes

    }

    [
        "mousemove",
        "mousedown",
        "keypress",
        "touchstart",
        "scroll",
    ].forEach(function (event) {
        document.addEventListener(event, resetInactivityTimer);
    });

    resetInactivityTimer();

}


/*
+-----------------------------------------------------------------------------+
[+] PASSWORD TOGGLE

    Show / hide a password input.
+-----------------------------------------------------------------------------+
*/
function setupPasswordToggle(button) {

    const inputId = button.dataset.passwordInput;
    const input = document.getElementById(inputId);

    if (!input) {
        return;
    }

    button.addEventListener("click", function () {

        const icon = button.querySelector(".material-symbols-outlined");

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
