from typing import Annotated, List, Optional
from fastapi import Depends, FastAPI, HTTPException, Query, APIRouter
from sqlmodel import Field, Session, SQLModel, create_engine, select
from uuid import uuid3, NAMESPACE_DNS

from ..models.user import UserCreate, UserPublic, User, UserUpdate
from ..db import SessionDep

router = APIRouter(
    prefix="/customer_service",
    tags=["customer_service"]
)


@router.post("/users/", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep):
    db_user = User.model_validate(user)
    db_user.uuid = uuid3(NAMESPACE_DNS, db_user.email)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/users/", response_model=list[UserPublic])
def read_users(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.get("/users/{user_uuid}", response_model=UserPublic)
def read_user(user_uuid: str, session: SessionDep):
    user = session.exec(select(User).where(User.uuid == user_uuid)).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_uuid}", response_model=UserPublic)
def replace_or_create_user(user_uuid: str, user: UserCreate, session: SessionDep):
    db_user = session.exec(select(User).where(User.uuid == user_uuid)).one_or_none()

    if db_user:
        # Updating existing user
        user_data = user.model_dump()
        for key, value in user_data.items():
            setattr(db_user, key, value)
    else:
        # creating new user
        db_user = User(uuid=uuid3(NAMESPACE_DNS, user.email), **user.model_dump())
        session.add(db_user)

    session.commit()
    session.refresh(db_user)
    return db_user


@router.patch("/users/{user_uuid}", response_model=UserPublic)
def update_user(user_uuid: str, user: UserUpdate, session: SessionDep):
    db_user = session.exec(select(User).where(User.uuid == user_uuid)).one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/users/{user_uuid}")
def delete_user(user_uuid: str, session: SessionDep):
    user = session.exec(select(User).where(User.uuid == user_uuid)).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}
