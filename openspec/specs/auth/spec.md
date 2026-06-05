# Authentication

## Requirements

### Requirement: Login JWT

O sistema DEVE autenticar utilizadores via email/password e retornar token JWT.

#### Scenario: Login válido

- **GIVEN** utilizador admin existente
- **WHEN** POST `/auth/login` com credenciais correctas
- **THEN** retorna `access_token`

### Requirement: Proteção de escrita

Rotas de criação/edição DEEM exigir role admin.

#### Scenario: Criar modalidade sem token (auth activo)

- **GIVEN** `DISABLE_AUTH=false`
- **WHEN** POST `/modalidades/` sem Authorization
- **THEN** retorna 401
