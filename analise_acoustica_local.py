import os
import sys
import pandas as pd
import librosa
import numpy as np

# --- 1. CONFIGURAÇÃO ---
AUDIO_FOLDER_PATH = 'musicas_flac/'
FINAL_OUTPUT_PATH = 'dataset_final_analisado.csv'

# --- 2. PERFIS DE TONALIDADE (Krumhansl-Kessler) ---
# Baseado na pesquisa fundamental da área, como mencionado no seu documento.
# Valores para as tonalidades raíz (C Major e C minor).
krumhansl_key_profiles = {
    'major': np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]),
    'minor': np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.78, 3.98, 2.69, 3.34, 3.17])
}

# Nomes das 12 notas musicais (classes de altura)
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Gerar todos os 24 perfis de tonalidade (12 maiores, 12 menores) através do deslocamento circular
# Exatamente como descrito na referência [2] e [37] do seu documento.
all_profiles = {}
for i in range(12):
    all_profiles[f'{notes[i]} major'] = np.roll(krumhansl_key_profiles['major'], i)
    all_profiles[f'{notes[i]} minor'] = np.roll(krumhansl_key_profiles['minor'], i)


# --- 3. FUNÇÕES DE ANÁLISE DE ÁUDIO ---

def estimar_tonalidade_completa(chroma_vector):
    """
    Compara o vetor de croma de uma música com os 24 perfis de tonalidade
    e retorna aquele com a maior correlação (produto escalar).
    """
    best_match = None
    max_corr = -1
    
    # Normaliza o vetor de croma da música para a comparação
    chroma_vector_norm = chroma_vector / np.linalg.norm(chroma_vector)
    
    for key_name, profile in all_profiles.items():
        # Normaliza o perfil de tonalidade do gabarito
        profile_norm = profile / np.linalg.norm(profile)
        # Calcula a correlação (produto escalar)
        correlation = np.dot(chroma_vector_norm, profile_norm)
        
        if correlation > max_corr:
            max_corr = correlation
            best_match = key_name
            
    return best_match

def analisar_faixa_local(filepath):
    """
    Analisa um ficheiro de áudio local para extrair BPM e a Tonalidade completa.
    """
    try:
        y, sr = librosa.load(filepath, sr=None)
        
        # 1. Estimar o BPM
        tempo_array, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = round(tempo_array[0]) if tempo_array.size > 0 else None

        # 2. Estimar a Tonalidade e Escala
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)
        
        # Usa a nossa nova função para obter a tonalidade completa
        key_full = estimar_tonalidade_completa(chroma_mean)
        
        print(f"  -> Análise OK: BPM={bpm}, Tonalidade={key_full}")
        return bpm, key_full

    except Exception as e:
        print(f"  -> !! Erro ao analisar o ficheiro: {e}")
        return None, None

# --- 4. PROCESSAMENTO PRINCIPAL ---
print(f"--- Iniciando a análise dos ficheiros na pasta '{AUDIO_FOLDER_PATH}' ---")
if not os.path.isdir(AUDIO_FOLDER_PATH):
    print(f"ERRO: A pasta '{AUDIO_FOLDER_PATH}' não foi encontrada.")
    sys.exit()

audio_files = [f for f in os.listdir(AUDIO_FOLDER_PATH) if f.endswith('.flac')]
if not audio_files:
    print(f"AVISO: Nenhum ficheiro .flac encontrado na pasta '{AUDIO_FOLDER_PATH}'.")
    sys.exit()

print(f"Encontrados {len(audio_files)} ficheiros de áudio para processar.")
all_tracks_data = []

for filename in audio_files:
    print(f"\nProcessando: {filename}")
    filename_no_ext = os.path.splitext(filename)[0]
    try:
        artista, nome_da_musica = filename_no_ext.split(' - ', 1)
    except ValueError:
        artista = "Desconhecido"
        nome_da_musica = filename_no_ext
        
    filepath = os.path.join(AUDIO_FOLDER_PATH, filename)
    bpm, key = analisar_faixa_local(filepath)
    
    all_tracks_data.append({
        'artista': artista.strip(),
        'nome_da_musica': nome_da_musica.strip(),
        'bpm': bpm,
        'key_estimada': key,
        'filename': filename
    })

# --- 5. RESULTADO FINAL ---
print("\n--- Análise concluída. Criando o DataFrame final. ---")
df_final = pd.DataFrame(all_tracks_data)
df_final.dropna(subset=['bpm', 'key_estimada'], inplace=True)

print("\n--- Amostra do Dataset Final Analisado ---")
print(df_final[['artista', 'nome_da_musica', 'bpm', 'key_estimada']].head())

df_final.to_csv(FINAL_OUTPUT_PATH, index=False, encoding='utf-8')
print(f"\nDataset final com {len(df_final)} faixas analisadas salvo com sucesso em: {FINAL_OUTPUT_PATH}")

print("\nBASE DE DADOS COMPLETA E PRONTA PARA A ENGENHARIA DE ATRIBUTOS (CAMELOT)!")