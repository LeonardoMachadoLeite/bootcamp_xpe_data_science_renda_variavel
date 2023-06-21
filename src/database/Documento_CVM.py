class Documento_CVM(object):
    def __init__(self, row):
        self.cod_cvm = row[0]
        self.sequencia = row[1]
        self.versao = row[2]
        self.protocolo = row[3]
        self.tipo = row[4]
    
    def values(self):
        return f"('{self.cod_cvm}', {self.sequencia}, {self.versao}, '{self.protocolo}', '{self.tipo}')"
    
    def insert_all(list_docs_cvm):
        first = True
        sql = "REPLACE INTO 'documentos_cvm' ('cod_cvm', 'sequencia', 'versao') VALUES"

        for doc_cvm in list_docs_cvm:
            if not first:
                sql = f"{sql},{doc_cvm.values()}"
            else:
                sql = f"{sql} {doc_cvm.values()}"
                first = False
        
        return sql
    
    def get_data_doc(self):
        data = self.protocolo[9:17]
        dia = data[:2]
        mes = data[2:4]
        ano = data[-4:]
        return f"{ano}-{mes}-{dia}"

    def get_xml_name(self):
        return f"{self.cod_cvm}{self.tipo}{self.get_data_doc()}v{self.versao}.xml"

def main():
    row = ('021610', 103505, 1, '021610ITR310320210100103505-72', 'ITR')
    doc = Documento_CVM(row)
    # x = doc.__dict__
    # print(x)

    print(doc.get_xml_name())

if __name__ == '__main__':
    main()
