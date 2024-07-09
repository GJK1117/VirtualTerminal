import subprocess
from typing import List
from api.command.command import Command
from api.user import User

class Command_PWD(Command):
    def execute_command(self, user: User, command_parts: List[str], template=None) -> str:
        new_path: subprocess.CompletedProcess = subprocess.run(command_parts,
                                                             capture_output=True,
                                                             text=True,
                                                             shell=False
                                                             )
        new_path = new_path.stdout.strip()
        print(new_path)
        result = new_path.replace(user.temp_root_dir, '')  # 출력할 경로 설정
        return result