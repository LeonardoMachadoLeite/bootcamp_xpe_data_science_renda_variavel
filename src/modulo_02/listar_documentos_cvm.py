import requests_html
import re
import pandas as pd

class ListarDocumentosCVM(object):

    ROTA_URL = "https://www.rad.cvm.gov.br/ENET/frmConsultaExternaCVM.aspx/ListarDocumentos"

    def __init__(self, list_cod_cvm, data_de, data_ate):
        self.list_cod_cvm = list_cod_cvm
        self.data_de = data_de
        self.data_ate = data_ate

        self.atualizar_empresas()
        self.atualizar_body()
    
    def atualizar_empresas(self):
        self.str_empresas = ''
        for cod_cvm in self.list_cod_cvm:
            self.str_empresas = f'{self.str_empresas},{cod_cvm}'
    
    def atualizar_body(self):
        self.body = { 
            "dataDe": self.data_de, 
            "dataAte": self.data_ate , 
            "empresa": self.str_empresas, 
            "setorAtividade": '-1', 
            "categoriaEmissor": '-1', 
            "situacaoEmissor": '-1', 
            "tipoParticipante": '-1', 
            "dataReferencia": '', 
            "categoria": 'EST_3', 
            "periodo": '2', 
            "horaIni": '', 
            "horaFim": '', 
            "palavraChave":'',
            "ultimaDtRef":'false', 
            "tipoEmpresa":'0', 
            "token": '', 
            "versaoCaptcha": ''
        }

    def obter_documentos(self):
        r = requests_html.HTMLSession().post(ListarDocumentosCVM.ROTA_URL, json=self.body)
        self.response = r.json()
    
    def cvt_response_to_df(self):
        dados = self.response["d"]["dados"]
        re_doc = re.findall(r"OpenDownloadDocumentos\('(.+?)'\)", dados)

        documents = []
        for match in re_doc:
            args = match.replace("'", "").split(",")
            cod_cvm = args[2][:6]

            documents.append({
                'Cod_CVM': cod_cvm,
                'Sequencia': args[0],
                'Versao': args[1],
                'Protocolo': args[2],
                'Tipo': args[3],
            })
        
        return pd.DataFrame.from_dict(documents)

def main():
    teste = ListarDocumentosCVM(['021610','025461'], '01/01/2021', '01/01/2023')

    teste.obter_documentos()
    args = teste.cvt_response_to_df()
    print(args.head())

if __name__ == '__main__':
    main()
