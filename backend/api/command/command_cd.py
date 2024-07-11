import os
from typing import List
from api.command.command import Command
from api.user import User

class Command_CD(Command):

    def execute_command(self, user: User, command_parts: List[str], template=None) -> str:
        current_dir_path: str = os.getcwd()
        try:
            if len(command_parts) > 1:
                target_dir = command_parts[1]
                if target_dir == '/':
                    new_path = user.temp_root_dir
                elif target_dir == '~':
                    new_path = user.temp_home_dir
                else:
                    new_path = os.path.abspath(os.path.join(current_dir_path, target_dir))
                    if not new_path.startswith(user.temp_root_dir):
                        new_path = os.path.join(user.temp_root_dir, os.path.relpath(new_path, '/'))

            else:
                new_path = user.temp_home_dir

            os.chdir(new_path)

            output_path = '/' if new_path == user.temp_root_dir else new_path.replace(user.temp_home_dir, '~').replace(user.temp_root_dir, '')
            return f"Changed directory to {output_path}"
            
        except Exception as e:
            error_message = 'No such file or directory: ' + command_parts[1] + '\''
            return error_message