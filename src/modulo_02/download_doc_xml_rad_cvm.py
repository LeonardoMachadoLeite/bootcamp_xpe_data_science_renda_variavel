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
XML_FOLDER = os.getenv("XML_TEMP_FOLDER")


sys.path.append(CLASSES_DIR)

from database.Documento_CVM import Documento_CVM

class DownloadDocXmlRadCvm(object):

    URL = "https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext"

    def __init__(self, doc_cvm: Documento_CVM):
        self.doc_cvm = doc_cvm

        if os.path.exists(f"{XML_FOLDER}\\{self.doc_cvm.protocolo}.zip"):
            self.open_xml()
        else:
            self.download_xml()
            self.open_xml()

    def build_url(self):
        return f"{DownloadDocXmlRadCvm.URL}&numSequencia={self.doc_cvm.sequencia}&numVersao={self.doc_cvm.versao}&numProtocolo={self.doc_cvm.protocolo}&descTipo={self.doc_cvm.tipo}&CodigoInstituicao=1"
    
    def download_xml(self):
        r = requests_html.HTMLSession().get(self.build_url())
        with open(f"{XML_FOLDER}\\{self.doc_cvm.protocolo}.zip", 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
    
    def baixar_novamente_xml(self):
        self.download_xml()
        self.open_xml()

    def open_xml(self):
        archive = zipfile.ZipFile(f"{XML_FOLDER}\\{self.doc_cvm.protocolo}.zip", 'r')
        xml_itr = archive.read(self.doc_cvm.get_xml_name())
        self.dados = xmltodict.parse(xml_itr)
    

