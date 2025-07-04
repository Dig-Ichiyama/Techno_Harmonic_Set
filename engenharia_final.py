import pandas as pd
import sys

# --- 1. CONFIGURAÇÃO ---
INPUT_PATH = 'dataset_final_analisado.csv'
OUTPUT_PATH = 'playlist_pronta_para_ordenar.csv'

# Dicionário completo para mapear Tonalidade -> Roda de Camelot
# Inclui sinónimos comuns (ex: G# e Ab)
CAMELOT_MAP = {
    # Tonalidades Maiores (B)
    'B major': '1B', 'F# major': '2B', 'C# major': '3B', 
    'G# major': '4B', 'D# major': '5B', 'A# major': '6B',
    'F major': '7B', 'C major': '8B', 'G major': '9B',
    'D major': '10B', 'A major': '11B', 'E major': '12B',
    # Tonalidades Menores (A)
    'G# minor': '1A', 'D# minor': '2A', 'A# minor': '3A',
    'F minor': '4A', 'C minor': '5A', 'G minor': '6A',
    'D minor': '7A', 'A minor': '8A', 'E minor': '9A',
    'B minor': '10A', 'F# minor': '11A', 'C# minor': '12A',
    # Sinónimos Enharmônicos (mesma nota, nome diferente)
    'Ab major': '4B', 'Eb major': '5B', 'Bb major': '6B',
    'Db major': '3B', 'Gb major': '2B',
    'Ab minor': '1A', 'Eb minor': '2A', 'Bb minor': '3A',
}

# --- 2. CARREGAR O DATASET ANALISADO ---
print(f"A carregar o dataset de: {INPUT_PATH}")
try:
    df = pd.read_csv(INPUT_PATH)
    print(f"Sucesso. {len(df)} faixas carregadas para a etapa final de engenharia.")
except FileNotFoundError:
    print(f"ERRO CRÍTICO: O ficheiro '{INPUT_PATH}' não foi encontrado.")
    print("Por favor, execute o script 'processar_musicas.py' primeiro.")
    sys.exit()

# --- 3. ENGENHARIA DA 'CAMELOT_KEY' ---

def encontrar_camelot_key(key_estimada):
    """
    Usa o dicionário CAMELOT_MAP para encontrar o código Camelot
    para uma tonalidade estimada.
    """
    # Precisamos tratar o caso de "Tom" e "Tom major" (assumindo major se não especificado)
    if not isinstance(key_estimada, str):
        return None
        
    key_completa = key_estimada
    if ' ' not in key_estimada:
        # Se o modo (major/minor) não foi estimado, não podemos determinar A ou B.
        # Por enquanto, vamos retornar None. Poderíamos ter lógicas mais complexas aqui.
        # Mas o nosso algoritmo de K-K deve sempre retornar major/minor.
        # Esta é uma salvaguarda.
        return None

    return CAMELOT_MAP.get(key_completa)

print("\nIniciando a criação do atributo 'camelot_key'...")

# Aplica a função para criar a nova coluna
df['camelot_key'] = df['key_estimada'].apply(encontrar_camelot_key)

# Verifica se alguma música ficou sem a chave Camelot e a remove
# (Isso só aconteceria se o nosso algoritmo retornasse uma tonalidade não padrão)
linhas_sem_camelot = df['camelot_key'].isnull().sum()
if linhas_sem_camelot > 0:
    print(f"AVISO: {linhas_sem_camelot} faixas não puderam ser mapeadas para uma chave Camelot e foram removidas.")
    df.dropna(subset=['camelot_key'], inplace=True)

print("Atributo 'camelot_key' criado com sucesso!")

# --- 4. RESULTADO FINAL ---
print("\n--- Tabela Final, Pronta para o Algoritmo de Ordenação ---")
# Mostra as colunas mais importantes
print(df[['artista', 'nome_da_musica', 'bpm', 'key_estimada', 'camelot_key']].head(10))

# Salva o dataset final, pronto para ser ordenado
df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8')
print(f"\nDataset final com {len(df)} faixas pronto para ordenação, salvo em: {OUTPUT_PATH}")

print("\nTODOS OS DADOS ESTÃO PRONTOS! BEM-VINDO AO MÓDULO FINAL: A LÓGICA DO DJ!")