import requests_html
import re
import pandas as pd
import xmltodict
import zipfile
import os
import sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
CLASSES_DIR = os.getenv("CLASSES_DIR")

sys.path.append(CLASSES_DIR)

from database.Documento_CVM import Documento_CVM

class DownloadDocXmlRadCvm(object):

    URL = "https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext"

    def __init__(self, doc_cvm: Documento_CVM):
        self.doc_cvm = doc_cvm

    def build_url(self):
        return f"{DownloadDocXmlRadCvm.URL}&numSequencia={self.doc_cvm.sequencia}&numVersao={self.doc_cvm.versao}&numProtocolo={self.doc_cvm.protocolo}&descTipo={self.doc_cvm.tipo}&CodigoInstituicao=1"
    
    def download_xml(self):
        r = requests_html.HTMLSession().get(self.build_url())
        with open(f"{self.doc_cvm.protocolo}.zip", 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
    
    def open_xml(self):
        archive = zipfile.ZipFile(f"{self.doc_cvm.protocolo}.zip", 'r')
        xml_itr = archive.read("FormularioDemonstracaoFinanceiraITR.xml")
        self.dados = xmltodict.parse(xml_itr)
    

