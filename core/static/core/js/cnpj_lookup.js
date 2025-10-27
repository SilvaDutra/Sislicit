// Arquivo: core/static/core/js/cnpj_lookup.js

// Garante que o script só rode depois que a página estiver totalmente carregada
document.addEventListener('DOMContentLoaded', function() {

    // Pega os elementos do formulário do admin pelos seus IDs
    const cnpjInput = document.querySelector('#id_cnpj');
    const razaoSocialInput = document.querySelector('#id_razao_social');
    const nomeFantasiaInput = document.querySelector('#id_nome_fantasia');
    // Adicione outros campos que a API possa retornar, se necessário

    // Se o campo CNPJ não existir na página, o script para aqui
    if (!cnpjInput) {
        return;
    }

    // Adiciona um "escutador" que dispara uma função quando o usuário
    // clica fora do campo CNPJ (evento 'blur')
    cnpjInput.addEventListener('blur', function() {
        // Pega o valor digitado no campo CNPJ
        let cnpj = cnpjInput.value;

        // Limpa o CNPJ, removendo tudo que não for número
        cnpj = cnpj.replace(/[^\d]/g, '');

        // Verifica se o CNPJ tem 14 dígitos. Se não, não faz nada.
        if (cnpj.length !== 14) {
            return;
        }

        // Mostra uma mensagem ao usuário
        console.log(`Buscando dados para o CNPJ: ${cnpj}...`);
        
        // Faz a chamada para a BrasilAPI usando a função fetch do navegador
        fetch(`https://brasilapi.com.br/api/cnpj/v1/${cnpj}`)
            .then(response => {
                // Se a resposta não for OK (ex: CNPJ não encontrado), gera um erro
                if (!response.ok) {
                    throw new Error('CNPJ não encontrado ou inválido.');
                }
                // Se a resposta for OK, converte os dados para JSON
                return response.json();
            })
            .then(data => {
                // Se tudo deu certo, preenche os campos do formulário com os dados recebidos
                console.log('Dados recebidos:', data);
                if (data.razao_social) {
                    razaoSocialInput.value = data.razao_social;
                }
                if (data.nome_fantasia) {
                    nomeFantasiaInput.value = data.nome_fantasia;
                }
                // Exemplo para preencher outros campos (descomente e ajuste se a API os retornar)
                // if (data.logradouro) {
                //     document.querySelector('#id_endereco').value = `${data.logradouro}, ${data.numero}`;
                // }
            })
            .catch(error => {
                // Se algo deu errado na chamada, mostra um erro no console e um alerta
                console.error('Erro ao buscar CNPJ:', error);
                alert(error.message);
            });
    });
});