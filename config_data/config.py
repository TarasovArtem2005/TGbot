from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    tocken: str
    admin_ids: list[int]

@dataclass
class Config:
    tg_bot: TgBot

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(
        tocken=env('BOT_TOKEN'),
        admin_ids=[int(i) for i in env.list('ADMIN_IDS')]
    ))
