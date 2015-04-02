#!/bin/python
# -*- coding: utf-8 -*-

import argparse
import logging
from urllib2 import urlopen, HTTPError
from threading import Thread
from Queue import Queue
from functools import wraps
from socket import error as SocketError

log = logging.getLogger('CTR Downloader')

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
    URL is built following the CTR logic
    """
    tavoletta = '0{tavoletta}'.format(tavoletta=tavoletta) if tavoletta < 10 else tavoletta
    filename = '{foglio}{tavoletta}{quadrante}'.format(foglio=foglio, tavoletta=tavoletta, quadrante=quadrante)
    url = URLS[download_type].format(foglio=foglio, filename=filename)
    log.debug('URL created: {url}'.format(url=url))
    return url

def run_async(func):
    @wraps(func)
    def wrap(queue, *args, **kwargs):
        queue.put(func(*args, **kwargs))

    def call(*args, **kwargs):
        queue = Queue()
        job = Thread(target=wrap, args=(queue, ) + args, kwargs=kwargs)
        job.start()
        return queue

    return call

#@run_async
def download_and_save(url):
    """
    Saving file is a I/O blocking operation and I can't get it to work with threads and queues
    Investigate select module before uncommenting the decorator, it'll be slow for time being
    """
    try:
        data = urlopen(url)
        log.debug('{url} found'.format(url=url))
        filename = url.split('/')[-1]
        with open(filename, "wb") as filename:
            filename.write(data.read())
            log.info("{filename} saved".format(filename=filename))
    except HTTPError:
        log.debug('{url} not found'.format(url=url))
    except SocketError:
        log.debug('{url} socket error'.format(url=url))


def get_args():
    parser = argparse.ArgumentParser(description="Download SIT Puglia CTR")
    parser.add_argument('--fogli', type=str, nargs='+', choices=set(FOGLI_ALL.keys()), default=set(FOGLI_ALL.keys()))
    parser.add_argument('--tavolette', type=int, nargs='+', choices=TAVOLETTE_ALL, default=TAVOLETTE_ALL)
    parser.add_argument('--quadranti', type=int, nargs='+', choices=QUADRANTI_ALL, default=QUADRANTI_ALL)
    parser.add_argument('--download', type=str, nargs='+', choices=set(URLS.keys()), default=set(URLS.keys()))
    parser.add_argument('-v', '--verbose', action='store_true', help='', default=False)

    return parser.parse_args()


def main(download, fogli, tavolette, quadranti):
    # build urls for all the combinations needed
    urls = map(lambda tpl: build_url(*tpl),
               [(download_type, foglio, tavoletta, quadrante)
                for download_type in download
                for foglio in fogli
                for tavoletta in tavolette
                for quadrante in quadranti])

    map(download_and_save, urls)

if __name__ == '__main__':
    args = get_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    main(args.download, args.fogli, args.tavolette, args.quadranti)