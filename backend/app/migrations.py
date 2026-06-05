from sqlalchemy import inspect, text

from .database import engine
from . import models


def upgrade_schema():
    """Aplica migrações incrementais em SQLite (create_all + ALTER TABLE)."""
    models.Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    if not inspector.has_table("mensalidades"):
        return

    cols = {c["name"] for c in inspector.get_columns("mensalidades")}

    with engine.begin() as conn:
        if "matricula_id" not in cols:
            conn.execute(
                text("ALTER TABLE mensalidades ADD COLUMN matricula_id INTEGER REFERENCES matriculas(id)")
            )
