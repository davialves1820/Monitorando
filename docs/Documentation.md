# Documentação das Alterações do Modelo

## 1. Introdução

Este documento descreve as alterações realizadas no modelo de classes em relação à primeira versão. O objetivo das modificações foi incorporar funcionalidades de cadastro, consulta, validação e persistência de dados, tornando o modelo mais aderente às regras de negócio definidas para o sistema de monitoria.

---

# 2. Atualização do Diagrama de Classes

O diagrama de classes foi revisado para representar não apenas a estrutura das entidades do domínio, mas também seus comportamentos e responsabilidades.

A estrutura principal do sistema foi mantida, preservando a hierarquia de usuários e as entidades relacionadas à monitoria. Entretanto, foram adicionadas operações, restrições e responsabilidades que refletem funcionalidades efetivamente implementadas no sistema.

---

# 3. Alterações na Hierarquia de Usuários

## Estrutura Mantida

A hierarquia de herança permaneceu organizada da seguinte forma:

```text
Usuario
├── Discente
│   └── Monitor
└── Docente
```

A utilização de herança continua permitindo o compartilhamento dos atributos comuns entre os diferentes perfis do sistema.

---

## Classe Usuario

### Situação Anterior

Possuía apenas atributos básicos comuns a todos os usuários.

### Situação Atual

Foram adicionadas operações responsáveis pelo gerenciamento de usuários:

* cadastrar_usuario()
* listar_usuarios()
* buscar_usuario()

### Regras adicionadas

* Nome obrigatório.
* E-mail obrigatório.
* Senha obrigatória.
* Usuário ativo por padrão.
* E-mail único no sistema.

### Justificativa

Centralizar funcionalidades relacionadas à gestão de usuários e explicitar regras de negócio essenciais.

---

## Classe Discente

### Alterações

* Inclusão da operação de cadastro.
* Validação obrigatória de matrícula.
* Restrição de cadastro utilizando apenas e-mails do domínio:

```text
@discente.ufpb.br
```

### Justificativa

Garantir que apenas alunos vinculados à instituição possam acessar o sistema.

---

## Classe Docente

### Alterações

* Inclusão da operação de cadastro.
* Validação dos domínios institucionais:

```text
@ufpb.br
@ci.ufpb.br
```

### Justificativa

Restringir o acesso aos docentes vinculados à instituição.

---

## Classe Monitor

### Situação Anterior

Representava apenas uma especialização de Discente.

### Situação Atual

Foram adicionadas operações específicas para gerenciamento da monitoria:

* promover_usuario()
* revogar_monitor()

### Regras adicionadas

* Apenas discentes podem ser promovidos.
* Disciplina vinculada obrigatória.
* Disponibilidade inicial definida como verdadeira.
* Controle de carga horária.

### Justificativa

Representar explicitamente o ciclo de vida de um monitor dentro do sistema.

---

# 4. Alterações na Classe Disciplina

## Situação Anterior

A classe possuía apenas atributos descritivos.

## Situação Atual

Foram adicionadas operações para gerenciamento das disciplinas:

* cadastrar_disciplina()
* listar_disciplinas()

### Regras adicionadas

* Código obrigatório.
* Nome obrigatório.
* Ementa obrigatória.
* Código único.
* Conversão automática do código para letras maiúsculas.

### Justificativa

Garantir consistência dos dados e evitar duplicidade de disciplinas.

---

# 5. Revisão dos Relacionamentos

Os relacionamentos existentes foram mantidos e refinados para refletir melhor as responsabilidades das entidades.

## Principais associações

### Discente ↔ DisciplinaFavorita

Permite que um aluno registre disciplinas de interesse.

### Discente ↔ DemonstracaoInteresse

Representa o interesse de um aluno em participar de sessões de monitoria.

### Monitor ↔ SessaoMonitoria

Relaciona monitores às sessões realizadas.

### SessaoMonitoria ↔ Inscricao

Representa os alunos inscritos em uma sessão.

### SessaoMonitoria ↔ RegistroPresenca

Permite registrar presença dos participantes.

### Disciplina ↔ MaterialDidatico

Representa os materiais disponibilizados para determinada disciplina.

### Disciplina ↔ Chat

Permite comunicação entre os participantes da disciplina.

### Chat ↔ Mensagem

Representa as mensagens trocadas dentro de um chat.

---

# 6. Inclusão de Regras de Negócio no Modelo

Uma das principais evoluções do modelo foi a incorporação explícita de regras de negócio.

## Regras de Usuário

### Validação de E-mail Institucional

Discente:

```text
@discente.ufpb.br
```

Docente:

```text
@ufpb.br
@ci.ufpb.br
```

### Validação de E-mail Único

Não é permitido o cadastro de usuários com e-mails já existentes.

### Política de Senha

A senha deve:

* possuir entre 8 e 100 caracteres;
* conter pelo menos uma letra maiúscula;
* conter pelo menos um número.

---

## Regras de Disciplina

* Código único.
* Campos obrigatórios preenchidos.
* Padronização do código em letras maiúsculas.

---

## Regras de Monitoria

* Apenas discentes podem ser promovidos a monitor.
* Monitores devem possuir disciplina vinculada.
* Monitores podem retornar ao perfil de discente.

---

# 7. Alterações Arquiteturais

Além da atualização do modelo de domínio, foi introduzida uma arquitetura em camadas para separar responsabilidades.

## Camada de Modelo (Model)

Responsável pela representação das entidades do domínio:

* Usuario
* Discente
* Monitor
* Docente
* Disciplina
* SessaoMonitoria
* Inscricao
* entre outras.

## Camada de Serviço (Service)

Responsável pelas regras de negócio:

### UsuarioService

* cadastro de usuários;
* consultas;
* paginação;
* promoção de monitores;
* revogação de monitoria.

### DisciplinaService

* cadastro de disciplinas;
* listagem de disciplinas;
* validações de negócio.

## Camada de Persistência (Repository)

Responsável pelo armazenamento e recuperação dos dados.

### UsuarioRepository

* salvar usuários;
* atualizar usuários;
* buscar usuários;
* paginação e filtros.

### DisciplinaRepository

* salvar disciplinas;
* buscar disciplinas;
* listar disciplinas.

---

# 8. Conclusão

O modelo evoluiu significativamente em relação à versão anterior. Além da manutenção da estrutura principal do domínio, foram adicionadas operações, validações e responsabilidades que refletem funcionalidades efetivamente implementadas no sistema.

As alterações realizadas tornaram o modelo mais consistente, aproximando-o da implementação real da aplicação e estabelecendo uma base sólida para futuras funcionalidades relacionadas à monitoria acadêmica.
