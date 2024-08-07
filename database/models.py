from abc import ABC, abstractmethod

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, func, Integer, Boolean, BigInteger


class Base(DeclarativeBase):
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class BlockPool(Base):
    __tablename__ = 'block_pool'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    block_main_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    has_media: Mapped[bool] = mapped_column(Boolean, nullable=False)


class Task(Base):
    __tablename__ = 'task'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    answer_mode: Mapped[str] = mapped_column(String(20), nullable=False)
    answers: Mapped[str] = mapped_column(Text, nullable=True)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    about: Mapped[str] = mapped_column(Text, nullable=True)
    addition: Mapped[str] = mapped_column(Text, nullable=True)
    points_for_task: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    is_visible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class Block(Base):
    __tablename__ = 'block'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    block_name: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    has_media: Mapped[bool] = mapped_column(Boolean, nullable=False)
    date_to_post: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    progress_block: Mapped[int] = mapped_column(Integer, default=0)
    callback_button_id: Mapped[str] = mapped_column(Text, nullable=True)
    count_send: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_vebinar: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_sub_block: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_visible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class MediaBlock(Base):
    __tablename__ = 'media_block'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    photo_id: Mapped[str] = mapped_column(Text, nullable=True)
    video_id: Mapped[str] = mapped_column(Text, nullable=True)


class MediaBlockPool(Base):
    __tablename__ = 'media_block_pool'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    block_pool_id: Mapped[int] = mapped_column(Integer, nullable=False)
    photo_id: Mapped[str] = mapped_column(Text, nullable=True)
    video_id: Mapped[str] = mapped_column(Text, nullable=True)


class MediaTask(Base):
    __tablename__ = 'media_task'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(Integer, nullable=False)
    photo_id: Mapped[str] = mapped_column(Text, nullable=False)


class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str] = mapped_column(Text, nullable=False)
    user_tag: Mapped[str] = mapped_column(Text, nullable=True)
    user_class: Mapped[str] = mapped_column(Text, nullable=False)
    user_become_children: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    parent_id: Mapped[int] = mapped_column(Integer, nullable=True)
    progress: Mapped[int] = mapped_column(Integer, default=0)
    name_of_user: Mapped[str] = mapped_column(Text, nullable=True)
    stop_spam: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    user_block_bot: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    id_last_block_send: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_subscribe: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    phone_number: Mapped[str] = mapped_column(Text, nullable=True)
    user_callback: Mapped[str] = mapped_column(Text, nullable=True)
    day_start_subscribe: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    day_end_subscribe: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class UsersTaskProgress(Base):
    __tablename__ = 'users_task_progress'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str] = mapped_column(Text, nullable=False)
    block_id: Mapped[int] = mapped_column(Integer, nullable=False)
    task_id: Mapped[int] = mapped_column(Integer, nullable=False)
    answer_mode: Mapped[str] = mapped_column(String(20), nullable=False)
    result: Mapped[str] = mapped_column(Text, nullable=False)
    is_pass: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
