/*
 * Snake-Lists
 *
 * Reserved for future behavior:
 * - auto-submit when per-page changes
 * - live search
 * - card selection
 * - keyboard navigation
 */

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".snake-list select").forEach(function (select) {
        select.addEventListener("change", function () {
            select.closest("form").submit();
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".snake-list").forEach(function (snakeList) {
        const form = snakeList.querySelector("form");
        const searchInput = form.querySelector("input[type='search']");
        const perPageSelect = form.querySelector("select");

        let timer = null;

        function submitSearch() {
            form.querySelector("input[name$='_page']").value = "1";
            form.submit();
        }

        searchInput.addEventListener("input", function () {
            clearTimeout(timer);

            timer = setTimeout(function () {
                submitSearch();
            }, 300);
        });

        perPageSelect.addEventListener("change", function () {
            submitSearch();
        });
    });
});
