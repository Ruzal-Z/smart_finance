from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from infrastructure.repositories.postgresql.models.user_profile import UserProfile

class UserProfileRepository:
    """
    Репозиторий для работы с таблицей профилей пользователей.

    Методы:
    - get_profile_by_user_id: Получение профиля по ID пользователя.
    - create_profile: Создание нового профиля.
    - update_profile: Обновление профиля.
    - delete_profile: Удаление профиля.
    """
    def __init__(self, db: AsyncSession):
        """
        Инициализация репозитория.
        
        :param db: Асинхронная сессия SQLAlchemy.
        """
        self.db = db

    async def get_profile_by_user_id(self, user_id: int) -> UserProfile | None:
        """
        Получение профиля по ID пользователя.

        :param user_id: Идентификатор пользователя.
        :return: Объект профиля или None, если не найден.
        """
        result = await self.db.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        return result.scalars().first()

    async def create_profile(self, profile: UserProfile) -> UserProfile:
        """
        Создание нового профиля.

        :param profile: Экземпляр модели UserProfile.
        :return: Созданный профиль.
        """
        self.db.add(profile)
        await self.db.commit()
        await self.db.refresh(profile)
        return profile

    async def update_profile(self, profile: UserProfile) -> UserProfile:
        """
        Обновление профиля.

        :param profile: Экземпляр модели UserProfile с обновленными данными.
        :return: Обновленный профиль.
        """
        await self.db.commit()
        await self.db.refresh(profile)
        return profile

    async def delete_profile(self, profile_id: int) -> None:
        """
        Удаление профиля по его ID.

        :param profile_id: Идентификатор профиля.
        """
        profile = await self.get_profile_by_user_id(profile_id)
        if profile:
            await self.db.delete(profile)
            await self.db.commit()
