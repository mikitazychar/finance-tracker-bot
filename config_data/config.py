from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    """
    Хранит настройки подключения к Telegram API

    Attributes:
        token (str): Токен бота, полученный от @BotFather.
    """
    token: str


@dataclass
class Config:
    """
    Главный объект конфигурации, объединяющий все подсистемы приложения.

    Attributes:
        tg_bot (TgBot): Настройки для работы Telegram-бота.
    """
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    """
    Читает переменные окружения и возвращает заполненный объект Config.

    Этот метод инициализирует библиотеку environs, загружает данные из файла .env
    и маппит их на структуру dataclasses.

    Args:
        path (str | None): Путь к файлу .env. Если None, ищется файл .env
            в корневой директории проекта.

    Returns:
        Config: Экземпляр конфигурации, готовый к использованию в приложении.

    Raises:
        environs.EnvError: Если обязательная переменная (например, BOT_TOKEN)
            отсутствует в окружении.
    """
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')
        )
    )
