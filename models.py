from app import db, ma

class Movimentacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo: db.Column(db.Text)
    data: db.Column(db.String(8))
    conteudo: db.Column(db.Text)
    url: db.Column(db.Text)

    processo_id = db.Column(db.Integer, db.ForeignKey('processo.id'), nullable=False)
    processo = db.relationship('Processo',
            backref=db.backref('movimentacoes', lazy=True))

class MovimentacaoSchema(ma.Schema):
    class Meta:
        fields = ('titulo', 'data', 'conteudo', 'url')

class Representante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo: db.Column(db.Text)
    nome: db.Column(db.Text)

    parte_id = db.Column(db.Integer, db.ForeignKey('parte.id'), nullable=False)
    parte = db.relationship('Parte',
            backref=db.backref('representacao', lazy=True))

class RepresentanteSchema(ma.Schema):
    class Meta:
        fields = ('tipo', 'nome', 'parte_id')

class Parte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo: db.Column(db.Text)
    nome: db.Column(db.Text)

    processo_id = db.Column(db.Integer, db.ForeignKey('processo.id'), nullable=False)
    processo = db.relationship('Processo',
            backref=db.backref('partes', lazy=True))

class ParteSchema(ma.Schema):
    class Meta:
        fields = ('tipo', 'nome', 'processo_id')

class Processo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_unico: db.Column(db.String(50), unique=True)
    classe: db.Column(db.Text)
    area: db.Column(db.Text)
    assunto: db.Column(db.Text)
    distribuicao: db.Column(db.Text)
    juiz: db.Column(db.Text)
    valor: db.Column(db.Float)

class ProcessoSchema(ma.Schema):
    class Meta:
        fields = ('numero_unico',
                  'classe',
                  'area',
                  'assunto',
                  'distribuicao',
                  'juiz',
                  'valor')
