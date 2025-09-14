from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

coordenadas_recentes = []

@app.route('/nova-coordenada', methods=['POST'])
def nova_coordenada():
    global coordenadas_recentes
    
    if not request.json or 'latitude' not in request.json or 'longitude' not in request.json:
        return jsonify({"erro": "Requisição inválida."}), 400

    latitude = request.json.get('latitude')
    longitude = request.json.get('longitude')
    
    coordenadas_recentes.append({
        'lat': latitude,
        'lon': longitude,
        'timestamp': datetime.now()
    })
    
    print(f"Nova coordenada recebida: ({latitude}, {longitude})")
    
    return jsonify({"mensagem": "Coordenada recebida com sucesso!"}), 200

# Endpoint para o Streamlit buscar as coordenadas, agora com o tempo de vida
@app.route('/coordenadas-recentes', methods=['GET'])
def get_coordenadas_recentes():
    global coordenadas_recentes
    
    # Define o tempo de vida máximo do ponto (em segundos)
    TEMPO_MAXIMO_PONTO = 2.0
    
    limite_de_tempo = datetime.now() - timedelta(seconds=TEMPO_MAXIMO_PONTO)
    
    # Remove os pontos antigos da lista
    coordenadas_recentes = [ponto for ponto in coordenadas_recentes if ponto['timestamp'] > limite_de_tempo]
    
    # Calcula a "idade" de cada ponto para enviar ao painel
    pontos_para_exibir = []
    for p in coordenadas_recentes:
        idade_segundos = (datetime.now() - p['timestamp']).total_seconds()
        
        pontos_para_exibir.append({
            'lat': p['lat'], 
            'lon': p['lon'],
            'idade': idade_segundos
        })
    
    return jsonify(pontos_para_exibir), 200

if __name__ == '__main__':
    app.run(debug=True)