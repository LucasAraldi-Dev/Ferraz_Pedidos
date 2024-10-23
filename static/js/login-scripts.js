document.getElementById("login-form").addEventListener("submit", async function(event) {
    event.preventDefault(); // Evita o comportamento padrão do envio do form

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/token", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                username: email,
                password: password
            })
        });

        const data = await response.json();
        const messageElement = document.getElementById("login-message");

        if (response.ok) {
            messageElement.textContent = "Login realizado com sucesso!";
            messageElement.style.color = "green";

            // Encaminha para a página de pedidos após 3 segundos
            setTimeout(() => {
                window.location.href = "./realizar_pedidos.html";
            }, 3000);
        } else {
            messageElement.textContent = data.detail || "Ocorreu um erro durante o login.";
            messageElement.style.color = "red";

            // Apaga a mensagem apos X segundos caso o erro aconteça
            setTimeout(() => {
                messageElement.textContent = ""; 
            }, 3000);
        }
    } catch (error) {
        console.error("Erro no login:", error);
        alert("Erro de conexão, tente novamente.");
    }
});
