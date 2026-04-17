class OrderExcelImportService:
    

    def importfile(self, file):
        if not file:
            raise ValueError("Nenhum arquivo fornecido.")
        
        # Se o arquivo for válido, ele será processado       

        #le linhas
        
        # valida
        # se ok, insere
        # se não ok, insere na planilha de erros