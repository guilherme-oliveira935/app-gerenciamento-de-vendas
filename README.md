# App de gerenciamento de vendas para um supermercado 
[![NPM](https://img.shields.io/npm/l/react)](https://github.com/guilherme-oliveira935/app-gerenciamento-de-vendas/blob/main/LICENSE) 

# Sobre o projeto

O app é uma aplicação full stack construido em Python com a biblioteca Kivy voltado para ser aplicado em diversas plataformas (windows, IOS, android e etc).

A aplicação consiste em um sistema em que um fornecedor pode salvar os dados de suas vendas para um determinado supermercado e visualizar aquelas que um grupo de pessoas que o auxiliam realizaram também.

O objetivo desse projeto é aprender mais sobre a biblioteca kivy, que é feita justamente para aplicações multiplataformas, além de ter um primeiro contato com APIs rest. Por esses motivos, a aplicação claramente apresenta muitas limitações, mas serve como alicerce para o desenvolvimentos de ideias parecidas.

## Layout do app
![Mobile 1](https://github.com/guilherme-oliveira935/assets/blob/main/foto_home_page_ge_vendas.png) ![Mobile 2](https://github.com/guilherme-oliveira935/assets/blob/main/foto_todas_vendas_page_ge_vendas.png)

![Mobile 3](https://github.com/guilherme-oliveira935/assets/blob/main/foto_add_venda_page_ge_vendas.png) ![Mobile 4](https://github.com/guilherme-oliveira935/assets/blob/main/foto_equipe_page_ge_vendas.png)

![Mobile 5](https://github.com/guilherme-oliveira935/assets/blob/main/ajustes_page_ge_vendas.png)

![Mobile 6](https://github.com/guilherme-oliveira935/assets/blob/main/foto_allfotos_page.png)

![Mobile 7](https://github.com/guilherme-oliveira935/assets/blob/main/foto_login_page.png)

![Mobile 8](https://github.com/guilherme-oliveira935/assets/blob/main/foto_cadastro_page.png)


## Tecnologias utilizadas
- Python
- Biblioteca Kivy
- Biblioteca Requests
- Biblioteca Partial
- Biblioteca urlib

# Como executar o projeto

## Pré-requisitos: Python 3
### Instalar as bibliotecas mencionadas
### Criar um projeto no firebase e ativar o firebase authentication por email e senha
### Criar o realtime database com uma chave "proximo_code" com o valor '1' (string)
### Clonar esse repisotório
### Substituir o valor da variável 'API_KEY' no arquivo myfirebase.py pela chave api do projeto no firebase
### Substituir o valor da variável 'base_URL' no arquivo myfirebase.py pela url do seu realtime database
## OBS:
Para um melhor nível de segurança, aplique ao realtime database as regras: 

```Firebase Realtime Database Security Rules Language
{
  "rules": {
    ".read": "query.orderByChild == 'codigo_compartilhavel'",  
    ".indexOn": ["codigo_compartilhavel"],
    
    "proximo_code": {
      ".read": "auth.uid !== null",
      ".write": "auth.uid !== null",
    },
    
    "$uid": {
    	".write": "$uid === auth.uid",
      ".read": "$uid === auth.uid",
    },
  }
}
```

Dessa maneira, você garante que:
- Os usuário so podem ler/modificar apenas suas próprias informações;
- o campo 'próximo_code' pode ser modificado por qualquer usuário que estiver logado, e só se estiver logado;
- o campo 'codigo_compartilhavel' pode ser usado como parâmetro ordenado nas requisições

# Autor

Guilherme Oliveira
