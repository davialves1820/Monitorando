"""
Factory Method — criação de objetos de domínio do módulo Usuário.

Centraliza a lógica de instanciação de Discente, Docente, Monitor e
InscricaoMonitoria, eliminando a criação ad-hoc dispersa nos services.

Padrão aplicado: Factory Method (GoF)
  Os métodos estáticos encapsulam *como* cada entidade é construída.
  Os services continuam responsáveis pelas *regras de negócio* que
  precedem a criação (validações, verificações de duplicidade etc.),
  mas delegam a montagem do objeto final a esta factory.

Hierarquia de entidades suportadas:
    Usuario
    ├── Discente   ← criar_discente()
    │   └── Monitor ← promover_para_monitor()
    └── Docente    ← criar_docente()

Exemplo de uso no service:
    from app.factories.usuario_factory import UsuarioFactory

    usuario = UsuarioFactory.criar_discente(cadastro, perfil)
    monitor = UsuarioFactory.promover_para_monitor(discente, request)
    aluno   = UsuarioFactory.revogar_monitor(monitor)
"""

from app.models.enums import TipoPerfil
from app.models.inscricao_monitoria import InscricaoMonitoria, InscricaoMonitoriaCadastro
from app.models.usuario import (
    Discente,
    Docente,
    Monitor,
    PromoverRequest,
    Usuario,
    UsuarioCadastro,
)


class UsuarioFactory:
    """
    Factory de entidades do domínio de usuários.

    Todos os métodos são estáticos — a factory não mantém estado próprio.
    Isso reflete a natureza pura de criação: entrada de dados brutos,
    saída de objetos de domínio válidos e imutáveis.
    """

    @staticmethod
    def criar_discente(cadastro: UsuarioCadastro, perfil: TipoPerfil) -> Discente:
        """
        Cria e retorna um Discente a partir dos dados de cadastro.

        Args:
            cadastro: Dados de entrada do formulário de cadastro.
            perfil:   TipoPerfil já validado (deve ser DISCENTE).

        Returns:
            Instância de Discente com ID gerado automaticamente.

        Note:
            A validação de que `matricula` é obrigatória deve ocorrer
            *antes* de chamar este método (responsabilidade do service).
        """
        return Discente(
            nome=cadastro.nome.strip(),
            login=cadastro.login.strip(),
            email=cadastro.email.strip().lower(),
            senha=cadastro.senha,
            perfil=perfil,
            matricula=cadastro.matricula.strip() if cadastro.matricula else "",
            curso=cadastro.curso.strip() if cadastro.curso else "",
            periodo=cadastro.periodo,
            disciplinasInteresse=[],
        )

    @staticmethod
    def criar_docente(cadastro: UsuarioCadastro, perfil: TipoPerfil) -> Docente:
        """
        Cria e retorna um Docente a partir dos dados de cadastro.

        Args:
            cadastro: Dados de entrada do formulário de cadastro.
            perfil:   TipoPerfil já validado (deve ser DOCENTE).

        Returns:
            Instância de Docente com ID gerado automaticamente.
        """
        return Docente(
            nome=cadastro.nome.strip(),
            login=cadastro.login.strip(),
            email=cadastro.email.strip().lower(),
            senha=cadastro.senha,
            perfil=perfil,
            siape=cadastro.siape.strip() if cadastro.siape else "",
            departamento=cadastro.departamento.strip() if cadastro.departamento else "",
            isCoordenador=cadastro.isCoordenador if cadastro.isCoordenador is not None else False,
            disciplinas=[],
        )

    @staticmethod
    def promover_para_monitor(discente: Discente, request: PromoverRequest) -> Monitor:
        """
        Cria um Monitor a partir de um Discente existente e dos dados da promoção.

        Preserva o UUID original do discente, garantindo rastreabilidade.

        Args:
            discente: Discente que será promovido.
            request:  Dados da promoção (disciplina vinculada, carga horária).

        Returns:
            Instância de Monitor com o mesmo ID do discente original.

        Note:
            A validação das pré-condições de negócio (perfil DISCENTE,
            disciplinaVinculada não-vazia) deve ocorrer antes desta chamada.
        """
        return Monitor(
            id=discente.id,
            nome=discente.nome,
            login=discente.login,
            email=discente.email,
            senha=discente.senha,
            perfil=TipoPerfil.MONITOR,
            ativo=discente.ativo,
            matricula=discente.matricula,
            curso=discente.curso,
            periodo=discente.periodo,
            disciplinasInteresse=discente.disciplinasInteresse,
            cargaHoraria=request.cargaHoraria,
            disciplinaVinculada=request.disciplinaVinculada.strip(),
            disponivel=True,
        )

    @staticmethod
    def revogar_monitor(monitor: Monitor) -> Discente:
        """
        Cria um Discente a partir de um Monitor existente (operação de revogação).

        Preserva o UUID original e os dados acadêmicos do ex-monitor.

        Args:
            monitor: Monitor que terá o status revogado.

        Returns:
            Instância de Discente com o mesmo ID do monitor original.

        Note:
            A validação de que o usuário é de fato um monitor deve
            ocorrer antes desta chamada (responsabilidade do service).
        """
        return Discente(
            id=monitor.id,
            nome=monitor.nome,
            login=monitor.login,
            email=monitor.email,
            senha=monitor.senha,
            perfil=TipoPerfil.DISCENTE,
            ativo=monitor.ativo,
            matricula=monitor.matricula,
            curso=monitor.curso,
            periodo=monitor.periodo,
            disciplinasInteresse=monitor.disciplinasInteresse,
        )

    @staticmethod
    def criar_inscricao(cadastro: InscricaoMonitoriaCadastro) -> InscricaoMonitoria:
        """
        Cria e retorna uma InscricaoMonitoria com status inicial PENDENTE.

        Args:
            cadastro: Dados de entrada do formulário de inscrição.

        Returns:
            Instância de InscricaoMonitoria com ID gerado automaticamente
            e status "PENDENTE".

        Note:
            A validação dos relacionamentos (usuario_id e disciplina_id
            existentes) deve ocorrer antes desta chamada.
        """
        return InscricaoMonitoria(
            usuario_id=cadastro.usuario_id,
            disciplina_id=cadastro.disciplina_id,
            motivacao=cadastro.motivacao.strip(),
        )
