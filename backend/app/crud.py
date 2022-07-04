from sqlalchemy.orm import Session

from . import models, schemas


# TODO: implement password hashify function
def _password_hasify(password):
    return password + 'isNotHashedActually'


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_from_login(db: Session, email: str, password: str):
    return db.query(models.User) \
             .filter(models.User.email == email) \
             .filter(models.User.hashed_password == _password_hasify(password)) \
             .first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, hashed_password=_password_hasify(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user