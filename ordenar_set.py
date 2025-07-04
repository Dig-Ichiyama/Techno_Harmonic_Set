import pandas as pd
import sys

# --- 1. CONFIGURAÇÃO ---
INPUT_PATH = 'playlist_pronta_para_ordenar.csv'
OUTPUT_PATH = 'dj_set_final_ordenado.csv'

# --- 2. CARREGAR O DATASET FINAL ---
print(f"A carregar o dataset final de: {INPUT_PATH}")
try:
    df = pd.read_csv(INPUT_PATH)
    # Converte o DataFrame para uma lista de dicionários para facilitar a manipulação
    musicas_disponiveis = df.to_dict('records')
    print(f"Sucesso. {len(musicas_disponiveis)} faixas prontas para serem ordenadas.")
except FileNotFoundError:
    print(f"ERRO CRÍTICO: O ficheiro '{INPUT_PATH}' não foi encontrado.")
    sys.exit()

# --- 3. FUNÇÕES AUXILIARES PARA A LÓGICA DO DJ ---

def extrair_camelot(camelot_key):
    """Extrai o número e a letra de uma chave Camelot (ex: '8A' -> (8, 'A'))."""
    numero = int(camelot_key[:-1])
    letra = camelot_key[-1]
    return numero, letra

def calcular_pontuacao_harmonica(key_atual, key_candidata):
    """Calcula a pontuação de compatibilidade harmônica baseada nas nossas regras."""
    num_atual, letra_atual = extrair_camelot(key_atual)
    num_cand, letra_cand = extrair_camelot(key_candidata)

    # Regra de Prioridade Máxima (3 pontos): Mesma letra, número vizinho
    if letra_atual == letra_cand and abs(num_atual - num_cand) == 1:
        return 3
    # Tratamento especial para a transição 12 -> 1
    if letra_atual == letra_cand and sorted([num_atual, num_cand]) == [1, 12]:
        return 3

    # Regra de Prioridade Média (2 pontos): Mesmo número, letra diferente
    if num_atual == num_cand and letra_atual != letra_cand:
        return 2

    # Regra de Prioridade Baixa (1 ponto): Diagonal, número vizinho
    if letra_atual != letra_cand and abs(num_atual - num_cand) == 1:
        return 1
    # Tratamento especial da diagonal 12 -> 1
    if letra_atual != letra_cand and sorted([num_atual, num_cand]) == [1, 12]:
        return 1
        
    # Se não for compatível
    return 0

# --- 4. O ALGORITMO DE ORDENAÇÃO PRINCIPAL ---
print("\n--- Iniciando o algoritmo de ordenação do DJ Set ---")

playlist_ordenada = []

# REGRA 1: Ponto de Partida -> Menor BPM
musica_atual = min(musicas_disponiveis, key=lambda x: x['bpm'])
playlist_ordenada.append(musica_atual)
musicas_disponiveis.remove(musica_atual)

print(f"Música de Partida: {musica_atual['artista']} - {musica_atual['nome_da_musica']} ({musica_atual['bpm']} BPM, {musica_atual['camelot_key']})")

# Loop principal para ordenar o resto do set
while musicas_disponiveis:
    candidatas_pontuadas = []
    
    # REGRA 2: Filtro Rígido de BPM
    bpm_atual = musica_atual['bpm']
    bpm_maximo = bpm_atual * 1.075 # Limite de 7.5% de aumento

    candidatas_bpm_ok = [m for m in musicas_disponiveis if m['bpm'] >= bpm_atual and m['bpm'] <= bpm_maximo]

    # REGRA 3: Sistema de Pontuação Harmônica
    if candidatas_bpm_ok:
        for candidata in candidatas_bpm_ok:
            pontuacao = calcular_pontuacao_harmonica(musica_atual['camelot_key'], candidata['camelot_key'])
            if pontuacao > 0:
                # Adiciona um critério de desempate: menor aumento de BPM é melhor
                desempate = 1 - ((candidata['bpm'] - bpm_atual) / (bpm_maximo - bpm_atual + 0.01))
                pontuacao_final = pontuacao + desempate
                candidatas_pontuadas.append((pontuacao_final, candidata))
    
    # Escolhe a melhor candidata
    if candidatas_pontuadas:
        # Ordena pela maior pontuação e escolhe a melhor
        candidatas_pontuadas.sort(key=lambda x: x[0], reverse=True)
        melhor_proxima_musica = candidatas_pontuadas[0][1]
    else:
        # REGRA 4: Plano de Contingência (Fallback)
        # Nenhuma música compatível encontrada, "reseta" pegando a de menor BPM restante
        print("AVISO: Nenhuma candidata compatível encontrada. Resetando com o menor BPM...")
        melhor_proxima_musica = min(musicas_disponiveis, key=lambda x: x['bpm'])

    # Adiciona a música escolhida à playlist e a remove das disponíveis
    musica_atual = melhor_proxima_musica
    playlist_ordenada.append(musica_atual)
    musicas_disponiveis.remove(musica_atual)
    
    print(f" -> Próxima: {musica_atual['artista']} - {musica_atual['nome_da_musica']} ({musica_atual['bpm']} BPM, {musica_atual['camelot_key']})")

# --- 5. RESULTADO FINAL ---
print("\n--- DJ SET FINAL ORDENADO ---")
df_final_ordenado = pd.DataFrame(playlist_ordenada)

# Mostra a ordem final
for index, row in df_final_ordenado.iterrows():
    print(f"{index+1:02d}. {row['artista']} - {row['nome_da_musica']} ({row['bpm']:.0f} BPM, {row['camelot_key']})")

# Salva o resultado final
df_final_ordenado.to_csv(OUTPUT_PATH, index=False, encoding='utf-8')
print(f"\nDJ Set com {len(df_final_ordenado)} músicas salvo com sucesso em: {OUTPUT_PATH}")
print("\nPROJETO CONCLUÍDO! PARABÉNS!")