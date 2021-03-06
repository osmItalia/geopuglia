# -*- coding: utf-8 -*-

import logging
import os
import errno

import eventlet
import requests


log = logging.getLogger(__name__)

LEGENDS = dict(
    ctr_codes="http://cartografia.sit.puglia.it/download/CTR/SHP/Descrizione_Layer_CTR.xls",
    ctr_legend="http://cartografia.sit.puglia.it/download/CTR/PDF/Legenda_CTR.pdf",
    usd_legend="http://cartografia.sit.puglia.it/download/UDS/SHP/Legenda_UDS.pdf"
)

URLS = dict(
    ctr_vet="http://cartografia.sit.puglia.it/download/CTR/SHP/{foglio}/{filename}_ctr.zip",
    ctr_pdf="http://cartografia.sit.puglia.it/download/CTR/PDF/{foglio}/{filename}.pdf",
    dtm="http://cartografia.sit.puglia.it/download/DTM/ASC/{foglio}/{filename}_asc.zip",
    photos="http://cartografia.sit.puglia.it/download/ORTO/ECW/{foglio}/{filename}_orto.zip",
    uds="http://cartografia.sit.puglia.it/download/UDS/SHP/{foglio}/{filename}_uds.zip"
)

# from http://www.sit.puglia.it/auth/portal/portale_cartografie_tecniche_tematiche/Download/Cartografie
FOGLI_ALL = {
    '382': 'Campo Marino',
    '383': 'Sannicandro Garganico',
    '383_bis': 'Sannicandro Garganico_bis',
    '384': 'Vico del Gargano',
    '384_bis': 'Vico Del Gargano_bis',
    '385': 'Vieste',
    '394': 'Casacalenda',
    '395': 'Torremaggiore',
    '396': 'San Severo',
    '397': 'Manfredonia',
    '398': 'Mattinata',
    '406': 'Riccia',
    '407': 'San Bartolomeo in Galdo',
    '408': 'Foggia',
    '409': 'Zapponeta',
    '410': 'Torre Pietra',
    '420': 'Troia',
    '421': 'Ascoli Satriano',
    '422': 'Cerignola',
    '423': 'Barletta',
    '424': 'Molfetta',
    '433': 'Ariano Irpino',
    '434': 'Candela',
    '435': 'Lavello',
    '436': 'Minervino Murge',
    '437': 'Corato',
    '438': 'Bari',
    '439': 'Mola di Bari',
    '452': 'Rionero in Vulture',
    '453': 'Spinazzola',
    '454': 'Altamura',
    '455': 'Acquaviva delle Fonti',
    '456': 'Monopoli',
    '457': 'Fasano',
    '471': 'Irsina',
    '472': 'Matera',
    '473': 'Gioia del Colle',
    '474': 'Noci',
    '475': 'Martina Franca',
    '476': 'Brindisi',
    '477': 'Brindisi_bis',
    '492': 'Ginosa',
    '493': 'Taranto',
    '494': 'Francavilla Fontana',
    '495': 'Mesagne',
    '496': 'Squinzano',
    '508': 'Policoro',
    '509': 'Leporano',
    '510': 'Manduria',
    '511': 'Veglie',
    '512': 'Lecce',
    '513': 'Melendugno',
    '525': 'Gallipoli',
    '526': 'Nardò',
    '527': 'Otranto',
    '536': 'Ugento',
    '536_bis': 'Ugento_bis',
    '537': 'Capo Santa Maria di Leuca',
    '537_bis': 'Capo Santa Maria Di Leuca_bis'
}

QUADRANTI_ALL = set(range(1, 5))

TAVOLETTE_ALL = set(range(1, 17))


def build_url(download_type, foglio, tavoletta, quadrante):
    """
    Construct the URL using the SIT Puglia logic
    """
    tavoletta = '0{tavoletta}'.format(tavoletta=tavoletta) if tavoletta < 10 else tavoletta
    filename = '{foglio}{tavoletta}{quadrante}'.format(foglio=foglio, tavoletta=tavoletta, quadrante=quadrante)
    url = URLS[download_type].format(foglio=foglio, filename=filename)
    log.debug('URL created: {url}'.format(url=url))
    return url


def download_and_save(url):
    """
    Download and saves the file found at URL
    :param url: string
    :return: filename (string) or None
    """
    try:
        response = requests.get(url, stream=True)
        if response.ok:
            log.debug('{url} found'.format(url=url))
            filename = os.path.join('./downloads', url.split('/')[-1])
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())
                return filename
        else:
            log.debug('{url} not found'.format(url=url))
    except requests.Timeout:
        log.debug('{url} timed out'.format(url=url))
    except requests.ConnectionError:
        log.debug('{url} connection error'.format(url=url))
    return


def make_sure_path_exists(path):
    """
    Try to create the destination folder if doesn't exist
    :param path: string
    :return: None
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    return


def orchestrator(download, fogli, tavolette, quadranti):
    """
    Call the right functions in the proper sequence
    :return: None
    """
    urls = map(lambda tpl: build_url(*tpl),
               [(download_type, foglio, tavoletta, quadrante)
                for download_type in download
                for foglio in fogli
                for tavoletta in tavolette
                for quadrante in quadranti])

    make_sure_path_exists('./downloads')
    pool = eventlet.GreenPool()
    for filename in pool.imap(download_and_save, urls):
        if filename:
            log.info("{filename} saved".format(filename=filename))
    return None