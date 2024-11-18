# Projeto: Busca de Vagas e Visualização de Dados  

Este projeto permite "buscar vagas de emprego" utilizando a API do Google Jobs, "exportá-las" para um arquivo CSV e "gerar insights e gráficos" baseados nos dados coletados.

---

## 📋 Funcionalidades  

- **"Busca de vagas de emprego"** por palavras-chave, modelo de trabalho (remoto, híbrido, presencial) e tipo de contratação (CLT ou PJ).
- **"Exportação dos resultados para um arquivo CSV"** contendo informações sobre as vagas.
- **"Geração de insights"** sobre os dados, incluindo:
  - **"Número de vagas por empresa"**.
  - **"Número de vagas por cidade"**.
  - **"Número de vagas por senioridade"**.
  - **"Contagem de vagas com dados completos ou incompletos"**.
- **"Geração de gráficos"** para visualização dos dados:
  - **"Gráfico de Barras"**: Vagas por tipo de contratação.
  - **"Gráfico de Barras"**: Vagas por cidade.
  - **"Gráfico de Barras"**: Vagas por senioridade.
---

## 🛠️ Requisitos  

### Dependências do Python  

- **Python 3.8+**
- **Bibliotecas Python:**
  - `csv` (nativa do Python).
  - `re` (nativa do Python).
  - `serpapi`: "Biblioteca para consumir a API do Google Jobs".
    Para instalar, execute:
    ```bash
    pip install google-search-results
    ```
  - `pandas`: "Para manipulação e análise de dados".
    Para instalar, execute:
    ```bash
    pip install pandas
    ```
  - `matplotlib`: "Para geração de gráficos".
    Para instalar, execute:
    ```bash
    pip install matplotlib
    ```

## 🚀 Como Configurar e Executar o Projeto  

### Passo 1: Obter uma Chave de API do SerpAPI  

1. Acesse [SerpAPI](https://serpapi.com/).  
2. Crie uma conta e obtenha sua chave de API.  

### Passo 2: Configurar a Busca de Vagas  

1. Clone este repositório ou copie os arquivos para seu ambiente local.  
2. Substitua a API Key no código Python no trecho:  
   
   ```python
   buscar_vagas("SUA_API_KEY_AQUI")

### Passo 3: Executar o Código Python

1. Certifique-se de que está no diretório onde está o arquivo vagas.py.

2. Execute o script:

    ```bash
    python vagas.py
    ```
* Siga as instruções no terminal para configurar sua busca:

    1. Escolha palavras-chave, modelo de trabalho e tipo de contratação.

    2. O script gerará o arquivo vagas_emprego.csv e imagens .png dos gráficos com os resultados.

    3. O script gerará também insights sobre os gráficos gerados.


--------------------------------

## 📁 Estrutura do Projeto

 ```bash
.
├── vagas.py         # Script Python para buscar vagas e gerar o CSV.
├── index.html       # Interface web para upload e visualização dos dados.
├── README.md        # Instruções do projeto.
```
💡 Notas Adicionais
Cuidado com os Limites da API: 
* Certifique-se de não exceder o número de requisições permitido pelo SerpAPI para sua chave de API (100 requisições). 
* Personalização: Adicione palavras-chave ou outros filtros diretamente na lista vagas no código Python.
* Compatibilidade: O arquivo index.html foi testado nos navegadores Chrome, Firefox e Edge.
