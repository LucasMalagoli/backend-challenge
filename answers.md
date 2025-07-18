# Respostas ao Desafio Backend

## Reflexão sobre o projeto

Foi muito interessante aprender a lidar com **FastAPI** e o ORM do **SQLAlchemy**, visto que minha experiência anterior é com **Django**. Acabei transferindo algumas ideias, como a criação de um roteador genérico para simular o que o `ModelViewSet` fazia no Django Rest Framework.

Cogitei fazer esse projeto em Django para entregar mais funcionalidades, mas optei por usar FastAPI para adquirir esse novo aprendizado.

Gostaria de ter tido mais tempo para trabalhar no repositório, implementar testes, pesquisar e desenvolver um sistema de login que desse sentido ao usuário, armazenar as senhas como hash e fazer o deploy na nuvem.

---

## 1. Consulta SQL

```sql
SELECT 
    u.name, 
    u.email, 
    r.description AS role_desc, 
    c.description AS claim_desc
FROM 
    users u
JOIN 
    roles r ON r.id = u.role_id
JOIN 
    user_claims uc ON uc.user_id = u.id
JOIN 
    claims c ON c.id = uc.claim_id
WHERE 
    c.active = true
ORDER BY 
    u.id, 
    role_desc, 
    claim_desc;
```

---

## 2. Consultas com SQLAlchemy ORM

Optei pelo **SQLAlchemy ORM**, apresentando duas soluções, supondo que `db` é um objeto Session:

### Consulta explícita

Retorna apenas as colunas selecionadas, como uma linha de resultado SQL:

```python
db.query(
    User.name,
    User.email,
    Claim.description.label("claim_desc"),
    Role.description.label("role_desc")
).join(
    User.role
).join(
    User.claims
).filter(
    Claim.active
)
```

### Consulta complexa

Retorna objetos mapeados com relacionamentos:

```python
from sqlalchemy.orm import load_only, joinedload

db.query(User).options(
    load_only(User.name, User.email),
    joinedload(User.role).load_only(Role.description),
    joinedload(User.claims).load_only(Claim.description)
).filter(
    Claim.active
)
```

---

## 6. Sobre o atributo `WALLET_X_TOKEN_MAX_AGE`

O arquivo `settings` dentro da pasta `core` **não possui** o atributo `WALLET_X_TOKEN_MAX_AGE`. Dependendo do contexto, este atributo pode estar vazio, sem definição ou simplesmente não estar presente.

---

## 7. Code Review

O código está disponível para revisão no link:

[https://github.com/LucasMalagoli/backend-challenge/pull/1/files](https://github.com/LucasMalagoli/backend-challenge/pull/1/files)

---

## 8. Padrão Adapter para envio de emails

É possível criar uma interface comum para envio de emails, implementando um Adapter para cada serviço de email. Para facilitar a usabilidade, podemos usar uma Factory que instancia o Adapter correto conforme o serviço desejado.

Exemplo em Python:

```python
class IEmailService:
    def send_email(self, to, subject, body): 
        pass


class EmailService1(IEmailService):
    def send_email(self, to, subject, body):
        # traduz para API do serviço 1
        pass


class EmailService2(IEmailService):
    def send_email(self, to, subject, body):
        # traduz para API do serviço 2
        pass


class EmailServiceFactory:
    @staticmethod
    def create(service_name):
        if service_name == "service_1":
            return EmailService1()
        elif service_name == "service_2":
            return EmailService2()
        else:
            raise ValueError("Unknown service")


email_service = EmailServiceFactory.create("service_2")
email_service.send_email("user@example.com", "Hello!", "Test message")
```