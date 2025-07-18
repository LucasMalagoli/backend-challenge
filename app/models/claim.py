from sqlalchemy import Column, String, BigInteger, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Claim(Base):
    __tablename__ = "claim"
    id = Column(BigInteger, primary_key=True, index=True)
    description = Column(String, nullable=False)
    active = Column(Boolean, default=True)

    user_claims = relationship("UserClaim", back_populates="claim", cascade="all, delete-orphan")
    users = relationship("User", secondary="user_claim", viewonly=True, back_populates="claims")
