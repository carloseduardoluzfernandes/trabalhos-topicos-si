import csv
import re
import pandas as pd
import matplotlib.pyplot as plt
from serpapi import GoogleSearch


# Função principal para buscar vagas e exportar os dados em um CSV
def buscar_vagas(api_key):

    # Lista de palavras-chave gerais para pesquisa
    vagas = ["Desenvolvedor Java", "Desenvolvedor Python", "Desenvolvedor Frontend"]

    # Solicitação ao usuário sobre inclusão de filtros para modelo de trabalho
    print("Deseja incluir o filtro de modelo de trabalho?")
    print("1 - Sim")
    print("2 - Não")
    isModeloTrabalho = input("Digite o número correspondente: ")

    # Inicialização do filtro de modelo de trabalho
    if isModeloTrabalho == "1":
        modeloTrabalho = "" # Inicializa variável para armazenar o modelo escolhido
        print("Escolha o modelo de trabalho:")
        print("1 - Remoto")
        print("2 - Híbrido")
        print("3 - Presencial")
        modeloTrabalho_option = input("Digite o número correspondente: ")
        # Define o modelo de trabalho com base na escolha do usuário
        if modeloTrabalho_option == "1":
            modeloTrabalho = "remoto"
        elif modeloTrabalho_option == "2":
            modeloTrabalho = "hibrido"
        elif modeloTrabalho_option == "3":
            modeloTrabalho = "presencial"
    else:
        modeloTrabalho = ""

    # Solicita ao usuário o tipo de contratação (CLT ou PJ)
    print("Escolha o tipo de contratação:")
    print("1 - CLT")
    print("2 - PJ")
    tipoContratacao_option = input("Digite o número correspondente: ")
    tipoContratacao = ""
    if tipoContratacao_option == "1":
        tipoContratacao = "CLT"
    elif tipoContratacao_option == "2":
        tipoContratacao = "PJ"

    # Criação de um arquivo CSV para exportar os dados coletados
    with open('vagas_emprego.csv', mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file) # Objeto para escrever no CSV
        # Escreve o cabeçalho no arquivo CSV
        writer.writerow(["Título", "Empresa", "Localização", "Forma de Envio", "Link de Inscrição", "Senioridade"])

        # Itera pela lista de palavras-chave de busca
        for query in vagas:
            print(f"\nBuscando vagas para: {query}")

            # Parâmetros da busca na API SerpAPI
            params = {
                "engine": "google_jobs", # Define o mecanismo de busca
                "q": f"{query} {modeloTrabalho} {tipoContratacao}", # Combina filtros com palavra-chave
                "location": "Brazil", # Restringe a localização para o Brasil
                "hl": "pt-br", # Resultados em português
                "api_key": f"{api_key}" # Chave da API para autenticação
            }

            # Realiza a busca e converte os resultados para um dicionário
            search = GoogleSearch(params)
            results = search.get_dict()

            # Verifica se a chave 'jobs_results' está presente nos resultados
            if "jobs_results" in results:
                jobs_results = results["jobs_results"]

                # Verifica se existem resultados de vagas
                if jobs_results:
                    for job in jobs_results:
                        title = job.get("title", "N/A")  # Obtém o título da vaga
                        company_name = job.get("company_name", "N/A")  # Nome da empresa
                        location = job.get("location", "N/A")  # Localização
                        via = job.get("via", "N/A")  # Forma de envio
                        apply_options = job.get("apply_options", [])  # Opções de aplicação

                      
                        # Identifica a senioridade da vaga através do título
                        # Verifica padrões usando expressões regulares
                        title_lower = title.lower()
                        if re.search(r'\bjunior\b|\bjúnior\b|\bjr\b|\bjr\b', title_lower):  # Inclui "junior", "Júnior", "Jr" e "JR"
                            senioridade = "Junior"
                        elif re.search(r'\bpleno\b|\bpl\b', title_lower):  # Inclui "pleno" e "PL"
                            senioridade = "Pleno"
                        elif re.search(r'\bsenior\b|\bsênior\b|\bsr\b|\bsr\b', title_lower):  # Inclui "senior", "sênior", "sr" e "SR"
                            senioridade = "Senior"
                        elif re.search(r'\bpleno\b.*\bsenior\b|\bsenior\b.*\bpleno\b', title_lower):  # Para Pleno/Senior
                            senioridade = "Pleno/Senior"
                        else:
                            senioridade = "Outros"

                        # Adiciona as informações no arquivo CSV para cada link de inscrição disponível
                        for options in apply_options:
                            link = options.get("link", "N/A")  # Link para se inscrever
                            writer.writerow([title, company_name, location, via, link, senioridade])
                else:
                    print("Não foram encontrados resultados para esta pesquisa!")
            else:
                print("A chave que trás os resultados da busca não foi encontrada nos resultados!")

    print("Dados exportados para 'vagas_emprego.csv' com sucesso!")


# Função para gerar insights do CSV exportado
def gerar_insights(df, caminho_arquivo="insights.txt"):
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        # Insight 1: Número de vagas por empresa
        empresa_counts = df["Empresa"].value_counts().head(5)
        f.write("=== Insights sobre Vagas por Empresa ===\n")
        f.write("As 5 empresas com mais vagas são:\n")
        for empresa, count in empresa_counts.items():
            f.write(f"{empresa}: {count} vagas\n")
        f.write("\n")

        # Insight 2: Número de vagas por cidade
        localizacao_counts = df["Localização"].value_counts().head(5)
        f.write("=== Insights sobre Vagas por Localização ===\n")
        f.write("As 5 cidades com mais vagas são:\n")
        for cidade, count in localizacao_counts.items():
            f.write(f"{cidade}: {count} vagas\n")
        f.write("\n")

        # Insight 3: Número de vagas por senioridade
        senioridade_counts = df["Senioridade"].value_counts()
        f.write("=== Insights sobre Vagas por Senioridade ===\n")
        for senioridade, count in senioridade_counts.items():
            f.write(f"{senioridade}: {count} vagas\n")
        f.write("\n")

        # Insights gerais
        total_vagas = len(df)
        vagas_completo = df.dropna(subset=["Empresa", "Localização", "Senioridade"]).shape[0]
        vagas_incompleto = total_vagas - vagas_completo
        f.write("=== Insights Gerais ===\n")
        f.write(f"Total de vagas encontradas: {total_vagas}\n")
        f.write(f"Vagas com todos os dados completos: {vagas_completo}\n")
        f.write(f"Vagas com dados incompletos: {vagas_incompleto}\n")

        print(f"Insights gerados e salvos em {caminho_arquivo}")

def gerar_graficos(caminho_csv):
    # Lê o CSV
    df = pd.read_csv(caminho_csv)

    # Verifica se as colunas necessárias existem no CSV
    colunas_necessarias = ["Título", "Empresa", "Localização", "Forma de Envio", "Link de Inscrição", "Senioridade"]
    for coluna in colunas_necessarias:
        if coluna not in df.columns:
            raise ValueError(f"A coluna '{coluna}' não foi encontrada no arquivo CSV.")

    # Gráfico 1: Número de vagas por Empresa
    if "Empresa" in df.columns:
        plt.figure(figsize=(10, 6))
        empresa_counts = df["Empresa"].value_counts().head(18)
        eixos = empresa_counts.plot(kind="bar", color="orange")
        plt.title("Número de Vagas por Tipo de Contratação")
        plt.xlabel("Tipo de Contratação")
        plt.ylabel("Número de Vagas")
        plt.xticks(rotation=45,ha='right')
        for p in eixos.patches:
            eixos.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                        textcoords='offset points')
        plt.tight_layout()
        plt.savefig("grafico_tipo_contratacao.png")
        plt.show()

    # Gráfico 2: Número de vagas por cidade (localização)
    if "Localização" in df.columns:
        plt.figure(figsize=(10, 6))
        localizacao_counts = df["Localização"].value_counts() # Top 10 cidades
        eixos = localizacao_counts.plot(kind="bar", color="orange")
        plt.title("Número de Vagas por Cidade")
        plt.xlabel("Cidade")
        plt.ylabel("Número de Vagas")
        plt.xticks(rotation=45,ha='right')
        for p in eixos.patches:
                eixos.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                            textcoords='offset points')
        plt.tight_layout()
        plt.savefig("grafico_vagas_por_cidade.png")
        plt.show()

    # Gráfico 3: Número de vagas por senioridade
    if "Senioridade" in df.columns:
        plt.figure(figsize=(10, 6))
        senioridade_counts = df["Senioridade"].value_counts()
        eixos = senioridade_counts.plot(kind="bar", color="green")
        plt.title("Número de Vagas por Senioridade")
        plt.xlabel("Senioridade")
        plt.ylabel("Número de Vagas")
        plt.xticks(rotation=45,ha='right')
        for p in eixos.patches:
                eixos.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                            textcoords='offset points')
        plt.tight_layout()
        plt.savefig("grafico_senioridade.png")
        plt.show()

    gerar_insights(df)
 
# Chama a função principal
if __name__ == "__main__":
    buscar_vagas("7868b4fae526af77f1c4df4df6082c79193f307c073edf1ff6870fd6574fe485")
    caminho_csv = "vagas_emprego.csv"  # Substitua pelo caminho real do CSV gerado
    gerar_graficos(caminho_csv)   