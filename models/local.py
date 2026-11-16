class Local:
    #Construtor da classe Local
    def __init__(self, cidade, bairro, endereco, noticia, id_local=None):
        self._id_local = id_local
        self._cidade = cidade
        self._bairro = bairro
        self._endereco = endereco
        self._noticia = noticia

    #Método para exibir o objeto Local
    def __str__(self):
        return f"\nID: {self._id_local} | Cidade: {self._cidade} | Bairro: {self._bairro} | \nEndereço: {self._endereco} | \n{self._noticia}"




