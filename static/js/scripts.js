// Função para abrir o modal e preencher os campos com os dados do pedido
async function editarPedido(pedidoId) {
    console.log('Abrindo modal para editar o pedido:', pedidoId); // Adicione este log
    try {
        const response = await fetch(`/pedidos/${pedidoId}`);
        if (!response.ok) {
            throw new Error('Erro ao buscar os dados do pedido.');
        }
        const pedido = await response.json();
        

        // Preencher os campos com os dados recebidos
        document.getElementById('pedido-id-value').innerText = pedido.id; // Atualiza o ID do pedido
        document.getElementById('pedido-id').value = pedido.id; // Armazena o ID no campo oculto
        document.getElementById('setor').value = pedido.setor;
        document.getElementById('produto').value = pedido.produto;
        document.getElementById('quantidade').value = pedido.quantidade;
        document.getElementById('data_entrega').value = pedido.data_entrega;
        document.getElementById('status').value = pedido.status;
        document.getElementById('observacao').value = pedido.observacao;
        document.getElementById('responsavel_compra').value = pedido.responsavel_compra;

        // Abrir o modal
        document.getElementById('modalEditar').style.display = 'block';
    } catch (error) {
        console.error('Erro ao carregar o pedido:', error);
        document.getElementById('message').innerText = 'Erro ao carregar os dados do pedido.';
    }
    
}

// Fechar o modal
document.getElementById('fecharModal').onclick = function() {
    document.getElementById('modalEditar').style.display = 'none';
}

// Fechar o modal clicando fora dele
window.onclick = function(event) {
    const modal = document.getElementById('modalEditar');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

// Submissão do formulário de edição
document.getElementById('editarPedidoForm').onsubmit = async function(event) {
    event.preventDefault();
    const pedidoId = document.getElementById('pedido-id').value; // Obter ID do pedido oculto
    console.log('ID do pedido:', pedidoId); // Adicione este log para depuração
    const pedidoData = {
        setor: this.setor.value,
        produto: this.produto.value,
        quantidade: this.quantidade.value,
        data_entrega: this.data_entrega.value,
        status: this.status.value,
        observacao: this.observacao.value,
        responsavel_compra: this.responsavel_compra.value,
    };

    try {
        const response = await fetch(`/pedidos/${pedidoId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(pedidoData),
        });

        if (response.ok) {
            document.getElementById('modalEditar').style.display = 'none';
            alert(`Pedido número ${pedidoId} editado com sucesso!`);
            carregarPedidos(); // Atualiza a tabela de pedidos
        } else {
            const errorData = await response.json();
            alert(`Erro: ${JSON.stringify(errorData)}`); // Mostre o erro de forma legível
        }
    } catch (error) {
        console.error('Erro ao editar o pedido:', error);
    }
};

// Carregar os pedidos e adicionar os botões de editar
async function carregarPedidos() {
    const response = await fetch('/pedidos/');
    const pedidos = await response.json();
    const corpoTabela = document.getElementById('corpo-tabela');
    corpoTabela.innerHTML = '';

    pedidos.forEach(pedido => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${pedido.id}</td>
            <td>${pedido.setor}</td>
            <td>${pedido.produto}</td>
            <td>${pedido.quantidade}</td>
            <td>${pedido.data_entrega}</td>
            <td>${pedido.status}</td>
            <td>${pedido.observacao}</td>
            <td>${pedido.responsavel_compra}</td>
            <td><button class="btn-editar" onclick="editarPedido(${pedido.id})">Editar</button></td>
        `;
        corpoTabela.appendChild(row);
    });
}

window.onload = carregarPedidos;
