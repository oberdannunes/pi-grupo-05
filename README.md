![FastLog](media/fastlog-logo.png)

# Sistema de consulta de entregas para os setores Comercial e Logístico da empresa Doce Festa

Este projeto consiste em o desenvolvimento inicial de um sistema web para consulta do status de entregas na empresa Doce Festa, que atua no ramo de produtos para festas. O principal objetivo do sistema é desenvolver um sistema web que centralize os dados de entrega, permitindo consultas rápidas e confiáveis.

A motivação por trás do desenvolvimento desta ferramenta é dificuldade de comunicação entre os setores Comercial e Logístico, devido ao uso de planilhas e contatos informais, o que gera atrasos, retrabalho e risco de informações desatualizadas.

## Tecnologias Utilizadas

O ecossistema do projeto foi construído utilizando tecnologias robustas e amplamente adotadas no mercado para garantir desempenho e escalabilidade.

- Python
- PostgreSQL
- Django
- Bootstrap
- Git e GitHub
- HTML5 e CSS3

A escolha da stack Python/Django/PostgreSQL baseia-se no equilíbrio entre velocidade de entrega e robustez técnica. O Python fornece uma base sólida e legível para o desenvolvimento; o Django acelera a construção da aplicação com segurança e padrões de projeto consolidados; e o PostgreSQL garante que os dados sejam armazenados em um ambiente performático e extensível.

Onde o sistema está funcionando? O sistema oficial já está rodando na internet e pode ser acessado por este link: https://fastlog.bravemoss-a1b57c9b.centraluz.azurecontainerapps.io/

## Como Funciona (Passo a Passo)

Este guia explica como preparar um computador (com Windows 10 ou 11) para rodar o FastLog, mostrando os programas necessários, o passo a passo da instalação e como o sistema lê planilhas do Excel automaticamente.

### Como o Sistema é Organizado por Dentro (Arquitetura)

O FastLog funciona em três camadas organizadas (chamadas de padrão MVT):

1. **O Banco de Dados (Model)**: Onde ficam guardadas as informações organizadas (País, Estado, Cidade, Transportadora, Cliente e Pedido).

2. **O Visual (Template)**: O que o usuário vê na tela (as páginas do site, os botões de busca).

3. **O Cérebro (View)**: O meio de campo. Quando você clica em um botão, o cérebro processa o pedido, busca a informação no Banco de Dados e mostra na tela do Usuário.

### Passo a Passo para Instalar no Computador

Para colocar o sistema para funcionar no seu computador local, siga as etapas abaixo:

#### Passo 1: Baixar o Código (Clonagem)

Você precisa ter o programa Git instalado. Abra o terminal (prompt de comando) do seu computador e digite:

```bash
git clone https://github.com/oberdannunes/pi-grupo-05.git

cd pi-grupo-05
```

Isso vai baixar uma pasta com todos os arquivos do projeto para o seu computador.

#### Passo 2: Criar uma "Caixa de Isolamento" (Ambiente Virtual)

Para que os programas do FastLog não entrem em conflito com outros programas que você já tem no computador, criamos um ambiente isolado. No terminal, digite:

```bash
python -m venv .venv

.venv\Scripts\activate
```

_(Nota: Se o Windows der um aviso de bloqueio, pode ser necessário autorizar a execução de scripts no seu PowerShell). Você saberá que deu certo quando aparecer um (.venv) no início da linha do comando._

#### Passo 3: Instalar os Pacotes Necessários

Com o ambiente isolado ativo, mude para a pasta do código e peça para o Python instalar todos os complementos de uma vez só:

```bash
cd src

pip install -r requirements.txt
```

#### Passo 4: Preparando o Banco de Dados e o Administrador

Agora precisamos criar a estrutura onde as informações serão salvas e a conta do "chefe" do sistema.

**Criar as tabelas:**

```bash
python manage.py migrate
```

**Criar o usuário administrador:**

```bash
python manage.py createsuperuser
```

O sistema vai pedir para você criar um nome de usuário, e-mail e uma senha (que deve ter pelo menos 8 caracteres e não pode ser apenas números).

Como Executar o Sistema

Para executar no seu computador, digite:

```bash
python manage.py runserver
```

Pronto! Agora abra o seu navegador de internet (Chrome, Edge, etc.) e digite o endereço:

http://localhost:8000

## Como Funciona (Passo a Passo para o usuário comum/cliente)

A jornada de utilização do sistema foi desenhada para ser simples e direta, exigindo poucos comandos por parte do usuário final.

O fluxo se inicia na página inicial da aplicação (http://localhost:8000), onde o usuário visualiza uma interface limpa com um campo centralizado de busca. Para realizar a consulta, o operador ou cliente deve digitar o número de CNPJ da empresa de interesse e o número de controle da nota fiscal (NFE).

Após preencher o campo e acionar o botão de busca, o sistema processa a requisição realizando uma varredura interna no banco de dados. Em poucos segundos, a tela exibe o resultado "Entregue" ou "Entrega em andamento".

Para uma nova consulta, há o botão "Voltar" do navegador aparece na exibição do status

Preenchendo somente CNPJ ou NFE têm a mensagem "Por favor, preencha ambos os campos: CNPJ e NFE.

## Como Funciona (Passo a Passo para o administrador)

Se você for o administrador e quiser gerenciar o sistema, o endereço é http://localhost:8000/admin (onde usará a senha criada no passo “Criar o usuário administrador”).

O administrador visualiza uma interface limpa com um campo centralizado de login e senha. Acessa o sistema, na sessão de pedidos e clica em Visualização. Irá parecer a lista dos pedidos já importados. Há duas possibilidade: cadastrar entrega por entrega ou cadastrar em lote. Por meio do botão "Upload Planilha de Carga", escolhe o arquivo e clica em processar. A validação e verificação de erros será realizada e dará retorno do que foi feito, finalizando o processo e podendo sair.

E se for o caso, apontará linhas inválidas.

### Regras para a Planilha Funcionar:

O arquivo do Excel precisa ter uma aba com o nome exato de "**FRETES CONSOLIDADA**" e deve conter as seguintes colunas obrigatórias:

- **TRANSPORTADORA** (Nome de quem vai levar)
- **DT. PEDIDO** (Data em que a compra foi feita)
- **NFE** (Número da Nota Fiscal)
- **RAZAO SOCIAL** (Nome da empresa do cliente)
- **CIDADE** (Cidade de entrega)
- **UF** (Estado, ex: SP)
- **PAÍS** (Geralmente BRASIL)

_Nota: Outras colunas como valor do frete ou data de entrega são opcionais._

### Como o sistema processa a planilha:

O FastLog lê a planilha linha por linha. Para garantir que nada dê errado, ele usa um sistema de segurança: **se uma linha tiver erro, ela é pulada e registrada em uma lista de erros, mas o restante da planilha continua sendo importado normalmente**.

Ao final, o sistema mostra um relatório: "X linhas foram importadas com sucesso e as linhas Y e Z deram erro". Isso evita que o banco de dados fique bagunçado ou com informações duplicadas. Essa função fica disponível apenas para o administrador dentro do painel de controle.



## Equipe de Desenvolvimento

- Aline Jady Cordeiro
- Bruno Henrique Cavasana
- Helton Cleiton de Souza
- Josse Givan Bombardi Ferreira
- Leandro Agiani Silva
- Mey Fan Porfírio Wai
- Oberdan Borges Nunes
- Wilker David Tosta Pinto