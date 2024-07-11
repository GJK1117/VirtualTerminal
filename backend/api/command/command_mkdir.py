import os
import subprocess
from typing import List
from api.command.command import Command
from api.user import User

class Command_MKDIR(Command):
    def execute_command(self, user: User, command_parts: List[str], template=None) -> str:
        for i, part in enumerate(command_parts):
            if part.startswith('/'):
                command_parts[i] = os.path.join(user.temp_root_dir, os.path.relpath(part, '/'))
            elif part.startswith('~'):
                    command_parts[i+1] = os.path.join(user.temp_home_dir, part[1:])
        try:
            subprocess.run(command_parts,
                           capture_output=True,
                           text=True,
                           shell=False
                           )
        except Exception as e:
            return 'Failed to make new directory'

        # return None
        return 'Made new directory'
