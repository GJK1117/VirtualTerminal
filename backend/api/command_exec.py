from typing import List
from VirtualTerminal import settings
from api.command.command import Command

class Command_Exec:
    command: Command

    def __init__(self, command):
        self.command = command

    def execute(self, command_parts: List[str], allowed_commands: List[str], template=None):
        if command_parts[0] not in allowed_commands:
            return f"'{command_parts[0]}' 는 지원하지 않는 명령어 입니다."
        user = settings.get_user_instance()
        return self.command.execute_command(user, command_parts, template)