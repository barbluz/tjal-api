from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
CORS(app)

from models import ProcessoSchema, ParteSchema, MovimentacaoSchema, RepresentanteSchema, Processo
from scraper_tjal import busca_processo, get_dados_processo, get_movimentacoes, get_partes

processo_schema = ProcessoSchema()
partes_schema = ParteSchema(many=True)
parte_schema = ParteSchema()
representante_schema = RepresentanteSchema()
movimentacao_schema = MovimentacaoSchema()
movimentacoes_schema = MovimentacaoSchema(many=True)


@app.route('/processo/<numero>', methods=['GET'])
def get_processo(numero):
    selector = busca_processo(numero)

    processo = Processo.query.filter_by(numero_unico=numero).first()
    if processo is None:
        processo = get_dados_processo(selector, numero)
        processo.partes, processo.representantes = get_partes(selector, processo, "create")
        processo.movimentacoes = get_movimentacoes(selector, processo, "create")

        db.session.add(processo)
        db.session.commit()
    else:
        processo.classe = get_dados_processo(selector, numero).classe
        processo.area = get_dados_processo(selector, numero).area
        processo.assunto = get_dados_processo(selector, numero).assunto
        processo.distribuicao = get_dados_processo(selector, numero).distribuicao
        processo.juiz = get_dados_processo(selector, numero).juiz
        processo.valor = get_dados_processo(selector, numero).valor

        processo.partes, processo.representantes = get_partes(selector, processo, "update")
        processo.movimentacoes = get_movimentacoes(selector, processo, "update")

        db.session.commit()

    return processo_schema.jsonify(processo)
