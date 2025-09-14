import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(layout="wide")
st.title('Mapa de Pontos que Piscam')

map_placeholder = st.empty()

# Define a localização central do mapa, por exemplo, São Paulo
# Isso evita que o mapa se mova para longe quando a lista de pontos estiver vazia
centro_do_mapa = pd.DataFrame([
    {'lat': -23.5505, 'lon': -46.6333}
])

# Loop infinito de polling
while True:
    try:
        response = requests.get("http://127.0.0.1:5000/coordenada-atual")
        
        if response.status_code == 200:
            coordenadas = response.json()
            
            with map_placeholder.container():
                if coordenadas:
                    # Se há coordenadas, exibe o ponto
                    df_pontos = pd.DataFrame(coordenadas)
                    # O mapa mostrará apenas os pontos do DataFrame
                    st.map(df_pontos, zoom=12) 
                    st.success(f"Ponto recebido em ({df_pontos.iloc[0]['lat']:.4f}, {df_pontos.iloc[0]['lon']:.4f})")
                else:
                    # Se não há coordenadas, exibe o mapa no centro sem pontos
                    st.map(centro_do_mapa, zoom=12)
                    st.info("Aguardando novas requisições...")
        else:
            with map_placeholder.container():
                st.error(f"Erro ao buscar coordenadas: {response.status_code}")
                
    except requests.exceptions.RequestException as e:
        with map_placeholder.container():
            st.error(f"Não foi possível conectar ao servidor: {e}")
            
    # Intervalo de tempo entre as requisições
    time.sleep(0.5) # Polling a cada meio segundo para uma atualização rápida