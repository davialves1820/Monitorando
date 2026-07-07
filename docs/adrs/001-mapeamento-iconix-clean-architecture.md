# ADR 001: Mapeamento dos Estereótipos ICONIX (Análise Robusta) para a Clean Architecture

**Data:** 2026-07-06  
**Status:** Aceito

## 1. Contexto

O enunciado do projeto e as diretrizes de avaliação (baseadas no processo ICONIX e Análise Robusta) solicitam explicitamente a utilização e identificação de três tipos de objetos/camadas clássicas: **Fronteira** (Boundary), **Controle** (Control) e **Entidade** (Entity).

No entanto, a implementação do sistema evoluiu para uma estrutura inspirada na **Clean Architecture** (ou arquitetura em camadas/cebola), utilizando nomenclatura padrão de mercado para APIs modernas em FastAPI, organizada nos diretórios `routers`, `services`, `models` e `repositories`. 

Esta abordagem foi adotada por ser arquitetonicamente superior no contexto de APIs web, garantindo alta testabilidade, baixo acoplamento e forte aderência aos princípios SOLID (especialmente o Princípio da Inversão de Dependência - DIP, implementado via injeção de repositórios). Renomear os diretórios e arquivos literais do projeto para "fronteira", "controle" e "entidade" causaria estranheza técnica e desvio dos padrões adotados pela comunidade Python/FastAPI, sem agregar valor técnico real ao software.

## 2. Decisão

Decidimos **manter a nomenclatura atual** da Clean Architecture (`routers`, `services`, `models`, `repositories`) no código-fonte, optando por **formalizar o mapeamento conceitual** destas camadas para os estereótipos da Análise Robusta do ICONIX através deste documento (ADR). 

Dessa forma, cumprimos os requisitos do enunciado ao demonstrar a clara separação de responsabilidades exigida pelos estereótipos, mantendo um código limpo, idiomático e com arquitetura escalável.

## 3. Mapeamento Arquitetural (ICONIX ↔ Clean Architecture)

A correspondência de 1 para 1 entre a exigência do enunciado e nossa arquitetura é a seguinte:

### 🎭 Fronteira (Boundary) ➔ `app/routers/`
Os objetos de fronteira são responsáveis pela interface com o mundo exterior. 
- Na nossa API, os **Routers** (endpoints FastAPI) assumem exatamente este papel. 
- Eles recebem as requisições HTTP, realizam a validação sintática da entrada (via Pydantic), formatam a saída (JSON) e delegam o trabalho real para a camada de controle. Não possuem regras de negócio.

### ⚙️ Controle (Control) ➔ `app/services/` e `app/controllers/`
Os objetos de controle orquestram a lógica do negócio, conectando a fronteira com as entidades e decidindo "o que fazer".
- No nosso sistema, os **Services** (`DisciplinaService`, `UsuarioService`, `InscricaoMonitoriaService`) contêm os casos de uso e as validações de domínio (ex: checar relacionamentos, regras de horários, regras de senhas).
- O `FacadeSingletonController` também age como um orquestrador de alto nível (Controle).

### 📦 Entidade (Entity) ➔ `app/models/` e `app/repositories/`
Os objetos de entidade representam a informação persistente do sistema e as regras de domínio intrínsecas aos dados.
- Os **Models** (`InscricaoMonitoria`, `Usuario`, etc.) definem a estrutura e os tipos de dados do domínio.
- Os **Repositories** (`abstract_*_repository.py`, implementações SQLite e InMemory) representam o acesso e a manipulação direta dessas entidades no armazenamento, encapsulando a complexidade de persistência.

## 4. Consequências

- **Positivas:** A base de código mantém-se alinhada com as melhores práticas da indústria para microsserviços e APIs web (SOLID, DIP, Injeção de Dependência). O projeto ganha flexibilidade (como a troca instantânea entre banco SQLite e armazenamento em RAM demonstrada no código).
- **Negativas:** Os avaliadores precisarão referenciar este documento para validar o cumprimento direto do requisito de "Fronteira/Controle/Entidade", já que os nomes não estão literais nas pastas do projeto.
