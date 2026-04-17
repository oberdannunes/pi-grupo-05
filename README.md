# pi-grupo-05

Projeto Integrador do Grupo 05 da Univesp - 2026

## 1. Configuração do ambiente desenvolvimento
1. Instalação do Python: 
    * https://www.python.org/downloads/

2. Clone do repositório do projeto
    * *git clone https://github.com/oberdannunes/pi-grupo-05.git*

3. Criação do virtual environment com o módulo venv
    * Entre no diretório raiz do projeto:
        * *cd pi-grupo-5*
    * Crie o venv:
        * *python3 -m venv .venv*
        * Obs: Aqui, dependendo da sua instalação pode ser *python* ou *python3*

4. Checagem
    * Uma vez que o venv tenha sido criado, o python já instala e configura o pip (que é um gerenciador de pacotes) dentro do venv
    * Para ativá-lo, a partir da pasta do projeto, rodar o comando abaixo:
        * (Windows CMD):
            * *.venv\scripts\activate.bat*
        * (Windows PowerShell):
            * *.venv\Scripts\Activate.ps1*
    * Ou, ao abrir a pasta do projeto no VSCode, ele automaticamente roda e ativa o venv
    * Pra testar se a ativação do venv funcionou:
        * Rode os comandos abaixo:
            * *pip --version*
        * O retorno deve ser o path onde ele está instalado, e deverá ser um path dentro do .venv

5. Instalação das dependências
    * Acesse a pasta src do projeto:
        * *cd src*
    * Rode o comando abaixo para que o PIP instale os módulos utilizados no projeto
        * *pip install -r requirements.txt*

6. Preparação da base local
    * A base de dados não está versionada (git), então vocês precisarão rodar os seguintes comandos para criar e incializar ela (sempre dentro da pasta src):
        * *python manage.py migrate*
        * *python manage.py createsuperuser*

7. Execução
    * Se tudo ocorreu bem até agora, e nada pegou fogo...
    * A partir da pasta src, rode o comando abaixo:
        * *python manage.py runserver*
    * Acesse a aplicação em http://localhost:8000
