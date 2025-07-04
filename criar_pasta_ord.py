import pandas as pd
import os
import shutil # Biblioteca para operações de ficheiros de alto nível, como copiar
import sys

# --- 1. CONFIGURAÇÃO ---
# O ficheiro que contém a ordem do nosso set
ORDERED_CSV_PATH = 'dj_set_final_ordenado.csv'

# A pasta onde estão os ficheiros de áudio originais
SOURCE_AUDIO_FOLDER = 'musicas_flac/'

# O nome da nova pasta que vamos criar para o set final
FINAL_SET_FOLDER = 'DJ_Set_Final_Ordenado'

# --- 2. CARREGAR A PLAYLIST ORDENADA ---
print(f"A carregar a ordem do set do ficheiro: {ORDERED_CSV_PATH}")
try:
    df_ordered = pd.read_csv(ORDERED_CSV_PATH)
except FileNotFoundError:
    print(f"ERRO: O ficheiro ordenado '{ORDERED_CSV_PATH}' não foi encontrado.")
    print("Por favor, execute o script 'ordenar_set.py' primeiro.")
    sys.exit()

# --- 3. CRIAR A PASTA DE DESTINO ---
if not os.path.exists(FINAL_SET_FOLDER):
    os.makedirs(FINAL_SET_FOLDER)
    print(f"Pasta de destino '{FINAL_SET_FOLDER}' criada com sucesso.")
else:
    print(f"Pasta de destino '{FINAL_SET_FOLDER}' já existe. Os ficheiros serão adicionados ou sobrescritos.")
    
# --- 4. COPIAR E RENOMEAR OS FICHEIROS NA ORDEM CORRETA ---
print("\nIniciando a criação da pasta do DJ set final...")

total_musicas = len(df_ordered)
# Calcula o número de dígitos necessários para o prefixo (ex: 109 músicas -> 3 dígitos)
num_digits = len(str(total_musicas))

for index, row in df_ordered.iterrows():
    ordem = index + 1
    nome_original = row['filename']
    
    # Caminho do ficheiro de origem
    caminho_origem = os.path.join(SOURCE_AUDIO_FOLDER, nome_original)
    
    # Cria o novo nome do ficheiro com o prefixo numérico
    # str(ordem).zfill(num_digits) garante os zeros à esquerda (ex: 1 -> "001")
    novo_nome = f"{str(ordem).zfill(num_digits)} - {nome_original}"
    caminho_destino = os.path.join(FINAL_SET_FOLDER, novo_nome)
    
    # Verifica se o ficheiro original existe antes de copiar
    if os.path.exists(caminho_origem):
        print(f"Copiando [{ordem}/{total_musicas}]: {novo_nome}")
        shutil.copy(caminho_origem, caminho_destino)
    else:
        print(f"AVISO: Ficheiro de origem não encontrado e ignorado: {nome_original}")

print("\n--- PROCESSO CONCLUÍDO! ---")
print(f"A sua pasta '{FINAL_SET_FOLDER}' está pronta!")
print("Pode agora importar esta pasta para o Rekordbox ou o seu software de DJ preferido, e as músicas estarão na ordem exata do seu set.")