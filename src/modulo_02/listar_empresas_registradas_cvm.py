import requests_html
import re
import pandas as pd
import numpy as np
import os

def status_registro(valor_registro):
    regex = r"\(.*?\)"
    matches = re.findall(regex, valor_registro)
    if len(matches) > 0:
        return matches[0][1:-1]
    else:
        return np.nan

def extract_name(value):
    min_ = value.find('-') + 2
    max_ = value.find('(') - 1

    if max_ == -2:
        max_ = len(value)

    return value[min_:max_]

class EmpresasRegistradasCVM(object):

    def __init__(self):
        if os.path.exists('registros_empresas_cvm.csv'):
            self.ler_arquivo_registro_empresas_cvm()
        else:
            self.atualizar_empresas_registradas()

    def baixar_registro_empresas_cvm():
        r = requests_html.HTMLSession().get("https://www.rad.cvm.gov.br/ENET/frmConsultaExternaCVM.aspx")
        a = re.findall(r'(?<=<input name="hdnEmpresas" type="hidden" id="hdnEmpresas" value=")[^"]*(?=" />)', r.text)
        a = a[0]

        df_empresas = pd.DataFrame(list(eval(a.replace("{ key:", "{'key':").replace("value:", "'value':"))))
        df_empresas['status'] = df_empresas['value'].apply(lambda x: status_registro(x))
        df_empresas['value'] = df_empresas['value'].apply(lambda x: extract_name(x))
        df_empresas['key'] = df_empresas['key'].apply(lambda x: x[2:])

        return df_empresas
    
    def atualizar_empresas_registradas(self):
        self.empresas = EmpresasRegistradasCVM.baixar_registro_empresas_cvm()

    def ler_arquivo_registro_empresas_cvm(self):
        self.empresas = pd.read_csv('registros_empresas_cvm.csv', dtype={'key':'object'}, sep=';')

    def salvar_arquivo_registro_empresas_cvm(self):
        self.empresas.to_csv('registros_empresas_cvm.csv', sep=';', index=False)