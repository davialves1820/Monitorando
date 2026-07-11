from typing import Union, Optional
from uuid import UUID
from app.factories.usuario_factory import UsuarioFactory
from app.business.relatorio_acesso_usuarios import RelatorioAcessoUsuariosHTML
from app.models.enums import TipoPerfil
from app.models.usuario import UsuarioCadastro, Discente, Docente, UsuarioResponse, PaginatedUsuarios, Monitor, PromoverRequest
from app.repositories.abstract_usuario_repository import AbstractUsuarioRepository
from app.exceptions import (
    LoginException,
    LoginVazioException,
    LoginMuitoLongoException,
    LoginContemNumerosException,
    CredenciaisInvalidasException,
    SenhaCurtaException,
    SenhaSemLetraMaiusculaException,
    SenhaSemLetraMinusculaException,
    SenhaSemNumeroException,
    SenhaSemCaractereEspecialException,
    CamposObrigatoriosException,
    EmailInvalidoException,
    EmailJaCadastradoException,
    UsuarioNaoEncontradoException,
    UsuarioJaEMonitorException,
    PromocaoApenasParaDiscentesException,
    DisciplinaVinculadaObrigatoriaException,
    UsuarioNaoEMonitorException
)

class UsuarioService:
    def __init__(self, repo: AbstractUsuarioRepository) -> None:
        """
        Injeção de dependência: o service depende apenas da interface,
        nunca de uma implementação concreta (DIP).
        """
        self._repo = repo

    def cadastrar_usuario(self, cadastro: UsuarioCadastro) -> Union[Discente, Docente]:
        # 1. Validar as regras do login
        self.validar_login(cadastro.login)

        # 2. Validar preenchimento dos campos obrigatórios comuns
        if (
            not cadastro.nome 
            or not cadastro.nome.strip() 
            or not cadastro.email 
            or not cadastro.email.strip() 
            or not cadastro.senha 
            or not cadastro.senha.strip()
        ):
            raise CamposObrigatoriosException()

        # 3. Validar e-mail institucional e determinar perfil (RN008)
        email = cadastro.email.strip().lower()
        if email.endswith("@discente.ufpb.br"):
            perfil = TipoPerfil.DISCENTE
        elif email.endswith("@ufpb.br") or email.endswith("@ci.ufpb.br"):
            perfil = TipoPerfil.DOCENTE
        else:
            raise EmailInvalidoException()

        # 4. Validar se o e-mail já está cadastrado
        if self._repo.find_by_email(email) is not None:
            raise EmailJaCadastradoException()

        # 5. Validar política de senha (RN009 / IAM)
        self.validar_senha(cadastro.senha)
        senha = cadastro.senha

        # 6. Lógica específica por perfil — criação delegada à UsuarioFactory
        if perfil == TipoPerfil.DISCENTE:
            # Matrícula é obrigatória para discentes
            if not cadastro.matricula or not cadastro.matricula.strip():
                raise CamposObrigatoriosException()
            # Ajusta o e-mail normalizado no cadastro antes de passar à factory
            cadastro = cadastro.model_copy(update={"email": email})
            usuario = UsuarioFactory.criar_discente(cadastro, perfil)
        else:
            # Docente
            cadastro = cadastro.model_copy(update={"email": email})
            usuario = UsuarioFactory.criar_docente(cadastro, perfil)

        # 7. Salvar no repositório
        self._repo.add(usuario)
        return usuario

    def listar_usuarios(self, pagina: int, limite: int) -> PaginatedUsuarios:
        """
        Lista todos os usuários com paginação.
        RF007: limite padrão de 50 registros por página.
        """
        limite_maximo = 200

        if limite > limite_maximo:
            limite = limite_maximo

        skip = (pagina - 1) * limite
        usuarios_db, total = self._repo.find_all_paginated(skip=skip, limit=limite)

        usuarios_response = [
            UsuarioResponse(
                id=u.id,
                nome=u.nome,
                login=u.login,
                email=u.email,
                perfil=u.perfil,
                ativo=u.ativo,
            )
            for u in usuarios_db
        ]

        return PaginatedUsuarios(
            total=total,
            pagina=pagina,
            limite=limite,
            usuarios=usuarios_response,
        )

    def buscar_usuarios(
        self,
        nome: Optional[str],
        matricula: Optional[str],
        pagina: int,
        limite: int,
    ) -> PaginatedUsuarios:
        """
        Busca usuários com filtros opcionais de nome (parcial) e matrícula (exata).
        RF008: retorna 404 quando nenhum resultado é encontrado.
        """
        limite_maximo = 200
        if limite > limite_maximo:
            limite = limite_maximo

        skip = (pagina - 1) * limite
        usuarios_db, total = self._repo.find_by_filters(
            nome=nome,
            matricula=matricula,
            skip=skip,
            limit=limite,
        )

        if total == 0:
            detalhe = "Nenhum usuário encontrado"
            if nome and matricula:
                detalhe = f"Nenhum usuário encontrado com nome contendo '{nome}' e matrícula '{matricula}'."
            elif nome:
                detalhe = f"Nenhum usuário encontrado com nome contendo '{nome}'."
            elif matricula:
                detalhe = f"Nenhum usuário encontrado com matrícula '{matricula}'."
            raise UsuarioNaoEncontradoException(detalhe)

        usuarios_response = [
            UsuarioResponse(
                id=u.id,
                nome=u.nome,
                login=u.login,
                email=u.email,
                perfil=u.perfil,
                ativo=u.ativo,
            )
            for u in usuarios_db
        ]

        return PaginatedUsuarios(
            total=total,
            pagina=pagina,
            limite=limite,
            usuarios=usuarios_response,
        )

    def buscar_usuario_por_id(self, id: UUID) -> Union[Discente, Docente]:
        """Retorna um usuário pelo ID. Lança 404 se não encontrado."""
        usuario = self._repo.find_by_id(id)
        if usuario is None:
            raise UsuarioNaoEncontradoException(f"Usuário com id '{id}' não encontrado.")
        return usuario

    def promover_usuario(self, id: UUID, request: PromoverRequest) -> Monitor:
        usuario = self.buscar_usuario_por_id(id)
        
        if usuario.perfil == TipoPerfil.MONITOR:
            raise UsuarioJaEMonitorException()
        elif usuario.perfil != TipoPerfil.DISCENTE:
            raise PromocaoApenasParaDiscentesException()
            
        if not request.disciplinaVinculada or not request.disciplinaVinculada.strip():
            raise DisciplinaVinculadaObrigatoriaException()
            
        monitor = UsuarioFactory.promover_para_monitor(usuario, request)
        self._repo.update(monitor)
        return monitor

    def revogar_monitor(self, id: UUID) -> Discente:
        usuario = self.buscar_usuario_por_id(id)
        
        if usuario.perfil != TipoPerfil.MONITOR:
            raise UsuarioNaoEMonitorException()
            
        aluno = UsuarioFactory.revogar_monitor(usuario)
        self._repo.update(aluno)
        return aluno

    def validar_login(self, login: str) -> None:
        if not login or not login.strip():
            raise LoginVazioException()
        if len(login) > 12:
            raise LoginMuitoLongoException()
        if any(char.isdigit() for char in login):
            raise LoginContemNumerosException()

    def validar_senha(self, senha: str) -> None:
        if not senha or len(senha) < 8:
            raise SenhaCurtaException()
        if not any(c.isupper() for c in senha):
            raise SenhaSemLetraMaiusculaException()
        if not any(c.islower() for c in senha):
            raise SenhaSemLetraMinusculaException()
        if not any(c.isdigit() for c in senha):
            raise SenhaSemNumeroException()
        
        # Caracteres especiais do AWS IAM: !@#$%^&*()_+-=[]{}|'
        especiais = "!@#$%^&*()_+-=[]{}|'"
        if not any(c in especiais for c in senha):
            raise SenhaSemCaractereEspecialException()

    def login_usuario(self, login: str, senha: str) -> Union[Discente, Docente, Monitor]:
        self.validar_login(login)
        usuario = self._repo.find_by_login(login.strip())
        if usuario is None:
            raise CredenciaisInvalidasException()
        if usuario.senha != senha:
            raise CredenciaisInvalidasException()
        return usuario

    def gerar_relatorio_acesso_html(self) -> str:
        usuarios = self._repo.find_all()
        return RelatorioAcessoUsuariosHTML().gerar(usuarios)
