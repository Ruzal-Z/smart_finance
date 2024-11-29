from abc import ABC, abstractmethod


class AppSettingsServiceInterface(ABC):
    """Interface settings."""
    @abstractmethod
    def get_app_setting(self, key: str) -> str:
        """Obtaining settings."""
        raise NotImplementedError
    