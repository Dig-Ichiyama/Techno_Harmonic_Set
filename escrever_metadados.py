import pandas as pd
import os
import sys
from mutagen.flac import FLAC

# --- 1. CONFIGURAÇÃO ---
# O ficheiro CSV que contém a nossa playlist final e os dados
ORDERED_CSV_PATH = 'dj_set_final_ordenado.csv'

# A pasta com os ficheiros numerados que vamos modificar
SET_FOLDER_PATH = 'DJ_Set_Final_Ordenado/'

# --- 2. CARREGAR OS DADOS FINAIS ---
print(f"A carregar o set ordenado de: {ORDERED_CSV_PATH}")
try:
    df_set = pd.read_csv(ORDERED_CSV_PATH)
except FileNotFoundError:
    print(f"ERRO: O ficheiro ordenado '{ORDERED_CSV_PATH}' não foi encontrado.")
    print("Por favor, execute o script 'ordenar_set.py' e 'criar_pasta_set.py' primeiro.")
    sys.exit()

# --- 3. ESCREVER OS METADADOS NOS FICHEIROS DE ÁUDIO ---
print("\nIniciando o processo de escrita de metadados nos ficheiros de áudio...")

total_musicas = len(df_set)
num_digits = len(str(total_musicas))

for index, row in df_set.iterrows():
    ordem = index + 1
    
    # Recria o nome do ficheiro numerado, como fizemos no script anterior
    nome_ficheiro_original = row['filename']
    nome_ficheiro_numerado = f"{str(ordem).zfill(num_digits)} - {nome_ficheiro_original}"
    
    caminho_completo = os.path.join(SET_FOLDER_PATH, nome_ficheiro_numerado)
    
    # Extrai os dados que vamos escrever
    bpm = str(round(row['bpm'])) # Converte para string
    camelot_key = row['camelot_key']
    
    # Verifica se o ficheiro existe antes de tentar modificá-lo
    if os.path.exists(caminho_completo):
        try:
            # Abre o ficheiro FLAC com o mutagen
            audio = FLAC(caminho_completo)
            
            # Apaga tags antigas para evitar duplicados
            if 'BPM' in audio:
                del audio['BPM']
            if 'INITIALKEY' in audio:
                del audio['INITIALKEY']
            
            # Escreve as novas tags (metadados)
            audio['BPM'] = bpm
            audio['INITIALKEY'] = camelot_key
            audio['COMMENT'] = f"Analisado e ordenado pelo projeto TechnoSetHarmonizado. Posição no set: {ordem}"
            
            # Salva as alterações no ficheiro
            audio.save()
            
            print(f"[{ordem}/{total_musicas}] Metadados escritos com sucesso para: {nome_ficheiro_numerado} (BPM: {bpm}, Key: {camelot_key})")

        except Exception as e:
            print(f"ERRO ao processar o ficheiro {nome_ficheiro_numerado}: {e}")
    else:
        print(f"AVISO: Ficheiro não encontrado, ignorado: {nome_ficheiro_numerado}")

print("\n--- PROCESSO DE METADADOS CONCLUÍDO! ---")
print("As suas faixas de áudio na pasta 'DJ_Set_Final_Ordenado' agora contêm os dados de BPM e Tom.")