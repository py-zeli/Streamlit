from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Lista para armazenar temporariamente as coordenadas recentes
# A cada nova requisição, a lista é limpa de pontos antigos
coordenadas_recentes = []

# Endpoint para receber a nova coordenada (POST)
@app.route('/nova-coordenada', methods=['POST'])
def nova_coordenada():
    global coordenadas_recentes
    
    if not request.json or 'latitude' not in request.json or 'longitude' not in request.json:
        return jsonify({"erro": "Requisição inválida."}), 400

    latitude = request.json.get('latitude')
    longitude = request.json.get('longitude')
    
    # Adiciona a nova coordenada com o timestamp atual na lista
    coordenadas_recentes.append({
        'lat': latitude,
        'lon': longitude,
        'timestamp': datetime.now()
    })
    
    print(f"Nova coordenada recebida: ({latitude}, {longitude})")
    
    return jsonify({"mensagem": "Coordenada recebida com sucesso!"}), 200

# Endpoint para o Streamlit buscar as coordenadas recentes (GET)
@app.route('/coordenadas-recentes', methods=['GET'])
def get_coordenadas_recentes():
    global coordenadas_recentes
    
    # Define o limite de tempo (2 segundos atrás)
    limite_de_tempo = datetime.now() - timedelta(seconds=2)
    
    # Filtra a lista, removendo os pontos que são mais antigos que o limite de tempo
    coordenadas_recentes = [ponto for ponto in coordenadas_recentes if ponto['timestamp'] > limite_de_tempo]
    
    # Extrai apenas as coordenadas (lat e lon) para enviar ao Streamlit
    pontos_para_exibir = [{'lat': p['lat'], 'lon': p['lon']} for p in coordenadas_recentes]
    
    return jsonify(pontos_para_exibir), 200

if __name__ == '__main__':
    app.run(debug=True)