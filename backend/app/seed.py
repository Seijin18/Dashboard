import os
from sqlalchemy.orm import Session
from . import models
from .auth_utils import hash_password


def seed_defaults(db: Session):
    if not db.query(models.Associacao).filter(models.Associacao.slug == "kannon-do").first():
        assoc = models.Associacao(nome="Kannon Do", slug="kannon-do")
        db.add(assoc)
        db.commit()
        db.refresh(assoc)
    else:
        assoc = db.query(models.Associacao).filter(models.Associacao.slug == "kannon-do").first()

    if not db.query(models.Modalidade).filter(models.Modalidade.slug == "judo").first():
        db.add(models.Modalidade(
            associacao_id=assoc.id,
            nome="Judô",
            slug="judo",
            ativa=True,
        ))
        db.commit()

    if not db.query(models.Modalidade).filter(models.Modalidade.slug == "yoga").first():
        db.add(models.Modalidade(
            associacao_id=assoc.id,
            nome="Yoga",
            slug="yoga",
            ativa=True,
        ))
        db.commit()

    admin_email = os.getenv("ADMIN_EMAIL", "admin@kannondo.local")
    if not db.query(models.User).filter(models.User.email == admin_email).first():
        db.add(models.User(
            email=admin_email,
            hashed_password=hash_password(os.getenv("ADMIN_PASSWORD", "admin123")),
            role="admin",
        ))
        db.commit()
