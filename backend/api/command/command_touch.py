import os
import subprocess
from typing import List
from api.command.command import Command
from api.user import User

class Command_TOUCH(Command):
    def execute_command(self, user: User, command_parts: List[str], template=None) -> str:
        try:
            for i, part in enumerate(command_parts[1:]):
                if part.startswith('/'):
                    command_parts[i+1] = os.path.join(user.temp_root_dir, os.path.relpath(part, '/'))
                elif part.startswith('~'):
                    command_parts[i+1] = os.path.join(user.temp_home_dir, part[1:])

            result: subprocess.CompletedProcess = subprocess.run(
                command_parts,
                capture_output=True,
                check=True,
                text=True,
            )

            # return None
            return f"file created"
                
        except subprocess.CalledProcessError as e:
            file_path = None
            for part in command_parts:
                if not part.startswith('-') and not part.startswith('/'):
                    file_path = part
                    break

            if not file_path:
                file_path = command_parts[-1]

            return f"touch: '{file_path}'에 touch 명령 실행 불가: 그런 파일이나 디렉터리가 없습니다"