from typing import Optional

import bcrypt
from flask_login import UserMixin
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Text

from settings import Base, Session_db


class Users(UserMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    sent_requests: Mapped[list["Friends"]] = relationship("Friends", foreign_keys="Friends.sender", back_populates="sender_user")
    received_requests: Mapped[list["Friends"]] = relationship("Friends", foreign_keys="Friends.recipient", back_populates="recipient_user")

    sent_messages: Mapped[list["Messages"]] = relationship("Messages", foreign_keys="Messages.sender", back_populates="sender_user")
    received_messages: Mapped[list["Messages"]] = relationship("Messages", foreign_keys="Messages.recipient", back_populates="recipient_user")

    def set_password(self, password: str):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Метод для перевірки пароля
    def check_password(self, password: str):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    def __repr__(self):
        return f"User: {self.username}"

    def to_json(self):
        return {"username": self.username, "email": self.email, 'id': self.id}

    @staticmethod
    def get(user_id):
        """ повинен бути методом классу, бо при пошуку ми оперуємо классами а не конкретними
        екземплярами."""        
        
        with Session_db() as conn:
            stmt = select(Users).where(Users.id == user_id)
            user = conn.scalar(stmt)
            return user if user else None

    @staticmethod
    def get_by_username(username):           
        with Session_db() as conn:
            stmt = select(Users).where(Users.username == username)
            user = conn.scalar(stmt)
            return user if user else None
    

# class Friends(Base):
#     __tablename__ = " friends"
#     id: Mapped[int] = mapped_column(primary_key=True)
    
#     sender : Mapped[int] = mapped_column(ForeignKey("users.id"))
#     recipient : Mapped[int] = mapped_column(ForeignKey("users.id"))
    
#     status : Mapped[bool] = mapped_column( default=False)

#     sender_user: Mapped["Users"] = relationship("Users", foreign_keys="Friends.sender", back_populates="sent_requests")
#     recipient_user: Mapped["Users"] = relationship("Users", foreign_keys="Friends.recipient", back_populates="received_requests")
    
#     @staticmethod
#     def _check_friend(user_sender, user_recip) -> bool:
#         with Session_db() as conn:
#             stmt = select(Friends).filter_by(sender = user_sender, recipient=user_recip)
#             request = conn.scalar(stmt)
#         return False if request else True
    
#     def check_friends(self, user_sender, user_recip):
#         return self._check_friend(user_sender, user_recip) and self._check_friend(user_recip, user_sender)
    
#     @staticmethod
#     def create_request(user_sender: Users, user_recip: Users):
#         with Session_db() as conn:
#             new_friend_request = Friends(sender = user_sender.id, recipient = user_recip.id, status = False)
#             conn.add(new_friend_request)
#             conn.commit()
        

# class Messages(Base):
#     __tablename__ = "messages"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     sender: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     recipient: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     message_text: Mapped[str] = mapped_column(Text)
#     status_check : Mapped[bool] = mapped_column( default=False)

#     sender_user: Mapped["Users"] = relationship("Users", foreign_keys="Messages.sender", back_populates="sent_messages")
#     recipient_user: Mapped["Users"] = relationship("Users", foreign_keys="Messages.recipient",
#                                                    back_populates="received_messages")
