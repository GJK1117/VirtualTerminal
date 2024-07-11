import os
import subprocess
from typing import List
from api.command.command import Command
from api.user import User
import glob

class Command_LS(Command):
    def execute_command(self, user: User, command_parts: List[str], template=None) -> str:
        try:
            updated_command_parts = [command_parts[0]]

            for part in command_parts[1:]:
                if part.startswith('/'):
                    part = os.path.join(user.temp_root_dir, os.path.relpath(part, '/'))
                elif part.startswith('~'):
                    part = os.path.join(user.temp_home_dir, part[1:])

                expanded_parts = glob.glob(part)
                if expanded_parts:
                    updated_command_parts.extend(expanded_parts)
                else:
                    updated_command_parts.append(part)

            result: subprocess.CompletedProcess = subprocess.run(
                updated_command_parts,
                capture_output=True,
                check=True,
                text=True,
            )

            return result.stdout.rstrip()

        except subprocess.CalledProcessError as e:
            file_path = None
            for part in command_parts:
                if not part.startswith('-') and not part.startswith('/'):
                    file_path = part
                    break

            if not file_path:
                file_path = command_parts[-1]

            return f"ls: '{file_path}'에 접근할 수 없음: 그런 파일이나 디렉터리가 없습니다"
