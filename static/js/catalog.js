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

        var priceInputMax = document.getElementById("price-max"),
            priceInputMin = document.getElementById("price-min");

        priceInputMax.addEventListener("change", function () {
            updatePriceSlider($(this).parent(), this.value);
        });

        priceInputMin.addEventListener("change", function () {
            updatePriceSlider($(this).parent(), this.value);
        });

        function updatePriceSlider(elem, value) {
            if (elem.hasClass("price-min")) {
                priceSlider.noUiSlider.set([value, null]);
            } else if (elem.hasClass("price-max")) {
                priceSlider.noUiSlider.set([null, value]);
            }
        }

        // Price Slider
        var priceSlider = document.getElementById("price-slider");
        if (priceSlider) {
            noUiSlider.create(priceSlider, {
                start: [
                    data.current_min_price == ""
                        ? data.min_price
                        : Number(data.current_min_price),
                    data.current_max_price == ""
                        ? data.max_price
                        : Number(data.current_max_price),
                ],
                connect: true,
                step: 0.01,
                range: {
                    min: Number(data.min_price),
                    max: Number(data.max_price),
                },
            });

            priceSlider.noUiSlider.on("update", function (values, handle) {
                var value = values[handle];
                handle
                    ? (priceInputMax.value = value)
                    : (priceInputMin.value = value);
            });
        }
    });
})();
