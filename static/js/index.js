(() => {
    const data = document.currentScript.dataset;

    $(document).ready(() => {
        $(".toast").toast("show");

        // JavaScript для керування чатом
        const chatModal = document.getElementById("chatModal");
        const openChatButton = document.getElementById("openChatButton");
        const closeChatButton =
            document.getElementsByClassName("close-chat")[0];
        const chatInput = document.getElementById("chatInput");
        const sendChatButton = document.getElementById("sendChatButton");
        const chatBody = document.getElementById("chatBody");

        // Відкриття чату
        openChatButton.onclick = function (event) {
            event.stopPropagation();
            chatModal.style.display = "block";
        };

        // Закриття чату
        closeChatButton.onclick = function () {
            chatModal.style.display = "none";
        };

        // Закриття чату при кліку поза ним
        window.onclick = function (event) {
            if (!event.target.closest("#chatModal")) {
                chatModal.style.display = "none";
            }
        };

        // Відправка повідомлення через API
        sendChatButton.addEventListener("click", function () {
            const message = chatInput.value.trim();
            if (message) {
                // Додаємо повідомлення користувача до чату
                addMessageToChat("You", message, "user");
                chatInput.value = "";

                fetch("/consult/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-CSRFToken": data.csrftoken,
                    },
                    body: new URLSearchParams({
                        message: message,
                    }),
                })
                    .then((response) => response.json())
                    .then((data) => {
                        let responseText = "";
                        if (data.choices && data.choices.length > 0) {
                            responseText = data.choices[0].message.content;
                        } else if (data.response) {
                            responseText = data.response;
                        } else {
                            responseText =
                                "Виникла помилка при отриманні відповіді.";
                        }
                        addMessageToChat(
                            "Консультант",
                            responseText,
                            "consultant"
                        );
                    })
                    .catch((error) => {
                        console.error("Помилка:", error);
                        addMessageToChat(
                            "Консультант",
                            "Виникла помилка при обробці запиту.",
                            "consultant"
                        );
                    });
            }
        });

        // Функція для додавання повідомлення до чату
        function addMessageToChat(sender, message, type) {
            const messageDiv = document.createElement("div");
            messageDiv.className = `chat-message ${type}`;
            messageDiv.innerHTML = `<strong>${sender}:</strong> <span>${message}</span>`;
            chatBody.appendChild(messageDiv);
            chatBody.scrollTop = chatBody.scrollHeight; // Автоматичний скрол донизу
        }

        // Відправка повідомлення при натисканні Enter
        chatInput.addEventListener("keypress", function (event) {
            if (event.key === "Enter") {
                sendChatButton.click();
            }
        });

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
            });

            up.on("click", function () {
                var value = parseInt($input.val()) + 1;
                $input.val(value);
                $input.change();
            });
        });
    });
})();
