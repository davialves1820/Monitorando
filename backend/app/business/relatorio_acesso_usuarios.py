from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass
from html import escape
from typing import Dict, List, Sequence

from app.models.usuario import Usuario


@dataclass(frozen=True)
class EstatisticasAcessoUsuarios:
    total_usuarios: int
    usuarios_ativos: int
    usuarios_inativos: int
    percentual_ativos: float
    usuarios_por_perfil: Dict[str, int]

    @classmethod
    def calcular(cls, usuarios: Sequence[Usuario]) -> "EstatisticasAcessoUsuarios":
        total = len(usuarios)
        ativos = sum(1 for usuario in usuarios if usuario.ativo)
        inativos = total - ativos
        percentual_ativos = (ativos / total * 100) if total else 0.0
        por_perfil = Counter(usuario.perfil.value for usuario in usuarios)

        return cls(
            total_usuarios=total,
            usuarios_ativos=ativos,
            usuarios_inativos=inativos,
            percentual_ativos=percentual_ativos,
            usuarios_por_perfil=dict(sorted(por_perfil.items())),
        )


class RelatorioAcessoUsuariosTemplate(ABC):
    """
    Template Method para relatorios de estatisticas de acesso dos usuarios.

    O fluxo de geracao fica fixo em `gerar`; subclasses definem o formato
    renderizando cada secao do documento.
    """

    def gerar(self, usuarios: Sequence[Usuario]) -> str:
        estatisticas = EstatisticasAcessoUsuarios.calcular(usuarios)
        secoes = [
            self.renderizar_cabecalho(estatisticas),
            self.renderizar_resumo(estatisticas),
            self.renderizar_distribuicao_perfis(estatisticas),
            self.renderizar_rodape(estatisticas),
        ]
        return self.montar_documento(secoes)

    @abstractmethod
    def renderizar_cabecalho(self, estatisticas: EstatisticasAcessoUsuarios) -> str:
        ...

    @abstractmethod
    def renderizar_resumo(self, estatisticas: EstatisticasAcessoUsuarios) -> str:
        ...

    @abstractmethod
    def renderizar_distribuicao_perfis(self, estatisticas: EstatisticasAcessoUsuarios) -> str:
        ...

    @abstractmethod
    def renderizar_rodape(self, estatisticas: EstatisticasAcessoUsuarios) -> str:
        ...

    @abstractmethod
    def montar_documento(self, secoes: List[str]) -> str:
        ...


class RelatorioAcessoUsuariosHTML(RelatorioAcessoUsuariosTemplate):
    def renderizar_cabecalho(self, estatisticas: EstatisticasAcessoUsuarios) -> str:
        return (
            "<header>"
            "<h1>Relat&oacute;rio de acesso dos usu&aacute;rios</h1>"
            "<p>Estat&iacute;sticas consolidadas de usu&aacute;rios com acesso ao sistema.</p>"
            "</header>"
        )

    def renderizar_resumo(self, estatisticas: EstatisticasAcessoUsuarios) -> str:
        return (
            "<section>"
            "<h2>Resumo</h2>"
            "<dl>"
            f"<dt>Total de usu&aacute;rios</dt><dd>{estatisticas.total_usuarios}</dd>"
            f"<dt>Usu&aacute;rios ativos</dt><dd>{estatisticas.usuarios_ativos}</dd>"
            f"<dt>Usu&aacute;rios inativos</dt><dd>{estatisticas.usuarios_inativos}</dd>"
            f"<dt>Percentual ativo</dt><dd>{estatisticas.percentual_ativos:.2f}%</dd>"
            "</dl>"
            "</section>"
        )

    def renderizar_distribuicao_perfis(self, estatisticas: EstatisticasAcessoUsuarios) -> str:
        linhas = [
            "<tr><th>Perfil</th><th>Quantidade</th></tr>",
            *[
                f"<tr><td>{escape(perfil)}</td><td>{quantidade}</td></tr>"
                for perfil, quantidade in estatisticas.usuarios_por_perfil.items()
            ],
        ]

        if not estatisticas.usuarios_por_perfil:
            linhas.append("<tr><td colspan=\"2\">Nenhum usu&aacute;rio cadastrado</td></tr>")

        return (
            "<section>"
            "<h2>Distribui&ccedil;&atilde;o por perfil</h2>"
            "<table>"
            "<tbody>"
            f"{''.join(linhas)}"
            "</tbody>"
            "</table>"
            "</section>"
        )

    def renderizar_rodape(self, estatisticas: EstatisticasAcessoUsuarios) -> str:
        return (
            "<footer>"
            "<p>Relat&oacute;rio gerado pelo sistema Monitorando.</p>"
            "</footer>"
        )

    def montar_documento(self, secoes: List[str]) -> str:
        corpo = "".join(secoes)
        return (
            "<!DOCTYPE html>"
            "<html lang=\"pt-BR\">"
            "<head>"
            "<meta charset=\"utf-8\">"
            "<title>Relat&oacute;rio de acesso dos usu&aacute;rios</title>"
            "<style>"
            "body{font-family:Arial,sans-serif;margin:32px;color:#1f2933;}"
            "header{border-bottom:1px solid #d9e2ec;margin-bottom:24px;}"
            "h1{font-size:28px;margin:0 0 8px;}"
            "h2{font-size:20px;margin-top:24px;}"
            "dl{display:grid;grid-template-columns:220px 1fr;gap:8px 16px;}"
            "dt{font-weight:700;}"
            "dd{margin:0;}"
            "table{border-collapse:collapse;min-width:360px;}"
            "th,td{border:1px solid #bcccdc;padding:8px 12px;text-align:left;}"
            "th{background:#f0f4f8;}"
            "footer{margin-top:32px;color:#52606d;font-size:13px;}"
            "</style>"
            "</head>"
            f"<body>{corpo}</body>"
            "</html>"
        )
