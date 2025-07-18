from app.models.claim import Claim
from app.schemas.claim import ClaimOut, ClaimCreate, ClaimUpdate
from app.database import get_db
from app.routers.crud_router import CRUDRouter

claim_crud = CRUDRouter(
    model=Claim,
    read_schema=ClaimOut,
    create_schema=ClaimCreate,
    update_schema=ClaimUpdate,
    db_getter=get_db,
    prefix="/claim",
    tags=["Claims"],
)

claim_crud.register_routes()
router = claim_crud.router
