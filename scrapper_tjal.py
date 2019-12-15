import aiohttp
from parsel import Selector
import re
from models import *

def get_movimentacoes(selector):
    movimentacoes = []
    for tr in selector.xpath('//*[@id="tabelaTodasMovimentacoes"]/tr'):
        data = tr.xpath('./td[1]/text()').extract_first()

        titulo = tr.xpath('./td[3]//text()').extract_first()
        if titulo is not None:
            titulo = titulo.strip()

        link = tr.xpath('./td[3]//@href').extract_first()

        conteudo = tr.xpath('./td[3]/span/text()').extract_first()
        if conteudo is not None:
            conteudo = conteudo.strip()

        movimentacoes.append(Movimentacao(titulo, data, conteudo, link))
    return movimentacoes

def get_dados_processo(selector):
    sel = selector.xpath('//*[@class="secaoFormBody" and @id=""]//tr[@class="" and td[1][text()]]')

    classe = sel.xpath(".//td[1][*[contains(text(), 'Classe:')]]/following-sibling::td//span/text()").extract_first()
    assunto = sel.xpath(".//td[1][*[contains(text(), 'Assunto:')]]/following-sibling::td//span/text()").extract_first()
    juiz = sel.xpath(".//td[1][*[contains(text(), 'Juiz:')]]/following-sibling::td//span/text()").extract_first()
    valor = sel.xpath(".//td[1][*[contains(text(), 'Valor da ação:')]]/following-sibling::td//span/text()").extract_first()
    area = sel.xpath(".//td[*[contains(text(), 'Área:')]]/text()[last()]").extract_first()

    classe = re.sub("\s\s+", "", classe)
    assunto = re.sub("\s\s+", "", assunto)
    juiz = re.sub("\s\s+", "", juiz)
    valor = re.sub("[R$|\s]*", "", valor)
    area = re.sub("\s\s+", "", area)

    return classe, assunto, juiz, valor, area

def get_partes(selector):
    partes = []
    for tr in selector.xpath('//*[@id="tablePartesPrincipais"]/tr'):
        titulo = re.sub("[(:|\s)]+", "", tr.xpath('./td[1]/span/text()').extract_first() )
        p = tr.xpath('./td[2]/text()').extract()
        nome = p[0]

        p = p[1:]
        representacao = tr.xpath('./td[2]/span/text()').extract()

        representantes = []
        for i,rep in enumerate(p):
            tipo = re.sub("[(:|\s)]+", "", representacao[i])
            representantes.append(Representante(tipo, rep))
        partes.append(Parte(titulo, nome, representantes))
    return partes

async def busca_processo(numero_unico):
    base_url = "https://www2.tjal.jus.br/"

    async with aiohttp.ClientSession() as session:
        url = base_url + "cpopg/open.do"
        async with session.get(url) as response:
            text = await response.text()
            # print(text)

        url = base_url + "cpopg/search.do"
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

        async with session.get(url, params=params) as response:
            print(response.status)
            print(response.url)
            text = await response.text()

            # removes whitespaces
            text = re.sub("[\t\r\n]", "", text)
            selector = Selector(text)

            movimentacoes = get_movimentacoes(selector)
            partes = get_partes(selector)
            dados_processo = get_dados_processo(selector)
            classe, area, assunto, juiz, valor = get_dados_processo(selector)

            p = Processo(numero_unico, classe, area, assunto, juiz, valor)
            return p, partes, movimentacoes

