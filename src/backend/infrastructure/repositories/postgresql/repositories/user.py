from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from src.backend.infrastructure.repositories.postgresql.models.user import User

class UserRepository:
    """
    Репозиторий для работы с таблицей пользователей.

    Методы:
    - get_user_by_id: Получение пользователя по ID.
    - get_user_by_email: Получение пользователя по email.
    - create_user: Создание нового пользователя.
    - update_user: Обновление данных пользователя.
    - delete_user: Удаление пользователя.
    """
    def __init__(self, db: AsyncSession):
        """
        Инициализация репозитория.
        
        :param db: Асинхронная сессия SQLAlchemy.
        """
        self.db = db

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Получение пользователя по его ID.

        :param user_id: Идентификатор пользователя.
        :return: Объект пользователя или None, если не найден.
        """
        result = await self.db.execute(
            select(User).where(User.id == user_id).options(joinedload(User.profile))
        )
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Получение пользователя по email.

        :param email: Email пользователя.
        :return: Объект пользователя или None, если не найден.
        """
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()

    async def create_user(self, user: User) -> User:
        """
        Создание нового пользователя.

        :param user: Экземпляр модели User.
        :return: Созданный пользователь.
        """
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user(self, user: User) -> User:
        """
        Обновление данных пользователя.

        :param user: Экземпляр модели User с обновленными данными.
        :return: Обновленный пользователь.
        """
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> None:
        """
        Удаление пользователя по его ID.

        :param user_id: Идентификатор пользователя.
        """
        user = await self.get_user_by_id(user_id)
        if user:
            await self.db.delete(user)
            await self.db.commit()
