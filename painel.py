import streamlit as st
import pandas as pd
import requests
import time
import pydeck as pdk

st.set_page_config(layout="wide")
st.title('Visualização em Tempo Real de Transações Pix')

map_placeholder = st.empty()

# Define a view fixa do mapa, centralizada no Brasil
view_state = pdk.ViewState(
    latitude=-15.7797,
    longitude=-47.9297,
    zoom=4,
    pitch=0
)

# Constante para o tempo de vida máximo dos pontos, deve ser o mesmo do app.py
TEMPO_MAXIMO_PONTO = 2.0

# Loop infinito de polling
while True:
    try:
        # Busca a lista de coordenadas recentes
        response = requests.get("http://127.0.0.1:5000/coordenadas-recentes")
        
        if response.status_code == 200:
            coordenadas = response.json()
            
            with map_placeholder.container():
                if coordenadas:
                    # Converte a lista para um DataFrame
                    df_pontos = pd.DataFrame(coordenadas)
                    
                    # Adiciona a coluna 'alpha' com a transparência calculada
                    # A fórmula (1 - idade/tempo_max) garante que o ponto fica mais transparente com a idade
                    df_pontos['alpha'] = df_pontos['idade'].apply(lambda idade: max(0, 255 * (1 - idade / TEMPO_MAXIMO_PONTO)))
                    
                    # Cria a camada de pontos
                    layer = pdk.Layer(
                        'ScatterplotLayer',
                        df_pontos,
                        get_position=['lon', 'lat'],
                        # Usa a nova coluna 'alpha' na cor
                        get_color='[255, 0, 0, alpha]', 
                        get_radius=5000
                    )

                    # Cria o mapa com a visão fixa e a camada
                    r = pdk.Deck(
                        layers=[layer],
                        initial_view_state=view_state
                    )
                    
                    st.pydeck_chart(r)
                    st.success(f"Número de pontos ativos: {len(coordenadas)}")
                else:
                    # Se não há coordenadas, exibe um mapa limpo
                    r = pdk.Deck(
                        initial_view_state=view_state
                    )
                    st.pydeck_chart(r)
                    st.info("Aguardando novas requisições...")

        else:
            with map_placeholder.container():
                st.error(f"Erro ao buscar coordenadas: {response.status_code}")
                
    except requests.exceptions.RequestException as e:
        with map_placeholder.container():
            st.error(f"Não foi possível conectar ao servidor: {e}")
            
    time.sleep(0.05) # Diminuí o polling para 50ms para um efeito mais suave