const form = document.getElementById("register-form");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const nome = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const senha = document.getElementById("password").value;
    
    const response = await fetch("/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: nome, email, password: senha })
    });

    const data = await response.json();
    const messageElement = document.getElementById("register-message");

    if (response.ok) {
        messageElement.textContent = "Cadastro realizado com sucesso.....";
        messageElement.style.color = "green";

        // Encaminha para a página de login apos o timeout setado.
        setTimeout(() => {
            window.location.href = "./login_pedidos.html";
        }, 2000); 
    } else {
        messageElement.textContent = data.detail || "Erro ao realizar o cadastro.";
        messageElement.style.color = "red";
    }
});