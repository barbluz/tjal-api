import re
import requests
from parsel import Selector

from app import db
from models import Movimentacao, Processo, Parte, Representante

def get_movimentacoes(selector: Selector, processo: Processo, action: str):
    if action == 'update':
        movimentacoes = Movimentacao.query.filter_by(processo_id=processo.id).all()

        for tr in selector.xpath('//*[@id="tabelaTodasMovimentacoes"]/tr'):
            data = tr.xpath('./td[1]/text()').extract_first()

            titulo = tr.xpath('./td[3]//text()').extract_first()
            if titulo is not None:
                titulo = titulo.strip()

            url = tr.xpath('./td[3]//@href').extract_first()

            conteudo = tr.xpath('./td[3]/span/text()').extract_first()
            if conteudo is not None:
                conteudo = conteudo.strip()

        m = Movimentacao(titulo=titulo, data=data, conteudo=conteudo, url=url, processo=processo)
        if m not in movimentacoes:
            movimentacoes.append(m)
    else:
        movimentacoes = []
        for tr in selector.xpath('//*[@id="tabelaTodasMovimentacoes"]/tr'):
            data = tr.xpath('./td[1]/text()').extract_first()

            titulo = tr.xpath('./td[3]//text()').extract_first()
            if titulo is not None:
                titulo = titulo.strip()

            url = tr.xpath('./td[3]//@href').extract_first()

            conteudo = tr.xpath('./td[3]/span/text()').extract_first()
            if conteudo is not None:
                conteudo = conteudo.strip()

            m = Movimentacao(titulo=titulo, data=data, conteudo=conteudo, url=url, processo=processo)
            db.session.add(m)
            db.session.commit()

            movimentacoes.append(m)
    return movimentacoes


def get_dados_processo(selector: Selector, numero_unico: str):
    sel = selector.xpath('//*[@class="secaoFormBody" and @id=""]//tr[@class="" and td[1][text()]]')

    classe = sel.xpath(".//td[1][*[contains(text(), 'Classe:')]]/following-sibling::td//span/text()").extract_first()
    assunto = sel.xpath(".//td[1][*[contains(text(), 'Assunto:')]]/following-sibling::td//span/text()").extract_first()
    juiz = sel.xpath(".//td[1][*[contains(text(), 'Juiz:')]]/following-sibling::td//span/text()").extract_first()
    valor = sel.xpath(".//td[1][*[contains(text(), 'Valor da ação:')]]/following-sibling::td//span/text()").extract_first()
    area = sel.xpath(".//td[*[contains(text(), 'Área:')]]/text()[last()]").extract_first()
    distribuicao = sel.xpath(".//td[1][*[contains(text(), 'Distribuição:')]]/following-sibling::td//span/text()").extract_first()

    classe = re.sub("\s\s+", "", classe)
    assunto = re.sub("\s\s+", "", assunto)
    juiz = re.sub("\s\s+", "", juiz)

    valor = re.sub("[R$]", "", valor)
    valor = re.sub("\s*", "", valor)
    valor = re.sub("\.", "", valor)
    valor = re.sub("\,", ".", valor)
    valor = float(valor)

    area = re.sub("\s\s+", "", area)
    distribuicao = re.sub("\s\s+", "", distribuicao)

    processo = Processo(numero_unico=numero_unico, classe=classe, area=area, assunto=assunto, distribuicao=distribuicao,
                        juiz=juiz, valor=valor)
    return processo


def get_partes(selector: Selector, processo: Processo, action: str):
    if action == 'update':
        partes = Parte.query.filter_by(processo_id = processo.id).all()

        for parte in partes:
            for tr in selector.xpath('//*[@id="tablePartesPrincipais"]/tr'):
                titulo = re.sub("[(:|\s)]+", "", tr.xpath('./td[1]/span/text()').extract_first() )
                p = tr.xpath('./td[2]/text()').extract()
                nome = p[0]

                p = p[1:]
                representacao = tr.xpath('./td[2]/span/text()').extract()

                parte.tipo = titulo
                parte.nome = nome

                representantes = Representante.query.filter_by(parte_id = parte.id).all()
                for representante in representantes:
                    for i,rep in enumerate(p):
                        tipo = re.sub("[(:|\s)]+", "", representacao[i])

                        representante.tipo = tipo
                        representante.nome = nome

    else:
        partes = []
        for tr in selector.xpath('//*[@id="tablePartesPrincipais"]/tr'):
            titulo = re.sub("[(:|\s)]+", "", tr.xpath('./td[1]/span/text()').extract_first() )
            p = tr.xpath('./td[2]/text()').extract()
            nome = p[0]

            p = p[1:]
            representacao = tr.xpath('./td[2]/span/text()').extract()

            pt = Parte(tipo=titulo, nome=nome, processo=processo)
            if action == "update":
                db.session.merge(pt)
            else:
                db.session.add(pt)
            db.session.commit()

            representantes = []
            for i,rep in enumerate(p):
                tipo = re.sub("[(:|\s)]+", "", representacao[i])

                r = Representante(tipo=tipo, nome=rep, parte=pt)
                db.session.add(r)
                db.session.commit()

                representantes.append(r)
            partes.append(pt)

    return partes, representantes


def busca_processo(numero_unico: str) -> Selector:
    url = 'https://www2.tjal.jus.br/cpopg/search.do'
    params = {
        "conversationId": "",
        "dadosConsulta.localPesquisa.cdLocal": "-1",
        "cbPesquisa": "NUMPROC",
        "dadosConsulta.tipoNuProcesso": "UNIFICADO",
        "numeroDigitoAnoUnificado": numero_unico[:13],
        "foroNumeroUnificado": numero_unico[-4:],
        "dadosConsulta.valorConsultaNuUnificado": numero_unico,
        "dadosConsulta.valorConsulta": "",
        "uuidCaptcha": ""
        }

    response = requests.get(url, params=params)
    text = response.text

    # removes whitespaces
    text = re.sub("[\t\r\n]", "", text)
    selector = Selector(text)

    return selector

def valid(selector):
    s = selector.xpath("//*[@id='mensagemRetorno']//*[contains(text(), 'Não existem informações disponíveis para os parâmetros informados.')]")
    
    return not s.extract()