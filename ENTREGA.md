# Entrega do desafio final

O briefing pede um único upload no AI/R Learning contendo o link do PR, o link público do vídeo, uma cópia de “Como usei IA” e a reflexão pessoal. Conforme a atualização informada pelo Fellow, o prazo foi alterado para **25/11/2026, às 23h59 (horário de Brasília)**.

## O que já foi publicado

- [x] Repositório pessoal: https://github.com/Viuutu/desafio-final-verdejar
- [x] Branch de trabalho publicada: `codex/desafio-final-verdejar`.
- [x] Pull Request #1 integrado à `main`: https://github.com/Viuutu/desafio-final-verdejar/pull/1
- [x] Código, contrato, consultas, testes, guia, registro de IA e planilha no repositório.

## O que ainda falta para a entrega

- [x] Revisar e aprovar `COMO_USEI_IA.md`, confirmando que o relato corresponde à experiência do Fellow.
- [x] Revisar e aprovar a reflexão em primeira pessoa, dentro do limite de 10–20 linhas.
- [x] Confirmar com a coordenação como tratar o requisito de falha de teste. Na apresentação, descrever os fatos conforme a orientação recebida, sem transformar o erro de importação em uma falha de pytest.
- [ ] Gravar a defesa oral de 5–8 minutos, com tela e narração, seguindo a ordem do `GUIA_DE_DEFESA.md`.
- [ ] Publicar o vídeo com acesso público sem login.
- [ ] Atualizar o resumo abaixo com o link do vídeo, reflexão final e cópia da seção final de “Como usei IA”.
- [ ] Fazer o único upload deste arquivo no AI/R Learning.

## Resumo para o upload

**Pull Request:** https://github.com/Viuutu/desafio-final-verdejar/pull/1 (integrado à `main`)

**Vídeo público da defesa oral:** PENDENTE — gravar e publicar.

##Reflexão pessoal

Quando comecei este desafio, eu ainda não sabia muito bem como uma API, um programa em Python e um banco de dados trabalhavam juntos.
Ao longo do projeto, fui acompanhando a montagem do ETL e comecei a entender o caminho que os dados percorrem.
Uma das partes que mais me confundiu foi descobrir por que alguns totais dos pedidos não batiam com a soma dos itens.
Depois entendi que corrigir o total recebido só para os números coincidirem esconderia uma informação importante.
Por isso, o projeto mantém o valor informado pela origem, calcula a soma dos itens separadamente e sinaliza as diferenças.
Também tive dificuldade para organizar os terminais do VS Code, iniciar a API e conectar o PostgreSQL no Docker.
Quando um comando falhou, precisei parar, olhar a mensagem e tentar entender o que estava acontecendo em vez de apenas repetir.
Usei a IA em partes importantes do código, dos testes, da documentação e da planilha, e reconheço que essa ajuda foi ampla.
Isso foi além do papel limitado recomendado no desafio, então quero ser transparente sobre como trabalhei.
Minha contribuição foi definir o que eu precisava entregar, configurar as ferramentas, executar os passos e trazer minhas dúvidas e resultados.
Ainda estou aprendendo, mas hoje consigo explicar melhor como a extração, a transformação, a carga e a validação se conectam.
Na revisão atual, os 11 testes passaram; a reconciliação registrada para o banco teve diferença de R$ 0,00.
Se eu tivesse mais uma semana, deixaria a inicialização dos serviços mais simples e praticaria a apresentação do projeto.
Antes da defesa, quero revisar as decisões com calma para conseguir explicá-las com minhas palavras, sem apenas ler o código. O que mais levo deste desafio é que pedir ajuda também exige conferir o resultado e assumir responsabilidade pelo que vou apresentar.

## Conferência do vídeo

Confirme que o vídeo pode ser aberto sem login e mostra: execução do ETL com contadores; explicação linha a linha de um trecho aceito da IA; uma sugestão real rejeitada; pytest passando e uma falha real de teste corrigida; consulta mensal e igualdade entre a soma dos meses e a soma geral. O briefing permite que o PR esteja aberto ou integrado; o PR deste projeto já foi integrado.
