(() => {
    const data = document.currentScript.dataset;

    $(document).ready(() => {
        if (data.sort != "") {
            document.querySelector("select[name='sort']").value = data.sort;
        }

        if (data.per_page != "") {
            document.querySelector("select[name='per_page']").value =
                data.per_page;
        }
    });
})();
