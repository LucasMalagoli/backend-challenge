from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.claim import Claim
from app.models.user_claim import UserClaim
from app.schemas.user import UserOut, UserCreate, UserUpdate
from app.database import get_db
from app.routers.crud_router import CRUDRouter


class UserCRUD(CRUDRouter):
    def create(self, item: UserCreate, db: Session = Depends(get_db)):  # type: ignore
        """
        Overrides the super method to handle creating user_claim instances.
        """
        claim_ids = item.claim_ids or []
        user_data = item.dict(exclude={"claim_ids"})

        existing_claims = db.query(Claim.id).filter(Claim.id.in_(claim_ids)).all()
        existing_claim_ids = {claim.id for claim in existing_claims}

        missing_claim_ids = set(claim_ids) - existing_claim_ids
        if missing_claim_ids:
            raise HTTPException(
                status_code=400,
                detail=f"Claims with IDs {list(missing_claim_ids)} do not exist."
            )

        user = User(**user_data)
        db.add(user)
        db.flush()

        for claim_id in claim_ids:
            user_claim = UserClaim(user_id=user.id, claim_id=claim_id)
            db.add(user_claim)

        db.commit()
        db.refresh(user)

        return user

    def _create(self):
        # Overriding for documentation purposes only
        result = super()._create()
        result.__doc__ = """
        <b>About creating claims while creating the user </b>:
        - To create any claims, first validate that they exist, then add it in a list.
            - Example: [1, 2, 3]
        - To avoid creating any claims, set claim_ids as an empty list or remove it.

        <b> About the password </b>:
        - If left empty, the server will generate a 12 characters using ASCII characters and digits.
        - The password will not be returned in the response for safety reasons.
        """
        return result


user_crud = UserCRUD(
    model=User,
    read_schema=UserOut,
    create_schema=UserCreate,
    update_schema=UserUpdate,
    db_getter=get_db,
    prefix="/user",
    tags=["User"],
)

user_crud.register_routes()
router = user_crud.router
