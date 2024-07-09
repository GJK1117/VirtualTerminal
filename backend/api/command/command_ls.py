import os
import subprocess
from typing import List
from api.command.command import Command
from api.user import User

class Command_LS(Command):
    def execute_command(self, user: User, command_parts: List[str], template=None) -> str:
        try:
            for i, part in enumerate(command_parts[1:]):
                if part.startswith('/'):
                    command_parts[i+1] = os.path.join(user.temp_root_dir, os.path.relpath(part, '/'))

            result: subprocess.CompletedProcess = subprocess.run(
                command_parts,
                capture_output=True,
                check=True,
                text=True,
            )

            return result.stdout.rstrip()
        
        except subprocess.CalledProcessError as e:
            return f"ls: '{command_parts[-1]}'에 접근할 수 없음: 그런 파일이나 디렉터리가 없습니다"