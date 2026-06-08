# 📚 Monitorando

> **Monitorias e materiais: tudo em um só lugar!**

Monitorando é uma plataforma web centralizada de apoio acadêmico que conecta alunos, monitores e coordenadores em um único ecossistema — eliminando a dispersão de informações e tornando a gestão de monitorias eficiente, transparente e acessível.

---

## 📋 Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Motivação](#motivação)
- [Funcionalidades Principais](#funcionalidades-principais)
- [Usuários do Sistema](#usuários-do-sistema)
- [Documentação](#documentação)
- [Tecnologias](#tecnologias)
- [Como Executar](#como-executar)
- [Contribuindo](#contribuindo)

---

## Sobre o Projeto

O ambiente acadêmico sofre com a desorganização e a dispersão de informações sobre monitorias e tutorias — comunicações espalhadas por múltiplos canais informais, horários desatualizados e ausência de métricas centralizadas.

O **Monitorando** resolve esses problemas ao oferecer uma plataforma única onde:

- 🎓 **Alunos** encontram horários atualizados e acessam materiais de apoio com facilidade
- 🧑‍🏫 **Monitores** organizam atendimentos, registram demandas e compartilham conteúdo
- 📊 **Professores e Coordenadores** acompanham métricas reais e geram relatórios automáticos

---

## Motivação

Os principais gargalos identificados no cenário atual:

| Problema | Impacto |
|---|---|
| Informações dispersas em múltiplos canais | Dificuldade de acesso e desorganização |
| Horários desatualizados | Alunos sem suporte, monitores ociosos |
| Registro manual de atendimentos | Ineficiência operacional e erros |
| Materiais espalhados em plataformas diversas | Baixo aproveitamento do conteúdo |
| Ausência de métricas centralizadas | Gestão acadêmica sem embasamento |

O Monitorando transforma essa realidade ao **centralizar registros, métricas e cronogramas**, permitindo que todos os envolvidos foquem no desenvolvimento acadêmico, não na burocracia.

---

## Funcionalidades Principais

- 🔐 **Autenticação por perfil** — Acesso diferenciado para Aluno, Monitor e Coordenador/Professor
- 🗓️ **Visualização de horários** — Consulta de monitores e horários disponíveis por disciplina
- ✋ **Demonstração de interesse** — Alunos podem sinalizar interesse em sessões futuras
- ✅ **Confirmação de presença** — Check-in presencial via código gerado pelo monitor
- 📂 **Repositório de materiais** — Upload e download de slides, listas de exercícios e videoaulas
- 💬 **Chat** — Comunicação direta entre alunos e monitores para dúvidas pontuais
- 📈 **Relatórios automáticos** — Geração de gráficos e métricas de presença, cancelamentos e engajamento
- ⭐ **Favoritar monitorias** — Alunos podem salvar disciplinas de interesse

---

## Usuários do Sistema

### 🎓 Alunos
Estudantes regularmente matriculados que buscam apoio acadêmico complementar.

**Principais interações:**
- Pesquisar disciplinas e visualizar grade de horários
- Demonstrar interesse em sessões e confirmar presença via código
- Baixar materiais de estudo no repositório
- Tirar dúvidas pontuais via chat

---

### 🧑‍🏫 Monitores / Tutores
Estudantes designados oficialmente pela coordenação para auxiliar em uma disciplina específica.

**Principais interações:**
- Gerenciar grade de horários de atendimento
- Visualizar demanda de alunos interessados
- Gerar códigos de presença durante as sessões
- Fazer upload de materiais didáticos
- Responder dúvidas dos alunos via chat

---

### 🏛️ Professores e Coordenadores
Membros do corpo docente ou coordenadores com permissões administrativas globais ou por conjunto de disciplinas.

**Principais interações:**
- **Coordenadores:** Gestão de acessos — promover alunos a monitores e revogar vínculos
- **Professores:** Upload de materiais complementares e geração de relatórios automáticos com métricas de impacto


## Tecnologias

> ⚙️ *Esta seção será atualizada conforme as decisões técnicas do projeto forem definidas.*

---

## Como Executar

### Backend (API)

1. Acesse o diretório da API:
```bash
cd monitorando-api
```

2. Crie e ative um ambiente virtual:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o servidor de desenvolvimento:
```bash
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`
A documentação interativa (Swagger) estará disponível em: `http://localhost:8000/docs`
---

## Contribuindo

Este projeto é desenvolvido no contexto da disciplina **Métodos de Projeto de Software**.

Para contribuir:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/minha-feature`)
3. Faça commit das suas alterações (`git commit -m 'feat: adiciona minha feature'`)
4. Envie para a branch (`git push origin feature/minha-feature`)
5. Abra um Pull Request

---

<div align="center">
  <sub>Desenvolvido como parte da disciplina Métodos de Projeto de Software</sub>
</div>