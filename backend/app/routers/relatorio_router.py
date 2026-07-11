from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse


router = APIRouter(prefix="/relatorios", tags=["Relatorios"])


@router.get(
    "/acessos/usuarios.html",
    response_class=HTMLResponse,
    summary="Gerar relatorio HTML de acesso dos usuarios",
)
def relatorio_acesso_usuarios_html(request: Request) -> HTMLResponse:
    html = request.app.state.usuario_service.gerar_relatorio_acesso_html()
    return HTMLResponse(content=html)

