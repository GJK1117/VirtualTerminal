import os
import subprocess
from typing import List
from api.command.command import Command
from api.user import User

class Command_MKDIR(Command):
    def execute_command(self, user: User, command_part: List[str], allowed_commands: List[str], template=None) -> str:
        for i, part in enumerate(command_part):
            if part.startswith('/'):
                command_part[i] = os.path.join(user.temp_root_dir, os.path.relpath(part, '/'))
        try:
            subprocess.run(command_part,
                           capture_output=True,
                           text=True,
                           shell=False
                           )
        except Exception as e:
            return 'Failed to make new directory'

        return 'Made new directory'
