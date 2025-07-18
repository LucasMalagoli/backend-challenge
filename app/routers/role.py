from app.models.role import Role
from app.schemas.role import RoleOut, RoleCreate, RoleUpdate
from app.database import get_db
from app.routers.crud_router import CRUDRouter

role_crud = CRUDRouter(
    model=Role,
    read_schema=RoleOut,
    create_schema=RoleCreate,
    update_schema=RoleUpdate,
    db_getter=get_db,
    prefix="/role",
    tags=["Role"],
)

role_crud.register_routes()
router = role_crud.router
