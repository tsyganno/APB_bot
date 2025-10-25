from sqlalchemy import Column, String, BigInteger, DateTime
from sqlalchemy.sql import func
from main_app.database.session import Base


# 👤 Пользователь
class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String, nullable=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username}, city={self.name})>"
