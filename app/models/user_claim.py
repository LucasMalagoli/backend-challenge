from sqlalchemy import Column, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from app.database import Base


class UserClaim(Base):
    __tablename__ = 'user_claim'
    user_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    claim_id = Column(BigInteger, ForeignKey('claim.id'), primary_key=True)

    users = relationship("User", back_populates="user_claims")
    claim = relationship("Claim", back_populates="user_claims")
