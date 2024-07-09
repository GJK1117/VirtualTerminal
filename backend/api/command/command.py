from abc import abstractmethod, ABC
from typing import List
from api.user import User

class Command(ABC):
    @abstractmethod
    def execute_command(self, user: User, command_part: List[str], template=None) -> str:
        pass