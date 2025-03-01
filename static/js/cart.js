function updatePrice(price, id) {
    const priceElm = $(`#price-${id}`);
    const checkbox = $(`#gift-${id}`);
    let newPrice = $(`#quantity-${id}`).val() * price;

    if (checkbox.is(":checked")) {
        newPrice += 10;
    }

    priceElm.text(`${formatPrice(newPrice)} грн`);

    updateTotalPrice();
}

function formatPrice(price) {
    return price.toLocaleString("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
}

function updateTotalPrice() {
    const totalPriceElm = $("#order-total");
    let total = 0;

    $("[id^='price-']").each((_, element) => {
        total += parseFloat($(element).text().replace(",", ""));
    });

    totalPriceElm.text(`${formatPrice(total)} грн`);
}

async function remove(id) {
    await fetch(`/cart/remove/${id}`)
        .then((response) => response.json())
        .then((response) => {
            if (response.success) {
                $(`#book-${id}`).remove();
            }
        });
}

(() => {
    $(document).ready(() => updateTotalPrice());
})();
