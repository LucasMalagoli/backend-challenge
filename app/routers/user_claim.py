from app.models.user_claim import UserClaim
from app.schemas.user_claim import UserClaimOut, UserClaimCreate, UserClaimUpdate
from app.database import get_db
from app.routers.crud_router import CRUDRouter

user_claim_crud = CRUDRouter(
    model=UserClaim,
    read_schema=UserClaimOut,
    create_schema=UserClaimCreate,
    update_schema=UserClaimUpdate,
    db_getter=get_db,
    prefix="/user_claim",
    tags=["UserClaim"],
)

user_claim_crud.register_routes()
router = user_claim_crud.router
