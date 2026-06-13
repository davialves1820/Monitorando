from fastapi import HTTPException
from typing import Union, Optional
from uuid import UUID
from app.models.enums import TipoPerfil
from app.models.usuario import UsuarioCadastro, Discente, Docente, UsuarioResponse, PaginatedUsuarios, Monitor, PromoverRequest
from app.repositories.usuario_repository import usuario_repository
from app.exceptions import (
    LoginException,
    LoginVazioException,
    LoginMuitoLongoException,
    LoginContemNumerosException,
    CredenciaisInvalidasException
)

class UsuarioService:
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
            raise HTTPException(
                status_code=400,
                detail="Preencha todos os campos obrigatórios para continuar"
            )

        # 3. Validar e-mail institucional e determinar perfil (RN008)
        email = cadastro.email.strip().lower()
        if email.endswith("@discente.ufpb.br"):
            perfil = TipoPerfil.DISCENTE
        elif email.endswith("@ufpb.br") or email.endswith("@ci.ufpb.br"):
            perfil = TipoPerfil.DOCENTE
        else:
            raise HTTPException(
                status_code=400,
                detail="E-mail inválido ou já cadastrado. Utilize seu e-mail institucional."
            )

        # 4. Validar se o e-mail já está cadastrado
        if usuario_repository.find_by_email(email) is not None:
            raise HTTPException(
                status_code=400,
                detail="E-mail inválido ou já cadastrado. Utilize seu e-mail institucional."
            )

        # 5. Validar política de senha (RN009)
        senha = cadastro.senha
        if (
            not (8 <= len(senha) <= 100) 
            or not any(c.isupper() for c in senha) 
            or not any(c.isdigit() for c in senha)
        ):
            raise HTTPException(
                status_code=400,
                detail="A senha deve conter entre 8 e 100 caracteres, incluindo pelo menos uma letra maiúscula e um número."
            )

        # 6. Lógica específica por perfil
        if perfil == TipoPerfil.DISCENTE:
            # Matrícula é obrigatória para discentes
            if not cadastro.matricula or not cadastro.matricula.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Preencha todos os campos obrigatórios para continuar"
                )
            
            usuario = Discente(
                nome=cadastro.nome.strip(),
                login=cadastro.login.strip(),
                email=email,
                senha=senha,
                perfil=perfil,
                matricula=cadastro.matricula.strip(),
                curso=cadastro.curso.strip() if cadastro.curso else "",
                periodo=cadastro.periodo,
                disciplinasInteresse=[]
            )
        else:
            # Docente
            usuario = Docente(
                nome=cadastro.nome.strip(),
                login=cadastro.login.strip(),
                email=email,
                senha=senha,
                perfil=perfil,
                siape=cadastro.siape.strip() if cadastro.siape else "",
                departamento=cadastro.departamento.strip() if cadastro.departamento else "",
                isCoordenador=cadastro.isCoordenador if cadastro.isCoordenador is not None else False,
                disciplinas=[]
            )

        # 7. Salvar na coleção em memória
        usuario_repository.add(usuario)
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
        usuarios_db, total = usuario_repository.find_all_paginated(skip=skip, limit=limite)

        usuarios_response = [
            UsuarioResponse(
                id=u.id,
                nome=u.nome,
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
        usuarios_db, total = usuario_repository.find_by_filters(
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
            raise HTTPException(status_code=404, detail=detalhe)

        usuarios_response = [
            UsuarioResponse(
                id=u.id,
                nome=u.nome,
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
        usuario = usuario_repository.find_by_id(id)
        if usuario is None:
            raise HTTPException(
                status_code=404,
                detail=f"Usuário com id '{id}' não encontrado."
            )
        return usuario

    def promover_usuario(self, id: UUID, request: PromoverRequest) -> Monitor:
        usuario = self.buscar_usuario_por_id(id)
        
        if usuario.perfil == TipoPerfil.MONITOR:
            raise HTTPException(
                status_code=400,
                detail="Usuário já é um monitor."
            )
        elif usuario.perfil != TipoPerfil.DISCENTE:
            raise HTTPException(
                status_code=400,
                detail="Apenas discentes podem ser promovidos a monitor."
            )
            
        if not request.disciplinaVinculada or not request.disciplinaVinculada.strip():
            raise HTTPException(
                status_code=400,
                detail="Disciplina vinculada é obrigatória."
            )
            
        monitor = Monitor(
            id=usuario.id,
            nome=usuario.nome,
            login=usuario.login,
            email=usuario.email,
            senha=usuario.senha,
            perfil=TipoPerfil.MONITOR,
            ativo=usuario.ativo,
            matricula=usuario.matricula,
            curso=usuario.curso,
            periodo=usuario.periodo,
            disciplinasInteresse=usuario.disciplinasInteresse,
            cargaHoraria=request.cargaHoraria,
            disciplinaVinculada=request.disciplinaVinculada.strip(),
            disponivel=True
        )
        
        usuario_repository.update(monitor)
        return monitor

    def revogar_monitor(self, id: UUID) -> Discente:
        usuario = self.buscar_usuario_por_id(id)
        
        if usuario.perfil != TipoPerfil.MONITOR:
            raise HTTPException(
                status_code=400,
                detail="O usuário não é um monitor."
            )
            
        aluno = Discente(
            id=usuario.id,
            nome=usuario.nome,
            login=usuario.login,
            email=usuario.email,
            senha=usuario.senha,
            perfil=TipoPerfil.DISCENTE,
            ativo=usuario.ativo,
            matricula=usuario.matricula,
            curso=usuario.curso,
            periodo=usuario.periodo,
            disciplinasInteresse=usuario.disciplinasInteresse
        )
        
        usuario_repository.update(aluno)
        return aluno

    def validar_login(self, login: str) -> None:
        if not login or not login.strip():
            raise LoginVazioException()
        if len(login) > 12:
            raise LoginMuitoLongoException()
        if any(char.isdigit() for char in login):
            raise LoginContemNumerosException()

    def login_usuario(self, login: str, senha: str) -> Union[Discente, Docente, Monitor]:
        self.validar_login(login)
        usuario = usuario_repository.find_by_login(login.strip())
        if usuario is None:
            raise CredenciaisInvalidasException()
        if usuario.senha != senha:
            raise CredenciaisInvalidasException()
        return usuario

usuario_service = UsuarioService()
