from peewee import *

db = MySQLDatabase(
        host='localhost',
        user='root',
        password='raquel',
        database='tjal'
        )

class Processo(Model):
    numero_unico = PrimaryKeyField()
    class Meta:
        database = db

class Movimentacao(Model):
    data = CharField()
    titulo = TextField()
    conteudo = TextField(null = True)
    url = TextField(null = True)
    processo = ForeignKeyField(Processo, backref='movimentacao')

    class Meta:
        database = db

class Parte(Model):
    class Meta:
        database = db

db.connect()
db.create_tables([Movimentacao, Processo, Parte])
