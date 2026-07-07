from fastapi import HTTPException
from typing import List
from app.models.disciplina import Disciplina, DisciplinaCadastro, DisciplinaResponse
from app.repositories.disciplina_repository import disciplina_repository

class DisciplinaService:
    def cadastrar_disciplina(self, cadastro: DisciplinaCadastro) -> Disciplina:
        # 1. Validar campos obrigatórios
        if (
            not cadastro.codigo
            or not cadastro.codigo.strip()
            or not cadastro.nome
            or not cadastro.nome.strip()
            or not cadastro.ementa
            or not cadastro.ementa.strip()
        ):
            raise HTTPException(
                status_code=400,
                detail="Preencha todos os campos obrigatórios para continuar"
            )

        codigo = cadastro.codigo.strip().upper()

        # 2. Validar se código já existe
        if disciplina_repository.find_by_codigo(codigo) is not None:
            raise HTTPException(
                status_code=400,
                detail="Já existe uma disciplina com este código."
            )

        # 3. Criar disciplina
        disciplina = Disciplina(
            codigo=codigo,
            nome=cadastro.nome.strip(),
            ementa=cadastro.ementa.strip(),
            periodo=cadastro.periodo
        )

        # 4. Salvar na coleção em memória
        disciplina_repository.add(disciplina)
        return disciplina

    def listar_disciplinas(self) -> List[DisciplinaResponse]:
        disciplinas_db = disciplina_repository.find_all()

        return [
            DisciplinaResponse(
                id=d.id,
                codigo=d.codigo,
                nome=d.nome,
                ementa=d.ementa,
                periodo=d.periodo
            )
            for d in disciplinas_db
        ]

disciplina_service = DisciplinaService()
