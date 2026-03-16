from typing import Optional

from sqlmodel import Session, select

from app.models.user import UserModel


class UserRepository:
    def get_by_email(self, session: Session, email: str) -> Optional[UserModel]:
        stmt = select(UserModel).where(UserModel.email == email)
        return session.exec(stmt).first()

    def get_by_id(self, session: Session, user_id: int) -> Optional[UserModel]:
        return session.get(UserModel, user_id)

    def create(self, session: Session, *, email: str, hashed_password: str) -> UserModel:
        user = UserModel(email=email, hashed_password=hashed_password, is_active=True)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


user_repo = UserRepository()
