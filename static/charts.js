function generateChartsProducts() {
    // Gráfico de barras - Produtos
    const ctxProdutos = document.getElementById('grafico_produtos').getContext('2d');
    new Chart(ctxProdutos, {
        type: 'bar',
        data: {
            labels: labelsProdutos,
            datasets: [{
                label: 'Quantidade de Itens',
                data: valoresProdutos,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function generateChartsCategory() {

    // Gráfico de pizza - Categorias
    const ctxCategorias = document.getElementById('grafico_categorias').getContext('2d');
    new Chart(ctxCategorias, {
        type: 'pie',
        data: {
            labels: labelsCategorias,
            datasets: [{
                data: valoresCategorias,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true
        }
    });
}

generateChartsProducts();
generateChartsCategory();
