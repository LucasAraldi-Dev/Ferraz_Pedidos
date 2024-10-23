document.getElementById("pedidoForm").onsubmit = async function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);

    const response = await fetch("/pedidos/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const messageElement = document.getElementById("message");

    if (response.ok) {
        const result = await response.json();
        messageElement.innerText = `Pedido número ${result.id} enviado com sucesso!`;
        messageElement.style.color = "green"; // Adiciona cor de sucesso
        event.target.reset(); // Limpa o formulário

        // Remove a mensagem após 5 segundos
        setTimeout(() => {
            messageElement.innerText = "";
        }, 3000);

    } else {
        messageElement.innerText = "Erro ao enviar o pedido.";
        messageElement.style.color = "red"; // Adiciona cor de erro

        // Remove a mensagem de erro após 5 segundos
        setTimeout(() => {
            messageElement.innerText = "";
        }, 3000);
    }
};
