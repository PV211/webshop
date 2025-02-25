$(document).ready(() => {
    // Input number
    $(".input-number").each(function () {
        var $this = $(this),
            $input = $this.find('input[type="number"]'),
            up = $this.find(".qty-up"),
            down = $this.find(".qty-down");

        down.on("click", function () {
            var value = parseInt($input.val()) - 1;
            value = value < 1 ? 1 : value;
            $input.val(value);
            $input.change();
            updatePriceSlider($this, value);
        });

        up.on("click", function () {
            var value = parseInt($input.val()) + 1;
            $input.val(value);
            $input.change();
            updatePriceSlider($this, value);
        });
    });

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
            start: [Number(priceInputMin.value), Number(priceInputMax.value)],
            connect: true,
            step: 1,
            range: {
                min: Number(priceInputMin.value),
                max: Number(priceInputMax.value),
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
