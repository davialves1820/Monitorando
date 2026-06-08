import sys
from uuid import uuid4

# Adiciona o diretório atual ao sys.path para permitir a importação do pacote 'app'
sys.path.append(".")

from app.repositories.usuario_repository import usuario_repository
from app.models.usuario import Usuario
from app.models.enums import TipoPerfil
from app.services.usuario_service import listar_usuarios, LIMITE_PADRAO, LIMITE_MAXIMO

def seed_usuarios(quantidade: int):
    """Popula o repositório em memória com usuários fictícios para teste."""
    # Limpa usuários existentes se houver
    usuario_repository._usuarios.clear()
    
    for i in range(quantidade):
        usuario = Usuario(
            id=uuid4(),
            nome=f"Usuario {i + 1}",
            email=f"usuario{i + 1}@exemplo.com",
            senha=f"senha_hash_{i + 1}",
            perfil=TipoPerfil.DISCENTE,
            ativo=True
        )
        usuario_repository.add(usuario)
    print(f"[OK] Repositorio populado com {quantidade} usuarios de teste.")

def testar_paginacao_padrao():
    print("\n--- Testando Paginacao Padrao (Limite Padrao = 50) ---")
    seed_usuarios(120)
    
    # Executa a listagem com os parâmetros padrão da rota
    resultado = listar_usuarios(pagina=1, limite=LIMITE_PADRAO)
    
    print(f"Total de usuarios no banco: {resultado.total} (Esperado: 120)")
    print(f"Pagina atual: {resultado.pagina} (Esperado: 1)")
    print(f"Limite por pagina: {resultado.limite} (Esperado: 50)")
    print(f"Quantidade retornada na pagina 1: {len(resultado.usuarios)} (Esperado: 50)")
    
    assert resultado.total == 120
    assert resultado.pagina == 1
    assert resultado.limite == 50
    assert len(resultado.usuarios) == 50
    print("[SUCCESS] Teste de paginacao padrao passou!")

def testar_paginacao_customizada():
    print("\n--- Testando Paginacao Customizada (Limite = 20) ---")
    seed_usuarios(35)
    
    # Testa página 1 com limite 20
    resultado_pag1 = listar_usuarios(pagina=1, limite=20)
    print(f"Pagina 1 - Retornou: {len(resultado_pag1.usuarios)} (Esperado: 20)")
    assert len(resultado_pag1.usuarios) == 20
    
    # Testa página 2 com limite 20 (deve retornar 15 usuários restantes)
    resultado_pag2 = listar_usuarios(pagina=2, limite=20)
    print(f"Pagina 2 - Retornou: {len(resultado_pag2.usuarios)} (Esperado: 15)")
    assert len(resultado_pag2.usuarios) == 15
    print("[SUCCESS] Teste de paginacao customizada passou!")

def testar_limite_maximo():
    print("\n--- Testando Limite Maximo Permitido (Maximo = 200) ---")
    seed_usuarios(250)
    
    # Solicita limite de 250, mas o serviço deve limitar a 200
    resultado = listar_usuarios(pagina=1, limite=250)
    print(f"Limite retornado/aplicado: {resultado.limite} (Esperado: 200)")
    print(f"Quantidade retornada na pagina: {len(resultado.usuarios)} (Esperado: 200)")
    
    assert resultado.limite == 200
    assert len(resultado.usuarios) == 200
    print("[SUCCESS] Teste de limite maximo passou!")

if __name__ == "__main__":
    try:
        testar_paginacao_padrao()
        testar_paginacao_customizada()
        testar_limite_maximo()
        print("\n[PASSED] Todos os testes de paginacao executados com sucesso!")
    except AssertionError as e:
        print(f"\n[FAILED] Falha em um dos testes (AssertionError). Verifique as validacoes.")
        sys.exit(1)
