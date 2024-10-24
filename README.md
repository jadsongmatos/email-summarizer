# Projeto de Processamento e Resumo de Emails

Este projeto tem como objetivo processar emails armazenados no formato **Maildir**, extrair e limpar o conteúdo das mensagens, resumir o texto utilizando modelos de **Natural Language Processing (NLP)** e armazenar os dados resumidos em um banco de dados **DuckDB**.

## Índice

- [Projeto de Processamento e Resumo de Emails](#projeto-de-processamento-e-resumo-de-emails)
  - [Índice](#índice)
  - [Visão Geral](#visão-geral)
  - [Funcionalidades](#funcionalidades)
  - [Configuração](#configuração)
    - [Configurar o Caminho do Maildir](#configurar-o-caminho-do-maildir)
    - [Escolher o Modelo de Sumarização](#escolher-o-modelo-de-sumarização)
  - [Uso](#uso)
    - [Passos Executados pelo Script](#passos-executados-pelo-script)
  - [Estrutura do Banco de Dados](#estrutura-do-banco-de-dados)
  - [Personalização](#personalização)
    - [Ajustar Parâmetros do Sumarizador](#ajustar-parâmetros-do-sumarizador)
    - [Modificar Função de Limpeza](#modificar-função-de-limpeza)
    - [Alterar Estrutura do Banco de Dados](#alterar-estrutura-do-banco-de-dados)

## Visão Geral

Este script realiza as seguintes etapas:

1. **Leitura de Emails**: Acessa e lê emails armazenados em um diretório Maildir.
2. **Decodificação e Limpeza**: Decodifica cabeçalhos MIME (como assunto e remetente) e limpa o conteúdo dos emails, removendo links, imagens, tabelas e outros elementos indesejados.
3. **Resumo do Conteúdo**: Utiliza modelos de sumarização de texto (como **PEGASUS**, **T5** ou **LED**) para resumir o conteúdo dos emails.
4. **Armazenamento**: Insere os dados resumidos em um banco de dados DuckDB para fácil consulta e análise.

## Funcionalidades

- **Decodificação de Cabeçalhos MIME**: Manipula cabeçalhos codificados conforme RFC 2047.
- **Processamento de Conteúdo Multipart**: Lida com diferentes tipos de conteúdo, como `text/plain` e `text/html`.
- **Limpeza de Texto**: Remove elementos indesejados do texto, como URLs, e-mails, números, símbolos de moeda e pontuação.
- **Sumarização de Texto**: Resumo eficiente do conteúdo dos emails utilizando modelos avançados de NLP.
- **Armazenamento Eficiente**: Utiliza DuckDB para armazenar e consultar os dados de forma eficiente.

## Configuração

### Configurar o Caminho do Maildir

No script fornecido, localize a seguinte linha e ajuste o caminho para o diretório Maildir onde seus emails estão armazenados:

```python
maildir_path = '/caminho/para/seu/maildir/'
```

### Escolher o Modelo de Sumarização

Você pode selecionar diferentes modelos de sumarização ajustando o parâmetro `model_name_or_path`:

```python
summarizer = Summarizer(
    model_name_or_path="pszemraj/led-large-book-summary",
    # Outras configurações...
)
```

**Modelos disponíveis comentados no script:**

- `pszemraj/pegasus-x-large-book_synthsumm`
- `pszemraj/long-t5-tglobal-base-16384-book-summary`
- `pszemraj/led-large-book-summary`

## Uso

Execute o script principal para iniciar o processamento dos emails:

```bash
python process_emails.py
```

### Passos Executados pelo Script

1. **Inicialização do Sumarizador**: Configura e carrega o modelo de sumarização escolhido.
2. **Leitura e Decodificação dos Emails**: Abre o diretório Maildir e itera sobre cada mensagem, decodificando cabeçalhos e conteúdo.
3. **Limpeza do Conteúdo**: Remove elementos indesejados do texto dos emails.
4. **Sumarização**: Gera um resumo do conteúdo limpo de cada email.
5. **Armazenamento no DuckDB**: Insere os dados resumidos (assunto, remetente, corpo resumido e data) no banco de dados DuckDB.

## Estrutura do Banco de Dados

O banco de dados DuckDB criado (`emails2.duckdb`) contém a tabela `emails` com a seguinte estrutura:

| Coluna  | Tipo      | Descrição                  |
|---------|-----------|----------------------------|
| subject | TEXT      | Assunto do email           |
| sender  | TEXT      | Remetente do email         |
| body    | TEXT      | Conteúdo resumido do email |
| date    | TIMESTAMP | Data e hora do email       |

## Personalização

### Ajustar Parâmetros do Sumarizador

Você pode ajustar diversos parâmetros do sumarizador, como `num_beams`, `min_length`, `no_repeat_ngram_size`, entre outros, para otimizar a qualidade dos resumos:

```python
summarizer = Summarizer(
    model_name_or_path="pszemraj/led-large-book-summary",
    num_beams=4,
    min_length=16,
    no_repeat_ngram_size=3,
    # Outros parâmetros...
)
```

### Modificar Função de Limpeza

A função `cleartext` utiliza a biblioteca `cleantext` para limpar o texto. Você pode ajustar os parâmetros para remover ou manter diferentes tipos de conteúdo:

```python
texto_limpo = clean(
    texto_limpo,
    fix_unicode=True,
    to_ascii=False,
    lower=False,
    no_line_breaks=True,
    no_urls=True,
    # Outros parâmetros...
)
```

### Alterar Estrutura do Banco de Dados

Se desejar armazenar informações adicionais, modifique a criação da tabela e a lógica de inserção de dados:

```sql
CREATE TABLE IF NOT EXISTS emails (
    subject TEXT,
    sender TEXT,
    body TEXT,
    date TIMESTAMP PRIMARY KEY,
    -- Adicione novas colunas aqui
)
```