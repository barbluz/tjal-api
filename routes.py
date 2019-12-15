from app import app
from flask import jsonify
import os
from models import *
from app import *
from scrapper_tjal import busca_processo

processo_schema = ProcessoSchema()

@app.route('/processo/<numero>', methods=['GET'])
def get_processo(numero):
    # processo = Processo.query.filter_by(numero_unico = numero).first()
    processo = busca_processo("07175619820198020001")
    print(processo)

    #TODO verify if it has reached expiration date; if so, fetch process again
    # try: processo = get_processo(numero)
    # if processo === null
    #

    return processo_schema.jsonify(processo)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
