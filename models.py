from flask_marshmallow import fields

from app import db, ma


class Movimentacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.Text)
    data = db.Column(db.String(18))
    conteudo = db.Column(db.Text)
    url = db.Column(db.Text)

    processo_id = db.Column(db.Integer, db.ForeignKey('processo.id'), nullable=False)


class MovimentacaoSchema(ma.Schema):
    id = fields.fields.String()
    titulo = fields.fields.String()
    data = fields.fields.String()
    conteudo = fields.fields.String()
    url = fields.fields.String()


class Representante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Text)
    nome = db.Column(db.Text)

    parte_id = db.Column(db.Integer, db.ForeignKey('parte.id'))


class RepresentanteSchema(ma.Schema):
    id = fields.fields.String()
    tipo = fields.fields.String()
    nome = fields.fields.String()


class Parte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Text)
    nome = db.Column(db.Text)

    representantes = db.relationship('Representante', backref='parte')
    processo_id = db.Column(db.Integer, db.ForeignKey('processo.id'), nullable=False)


class ParteSchema(ma.Schema):
    id = fields.fields.String()
    tipo = fields.fields.String()
    nome = fields.fields.String()
    representantes = fields.fields.Nested(RepresentanteSchema(many=True))


class Processo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_unico = db.Column(db.String(50), unique=True)
    classe = db.Column(db.Text)
    area = db.Column(db.Text)
    assunto = db.Column(db.Text)
    distribuicao = db.Column(db.Text)
    juiz = db.Column(db.Text)
    valor = db.Column(db.Float)
    ultima_consulta = db.Column(db.DateTime)

    partes = db.relationship('Parte', backref='processo')
    movimentacoes = db.relationship('Movimentacao', backref='processo')

    def __init__(self, numero_unico, classe, area, assunto, distribuicao, juiz, valor):
        self.numero_unico = numero_unico
        self.classe = classe
        self.area = area
        self.assunto = assunto
        self.distribuicao = distribuicao
        self.juiz = juiz
        self.valor = valor


class ProcessoSchema(ma.Schema):
    numero_unico = fields.fields.String()
    classe = fields.fields.String()
    area = fields.fields.String()
    assunto = fields.fields.String()
    distribuicao = fields.fields.String()
    juiz = fields.fields.String()
    valor = fields.fields.String()
    ultima_consulta = fields.fields.DateTime()
    partes = fields.fields.Nested(ParteSchema(many=True))
    movimentacoes = fields.fields.Nested(MovimentacaoSchema(many=True))
