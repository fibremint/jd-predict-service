import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    email = sa.Column(sa.String, unique=True, index=True)
    hashed_password = sa.Column(sa.String)
