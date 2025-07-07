# **Techno Set Harmonizado: Um Pipeline de Engenharia de Dados e Análise Musical**

*Um pipeline de dados completo que analisa uma coleção de músicas, extrai atributos de áudio e as ordena de forma inteligente para criar um DJ set coeso e harmônico, pronto para ser usado em softwares como o rekordbox.*

## **📖 Introdução**

Este projeto nasceu da minha paixão pela música eletrónica e pela ciência de dados. O objetivo é automatizar uma das tarefas mais complexas e criativas de um DJ: a criação de um set com uma progressão de energia e harmonia perfeitas. Partindo de uma coleção local de ficheiros de áudio, este pipeline realiza a análise de cada faixa, extrai o seu Ritmo (BPM) e Tonalidade Musical, e aplica um algoritmo de ordenação baseado em regras de mixagem harmônica (usando o sistema Camelot) para gerar uma playlist final pronta para uso prático.

## **✨ Funcionalidades Principais**

* **Análise de Áudio Local:** Processamento direto de ficheiros de áudio (.flac) para extrair características musicais.  
* **Deteção de BPM e Tonalidade:** Utilização da biblioteca librosa para implementar um algoritmo de deteção de ritmo e um modelo de correspondência de perfis (baseado em Krumhansl-Kessler) para uma estimativa precisa da tonalidade (tom e escala).  
* **Engenharia de Atributos:** Conversão automática da tonalidade musical para o sistema da Roda de Camelot, facilitando a mixagem harmônica.  
* **Algoritmo de Ordenação de DJ Set:** Implementação de um algoritmo personalizável que ordena as faixas priorizando a compatibilidade de ritmo (BPM) e harmonia (Chave Camelot).  
* **Automação de Ficheiros:** Criação automática de uma pasta de DJ set final, com os ficheiros de áudio numerados para manter a ordem.  
* **Escrita de Metadados:** Gravação automática dos dados de BPM e Tom (Camelot) diretamente nas tags dos ficheiros de áudio, garantindo compatibilidade com softwares de DJ como o rekordbox.

## **🚀 A Jornada: Desafios e Soluções**

Um dos aspetos mais marcantes deste projeto foi a superação de desafios do mundo real.

A abordagem inicial previa o uso da API do Spotify. No entanto, durante o desenvolvimento, encontrei um erro 403 Forbidden persistente e não documentado ao tentar aceder ao endpoint de audio-features. Após uma depuração exaustiva, que incluiu testes com diferentes fluxos de autenticação e permissões (scopes), e uma pesquisa aprofundada na documentação e em fóruns, confirmei que o endpoint estava efetivamente depreciado ou inacessível para o meu tipo de aplicação.

**O Pivô Estratégico:** Em vez de abandonar o projeto, tomei a decisão de pivotar para uma solução de **análise de áudio local**. Esta mudança não só resolveu o problema, como tornou o projeto mais robusto e demonstrou uma competência crucial: a capacidade de adaptar-se e encontrar soluções alternativas face a bloqueios externos. A análise local com a biblioteca librosa garantiu 100% de cobertura de dados para a minha coleção de músicas, resultando num produto final de maior qualidade e controlo.

## **🛠️ Tecnologias Utilizadas**

* **Linguagem:** Python 3  
* **Análise e Manipulação de Dados:** Pandas  
* **Análise de Áudio:** Librosa, NumPy  
* **Manipulação de Metadados de Áudio:** Mutagen  
* **Gestão de Ambiente:** venv

## **⚙️ Como Executar o Projeto**

1. **Clone o Repositório:**  
   git clone \[URL\_DO\_SEU\_REPOSITORIO\_AQUI\]  
   cd TechnoSetHarmonizado

2. **Crie e Ative o Ambiente Virtual:**  
   python3 \-m venv venv  
   source venv/bin/activate  \# No macOS/Linux  
   \# venv\\Scripts\\activate  \# No Windows

3. **Instale as Dependências:**  
   pip install \-r requirements.txt

4. **Organize os seus Ficheiros de Áudio:**  
   * Crie uma pasta chamada musicas\_flac/ dentro do diretório principal.  
   * Coloque todos os seus ficheiros de áudio (.flac) dentro desta pasta. É recomendado que os nomes sigam o padrão Artista \- Nome da Música.flac.  
5. **Execute os Scripts na Ordem Correta:**  
   * **Passo 1: Análise e Geração do Dataset**  
     python processar\_musicas.py

   * **Passo 2: Engenharia de Atributos (Chave de Camelot)**  
     python engenharia\_final.py

   * **Passo 3: Ordenação do Set**  
     python ordenar\_set.py

   * **Passo 4 (Opcional): Criação da Pasta para o DJ**  
     python criar\_pasta\_set.py

   * **Passo 5 (Opcional): Escrita dos Metadados**  
     python escrever\_metadados.py

**📂 Estrutura do Projeto**

* ## **processar\_musicas.py: Lê os ficheiros da pasta musicas\_flac/, analisa-os com librosa para extrair BPM e Tom, e gera o dataset\_final\_analisado.csv.**

* engenharia\_final.py: Carrega o dataset analisado, converte a tonalidade para o sistema Camelot e salva o playlist\_pronta\_para\_ordenar.csv.  
* ordenar\_set.py: Aplica o algoritmo de ordenação de DJ set e gera o dj\_set\_final\_ordenado.csv.  
* criar\_pasta\_set.py: Cria uma nova pasta com os ficheiros de áudio copiados e numerados na ordem do set.  
* escrever\_metadados.py: Escreve os metadados de BPM e Tom diretamente nos ficheiros de áudio na pasta do set final.  
* musicas\_flac/: Pasta para colocar os seus ficheiros de áudio de entrada.  
* DJ\_Set\_Final\_Ordenado/: Pasta de saída gerada com o set pronto para uso.

## **📊 Resultados**

O output final do projeto é uma pasta contendo as faixas de música ordenadas de forma inteligente, com nomes de ficheiro prefixados para manter a ordem e metadados embutidos para compatibilidade com softwares de DJ.