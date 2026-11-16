class Usuario:
    #Construtor da classe Local
    def __init__(self, username, senha_user, email_user, assinatura="Padrão", id_usuario=None):
        self._id_usuario = id_usuario
        self._username = username
        self._senha_user = senha_user
        self._email_user = email_user
        self._assinatura = assinatura
    
    #Método para exibir o objeto Usuario
    def __str__(self):
        return f"\nID: {self._id_usuario} | Nome de Usuário: {self._username} | \nEmail: {self._email_user} | Plano: {self._assinatura}"
