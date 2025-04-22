# Conversor de Moedas

![Conversor de Moedas](https://img.shields.io/badge/Projeto-Conversor%20de%20Moedas-blue)

## Índice

- [Sobre](#sobre)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Instalação](#instalação)
  - [Pré-requisitos](#pré-requisitos)
  - [Via Docker](#via-docker)
  - [Via Aplicação Local](#via-aplicação-local)
- [Como Usar](#como-usar)

## Sobre

Este é um projeto simples para uma API de conversão de moedas. O objetivo é básico: você define qual a moeda que deseja converter, para qual outra moeda quer converter e quanto deseja converter. O resultado esperado é o valor convertido baseado na última cotação disponível.

O projeto tem poucas features, sendo uma logica básica de login e registro para gerarmos um bearer token para realizarmos a verificação das taxas.

O endpoint de gerar a conversão e o de visualizar as conversões do usuário..

O foco da arquitetura foi ser um arquitetura focada em dominios, baseada no DDD. 

A escolha de tecnologias ficou entre Django e o fastAPI, o django seria uma ótima opção por já ter toda uma estrutura pre-configurada, o que faria o teste ser apenas focado em montar a arquitetura e realizar a logica, mas acabei optando por um FastAPI mais "cru" para ter um controle total das coisas que estavam sendo feitas, poder gerar cada uma das logicas e estrutura de forma um pouco mais livre.

Eu quis focar bastante na parte de separar responsabilidades, deixar cada modulo independente, muito pensando em ficar mais fácil a manutenção ou debug

## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as variáveis de ambiente no seu arquivo `.env`:

1. Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

2. Agora adicione os seus valores reais nas variáveis de ambiente.

> ⚠️ **Importante**: Para realizar a conversão é necessário ter um `apiKey` válido.

3. Caso não tenha um API key válido, faça o registro ([Nesse site](https://apilayer.com/))

    3.1 Acesse ([essa api](https://apilayer.com/marketplace/exchangerates_data-api)) e realize a subscrição na api
## Instalação

### Pré-requisitos

- Docker instalado ([Windows/Mac](https://www.docker.com/products/docker-desktop/))
- Docker Compose (v2.0+)
- Python 3.8 ou superior (para execução local)
- pip (gerenciador de pacotes Python)

### Via Docker

1. Após configurar as variáveis de ambiente, construa o container:

```bash
docker-compose up -d --build
```

2. (Opcional) Para verificar se os containers foram iniciados corretamente:

```bash
docker-compose ps
```

### Via Aplicação Local

Para executar a aplicação localmente, também será necessário configurar as variáveis de ambiente conforme descrito anteriormente.

#### Criação e ativação do ambiente virtual

1. Crie um ambiente virtual Python:

```bash
python -m venv .venv
```

2. Ative o ambiente virtual:

   **Windows:**
   ```bash
   .\.venv\Scripts\activate
   ```

   **Linux/macOS:**
   ```bash
   source .venv/bin/activate
   ```

3. Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

4. Rode a aplicação
```bash
uvicorn src.index:app --host 0.0.0.0 --port 8000 --reload
```


## Como Usar
1. Após rodar a aplicação, acesse: ```/docs``` para ver a documentação da API
