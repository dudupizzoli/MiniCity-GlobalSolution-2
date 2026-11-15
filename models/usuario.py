class Usuario:
    #Construtor da classe Local
    def __init__(self, username, senha_user, email_user, assinatura, id_usuario=None, relatorios=None):
        self._id_usuario = id_usuario
        self._username = username
        self._senha_user = senha_user
        self._email_user = email_user
        self._assinatura = assinatura
        if relatorios is None:
            self._missoes = []
        else:
            self._missoes = relatorios
    
    #Método para exibir o objeto Usuario
    def __str__(self):
        return f"\nID: {self._id_usuario} | Nome de Usuário: {self._username} | Email: {self._email_user}"
