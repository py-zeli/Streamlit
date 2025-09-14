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

# Loop infinito de polling
while True:
    try:
        # Busca a lista de coordenadas recentes
        response = requests.get("http://127.0.0.1:5000/coordenadas-recentes")
        
        if response.status_code == 200:
            coordenadas = response.json()
            
            with map_placeholder.container():
                if coordenadas:
                    df_pontos = pd.DataFrame(coordenadas)
                    
                    # Cria a camada de pontos
                    layer = pdk.Layer(
                        'ScatterplotLayer',
                        df_pontos,
                        get_position=['lon', 'lat'],
                        get_color='[173, 216, 230, 1]', # Pontos vermelhos
                        get_radius=20000
                    )

                    # Cria o mapa com a visão fixa e a camada, mas sem estilo de mapa
                    r = pdk.Deck(
                        layers=[layer],
                        initial_view_state=view_state
                    )
                    
                    st.pydeck_chart(r)
                    st.success(f"Número de pontos ativos: {len(coordenadas)}")
                else:
                    # Se não há coordenadas, exibe um mapa limpo e sem a camada
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
            
    time.sleep(0.5)