from sqlalchemy import Column, String, BigInteger, DateTime, Text, Boolean
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


class Post(Base):
    __tablename__ = "posts"

    id = Column(BigInteger, primary_key=True)
    message_text = Column(Text, nullable=True)        # Описание или текст
    media_file_id = Column(String, nullable=True)     # file_id медиа
    media_type = Column(String, nullable=True)        # photo / video / document
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_sent = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Post(id={self.id}, created_at={self.created_at}, message_text={self.message_text})>"
