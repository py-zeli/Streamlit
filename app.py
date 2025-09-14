from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Variável global para armazenar a última coordenada recebida e o seu timestamp
ponto_atual = None

# Endpoint para receber a nova coordenada (POST)
@app.route('/nova-coordenada', methods=['POST'])
def nova_coordenada():
    global ponto_atual
    
    if not request.json or 'latitude' not in request.json or 'longitude' not in request.json:
        return jsonify({"erro": "Requisição inválida."}), 400

    latitude = request.json.get('latitude')
    longitude = request.json.get('longitude')
    
    # Armazena a nova coordenada e o timestamp atual
    ponto_atual = {
        'lat': latitude,
        'lon': longitude,
        'timestamp': datetime.now()
    }
    
    print(f"Nova coordenada recebida: ({latitude}, {longitude})")
    
    return jsonify({"mensagem": "Coordenada recebida com sucesso!"}), 200

# Endpoint para o Streamlit buscar a coordenada atual (GET)
@app.route('/coordenada-atual', methods=['GET'])
def get_coordenada_atual():
    global ponto_atual
    
    # Verifica se existe uma coordenada e se ela é "recente" (recebida nos últimos 2 segundos)
    if ponto_atual and datetime.now() - ponto_atual['timestamp'] < timedelta(seconds=2):
        # Se for recente, retorna a coordenada
        return jsonify([{'lat': ponto_atual['lat'], 'lon': ponto_atual['lon']}]), 200
    else:
        # Se não houver coordenada ou se ela for antiga, retorna uma lista vazia
        return jsonify([]), 200

if __name__ == '__main__':
    app.run(debug=True)