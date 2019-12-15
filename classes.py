from dataclasses import dataclass
from typing import List

class Movimentacao(db.Model):
    titulo: str
    data: str
    conteudo: str
    url: str

    def __init__(self, titulo: str, data: str = None, conteudo: str = None, url: str = None):
        self.titulo = titulo
        self.data = data
        self.conteudo = conteudo
        self.url = url

class MovimentacaoSchema(ma.Schema):
    class Meta:
        fields = ('titulo', 'data', 'conteudo', 'url')

class Representante:
    tipo: str
    nome: str

    def __init__(self, tipo: str, nome: str):
        self.tipo = tipo
        self.nome = nome

@dataclass
class parte:
    tipo: str   # demandante/demandado
    nome: str
    representacao: List[representante]

    def __init__(self, tipo: str, nome: str, representacao: List[representante] = None):
        self.tipo = tipo
        self.nome = nome
        self.representacao = representacao

@dataclass
class processo:
    # numero_unico: str
    # classe: str
    # area: str
    # assunto: str
    # distribuicao: str
    # juiz: str
    # valor: float
    partes: List[parte]
    movimentacoes: List[movimentacao]

    def __init__(self, representacao: List[representante] = None, movimentacoes: List[movimentacao] = None):
        self.representacao = representacao
        self.movimentacoes = movimentacao

