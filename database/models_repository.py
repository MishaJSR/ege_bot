from database.models import Users, Task, MediaBlockPool, MediaBlock, Block, MediaTask, UsersTaskProgress
from database.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = Users


class TaskRepository(SQLAlchemyRepository):
    model = Task


class BlockRepository(SQLAlchemyRepository):
    model = Block


class MediaBlockRepository(SQLAlchemyRepository):
    model = MediaBlock


class MediaBlockPoolRepository(SQLAlchemyRepository):
    model = MediaBlockPool


class MediaTaskRepository(SQLAlchemyRepository):
    model = MediaTask


class UsersTaskProgressRepository(SQLAlchemyRepository):
    model = UsersTaskProgress
