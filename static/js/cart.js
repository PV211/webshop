async function updatePrice(price, id, update = false) {
    const quantity = $(`#quantity-${id}`).val();
    let newPrice = quantity * price;

    if ($(`#gift-${id}`).is(":checked")) {
        newPrice += 10;
    }

    if (update) {
        await fetch(`/cart/change/${id}?quantity=${quantity}`);
    }

    $(`#price-${id}`).text(`${formatPrice(newPrice)} грн`);

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

(() => {
    $(document).ready(() => updateTotalPrice());
})();
