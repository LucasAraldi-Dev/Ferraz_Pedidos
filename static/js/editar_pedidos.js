document.addEventListener('DOMContentLoaded', async () => {
    // Obtém o pedidoID da query da URL, em fase de testes...
    const params = new URLSearchParams(window.location.search);
    const pedidoId = params.get('pedidoId');

    if (pedidoId) {
        try {
            console.log(`Buscando dados do pedido: ${pedidoId}`);

            // Faz a requisição para buscar os dados do pedido correspondente
            const response = await fetch(`/pedidos/${pedidoId}`);
            
            // Verifica se a resposta deu OK , caso contrario exibe o erro.
            if (!response.ok) {
                throw new Error('Erro ao buscar os dados do pedido.');
            }
            //Console log para teste
            const pedido = await response.json();
            console.log("Dados recebidos:", pedido); // Adiciona o log dos dados recebidos para teste de futuras melhorias

            // Exibe o ID no topo da página
            document.getElementById('pedido-id').textContent = pedido.id;

            // Completa os campos do formulário com os dados do pedido encontrado
            document.getElementById('setor').value = pedido.setor || '';  // Colocando valores padrões vazios caso undefined para não dar crash.
            document.getElementById('produto').value = pedido.produto || '';
            document.getElementById('quantidade').value = pedido.quantidade || 1;
            document.getElementById('data_entrega').value = pedido.data_entrega || '';
            document.getElementById('status').value = pedido.status || 'Pendente';
            document.getElementById('observacao').value = pedido.observacao || '';
            document.getElementById('responsavel_compra').value = pedido.responsavel_compra || '';
            document.getElementById('pedidoId').value = pedido.id;

        } catch (error) {
            console.error('Erro:', error);
            document.getElementById('message').textContent = 'Erro ao carregar os dados do pedido.';
        }
    }
});
