import aiohttp
from scrapper_tjal import busca_processo

async def main():
    processo = await busca_processo("07175619820198020001")
    # processo = await busca_processo("00671545520108020001")
    print(processo)
    # p = Processo(numero_unico="07175619820198020001")
    # p.get_or_create()

