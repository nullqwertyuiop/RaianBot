import ujson
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Dict

from .model import WeiboUser


class BaseWeiboData(metaclass=ABCMeta):
    followers: Dict[str, WeiboUser]
    mapping: Dict[str, str]

    def __init__(self, filepath: str):
        self.path = Path(filepath)

    @abstractmethod
    def load(self) -> None:
        ...

    @abstractmethod
    def save(self) -> None:
        ...


class DefaultWeiboData(BaseWeiboData):

    def load(self):
        if self.path.exists():
            with self.path.open('r+', encoding='UTF-8') as f_obj:
                _config = ujson.load(f_obj)
                self.mapping = _config['mapping']
                self.followers = {k: WeiboUser.parse_obj(v) for k, v in _config['weibo_follower'].items()}
        else:
            _config = {"weibo_follower": {}, "mapping": {}}
            with self.path.open('w+', encoding='UTF-8') as f_obj:
                ujson.dump(_config, f_obj, ensure_ascii=False)
                self.mapping = {}
                self.followers = {}

    def save(self):
        with self.path.open('w+', encoding='UTF-8') as f_obj:
            ujson.dump(
                {
                    "weibo_follower": {k: v.dict() for k, v in self.followers.items()},
                    "mapping": self.mapping
                }, f_obj, ensure_ascii=False, indent=4
            )
