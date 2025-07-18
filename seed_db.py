from datetime import date
from app.database import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.claim import Claim


def seed():
    session = SessionLocal()
    try:
        admin_role = Role(description="Administrator")
        user_role = Role(description="Regular User")

        claim_read = Claim(description="Can read data")
        claim_write = Claim(description="Can write data")
        claim_delete = Claim(description="Can delete data")

        session.add_all([admin_role, user_role, claim_read, claim_write, claim_delete])
        session.commit()

        admin = User(
            name="admin",
            email="admin@example.com",
            password="GRzZ5nO0odsE",
            role=admin_role,
            created_at=date.today(),
            claims=[claim_read, claim_write, claim_delete]
        )
        user = User(
            name="Fulano Ciclano",
            email="fulano@example.com",
            password="XhmWU5cTn4C7",
            role=user_role,
            created_at=date.today(),
            claims=[claim_read]
        )

        session.add_all([admin, user])
        session.commit()

        print("Seeding complete!")

    except Exception as e:
        session.rollback()
        print("Error during seeding:", e)
    finally:
        session.close()


if __name__ == "__main__":
    seed()
