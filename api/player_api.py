# api/player_api.py
import os
from flask import Flask, jsonify, request, make_response
import requests

app = Flask(__name__)

# As variáveis são carregadas do painel da Vercel
VALID_USERNAME = os.environ.get('VALID_USERNAME')
VALID_PASSWORD = os.environ.get('VALID_PASSWORD')
M3U_URL = os.environ.get('M3U_URL')


@app.route('/api/player_api', methods=['GET'])
def iptv_api_handler():
    # 1. Obtém as credenciais da URL
    username = request.args.get('username')
    password = request.args.get('password')

    # 2. Validação de segurança
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        try:
            # 3. Busca a lista M3U original
            response = requests.get(M3U_URL, timeout=10)
            response.raise_for_status()

            # 4. Devolve a lista M3U com o formato correto
            resp = make_response(response.text)
            resp.headers['Content-Type'] = 'application/vnd.apple.mpegurl'
            return resp

        except requests.exceptions.RequestException as e:
            # Erro na lista M3U original
            return jsonify({"error": "Erro ao carregar a lista de mídia original."}), 500
    else:
        # Credenciais erradas
        return jsonify({"error": "Acesso Negado. Credenciais inválidas."}), 401
