from core.database.models.default import DefaultModel
from core.database.models.roles import Role

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(DefaultModel):
    __tablename__ = "users"

    firstname = Column(String, nullable=False)

    lastname = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    telephone = Column(String, nullable=True)

    password = Column(String, nullable=False)

    role = Column(String, nullable=False, default=Role.USER.value)

    reports = relationship("Report", back_populates="user")

    occurrences = relationship("Occurrence", back_populates="users")
