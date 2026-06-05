from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth_utils import require_admin
from .. import models
from ..services.migration import migrate_alunos_to_domain

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/migrate-legacy")
def run_migration(
    db: Session = Depends(get_db),
    _: models.User = Depends(require_admin),
):
    return migrate_alunos_to_domain(db)
