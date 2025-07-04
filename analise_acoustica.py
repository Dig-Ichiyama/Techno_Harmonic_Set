import pandas as pd
import sys
import time
import musicbrainzngs
import requests # <-- NOSSA NOVA BIBLIOTECA PARA PEDIDOS WEB

# --- 1. CONFIGURAÇÃO ---
input_path = 'playlist_tracklist.csv'
musicbrainzngs.set_useragent(
    "TechnoSetHarmonizado", "1.0", "seu.email@exemplo.com"
)

# --- 2. CARREGAR OS DADOS DA NOSSA PLAYLIST ---
print(f"A carregar a nossa lista de músicas do ficheiro: {input_path}")
try:
    df = pd.read_csv(input_path)
    print("Ficheiro carregado com sucesso!")
except FileNotFoundError:
    print(f"ERRO CRÍTICO: O ficheiro '{input_path}' não foi encontrado.")
    sys.exit()

# --- 3. FUNÇÕES DE BUSCA NAS APIS ---

def get_mbid(row):
    """Busca o MBID para uma faixa."""
    # (A nossa função anterior para o MusicBrainz)
    print(f"Buscando MBID para: {row['artista']} - {row['nome_da_musica']}")
    try:
        result = musicbrainzngs.search_recordings(
            artist=row['artista'], recording=row['nome_da_musica'], limit=1)
        time.sleep(1)
        if result['recording-list']:
            return result['recording-list'][0]['id']
        return None
    except Exception:
        time.sleep(1)
        return None

def get_acoustic_features(mbid):
    """Busca os dados de BPM e Tom no AcousticBrainz usando um MBID."""
    if pd.isna(mbid):
        return None, None # Retorna nulo se o MBID for nulo

    print(f"Buscando dados no AcousticBrainz para o MBID: {mbid}")
    url = f"https://acousticbrainz.org/api/v1/{mbid}/low-level"
    
    try:
        response = requests.get(url)
        # Pausa para não sobrecarregar a API
        time.sleep(0.5)

        if response.status_code == 200:
            data = response.json()
            bpm = data.get('rhythm', {}).get('bpm')
            key = data.get('tonal', {}).get('key_key')
            scale = data.get('tonal', {}).get('key_scale')
            return bpm, f"{key} {scale}" # Retorna BPM e a Chave completa (ex: "C# minor")
        else:
            return None, None
            
    except Exception as e:
        print(f"Erro na chamada ao AcousticBrainz para {mbid}: {e}")
        return None, None

# --- 4. EXECUÇÃO DO PROCESSO DE ENRIQUECIMENTO ---

# Passo 1: Obter todos os MBIDs (removido o .head() para processar tudo)
print("\n--- Fase 1: Buscando todos os MusicBrainz IDs ---")
print("Isto pode demorar alguns minutos...")
df['mbid'] = df.apply(get_mbid, axis=1)

# Passo 2: Obter os dados do AcousticBrainz
print("\n--- Fase 2: Buscando dados no AcousticBrainz ---")
# Criamos uma lista de tuplos com os resultados (bpm, key)
acoustic_data = [get_acoustic_features(mbid) for mbid in df['mbid']]

# Adicionamos os resultados como novas colunas no DataFrame
df['bpm'] = [item[0] for item in acoustic_data]
df['key_acousticbrainz'] = [item[1] for item in acoustic_data]


# --- 5. RESULTADO FINAL ---
print("\n--- Tabela Final Totalmente Enriquecida ---")
# Mostra as colunas mais importantes
print(df[['artista', 'nome_da_musica', 'mbid', 'bpm', 'key_acousticbrainz']].head(10))

# Salva o resultado final num novo CSV
final_output_path = 'playlist_com_dados_acusticos.csv'
df.to_csv(final_output_path, index=False, encoding='utf-8')
print(f"\nDados finais salvos com sucesso em: {final_output_path}")

print("\nPRÓXIMO PASSO: Módulo 3 - Engenharia de Atributos (Chave de Camelot)!")