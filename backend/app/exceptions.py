class LoginException(Exception):
    """Classe base para exceções relacionadas ao login."""
    pass

class LoginVazioException(LoginException):
    """Exceção lançada quando o login informado é vazio."""
    def __init__(self, message="O login não pode ser vazio."):
        self.message = message
        super().__init__(self.message)

class LoginMuitoLongoException(LoginException):
    """Exceção lançada quando o login ultrapassa 12 caracteres."""
    def __init__(self, message="O login deve ter no máximo 12 caracteres."):
        self.message = message
        super().__init__(self.message)

class LoginContemNumerosException(LoginException):
    """Exceção lançada quando o login contém números."""
    def __init__(self, message="O login não pode conter números."):
        self.message = message
        super().__init__(self.message)

class CredenciaisInvalidasException(LoginException):
    """Exceção lançada para erros de autenticação (senha incorreta ou usuário inexistente)."""
    def __init__(self, message="Login ou senha incorretos."):
        self.message = message
        super().__init__(self.message)

class IOException(Exception):
    """Exceção lançada para erros de Entrada/Saída (E/S) no sistema de arquivos."""
    def __init__(self, message="Erro de Entrada/Saída."):
        self.message = message
        super().__init__(self.message)

