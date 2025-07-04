import os
import sys
import spotipy
import pandas as pd
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# --- 1. CONFIGURAÇÃO E VERIFICAÇÃO ---
load_dotenv()
print("Configurações carregadas...")
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
playlist_id = os.getenv('PLAYLIST_ID')
if not all([client_id, client_secret, redirect_uri, playlist_id]):
    print("ERRO CRÍTICO: Verifique as variáveis de ambiente.")
    sys.exit()

# --- 2. AUTENTICAÇÃO ---
# Usaremos um scope vazio, pois a playlist é pública.
scope = "" 
print("A conectar ao Spotify com acesso a dados públicos...")
try:
    auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    print("Conexão com o Spotify bem-sucedida!")
except Exception as e:
    print(f"Erro na autenticação: {e}")
    sys.exit()

# --- 3. EXTRAÇÃO DAS MÚSICAS DA PLAYLIST E SALVAMENTO ---
print(f"A buscar músicas da Playlist ID: {playlist_id}")
try:
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    tracks_data = []
    for item in tracks:
        track = item.get('track')
        if track and not track.get('is_local'):
            tracks_data.append({
                'track_id': track['id'],
                'artista': ", ".join([artist['name'] for artist in track['artists']]),
                'nome_da_musica': track['name']
            })
    
    df_playlist = pd.DataFrame(tracks_data)
    print(f"Total de {len(df_playlist)} músicas válidas carregadas da playlist.")

    # Salvando nosso progresso em um ficheiro CSV
    output_path = 'playlist_tracklist.csv'
    df_playlist.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\nTracklist salvo com sucesso em: {output_path}")

except Exception as e:
    print(f"Erro ao buscar as músicas ou salvar o ficheiro: {e}")
    sys.exit()

print("\nProcesso concluído. A busca de atributos do Spotify foi ignorada devido à depreciação do endpoint.")
print("Próximo passo: Usar o ficheiro 'playlist_tracklist.csv' com a API do AcousticBrainz.")