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
                    # 'cd /' 명령어가 입력된 경우 temp_root_dir로 이동
                    new_path = user.temp_root_dir
                elif target_dir == '~':
                    # 'cd ~' 명령어가 입력된 경우 temp_root_dir/home/username으로 이동
                    new_path = user.temp_home_dir
                else:
                    # 상대 경로나 다른 절대 경로가 입력된 경우
                    # os.path.join 함수는 입력된 경로들 중 가장 마지막에 위치한 절대 경로를 기준으로 그 이후의 경로들을 결합
                    # 인자가 절대경로, 절대경로 순서로 왔을 경우 마지막 절대경로가 반환됨(앞의 절대경로는 무시)
                    # 절대 경로는 파일 시스템의 루트 경로부터 시작하므로, 그 이후의 경로 결합은 의미가 없음 절대경로가 오면 다른 경로 무시
                    # 인자가 상대경로, 절대경로, 절대경로, 상대경로 순서로 올 경우 마지막 절대경로 + 상대경로로 결합됨
                    new_path = os.path.abspath(os.path.join(current_dir_path, target_dir))
                    if not new_path.startswith(user.temp_root_dir):
                        # 새로운 경로가 temp_root_dir 내에 있는지 확인
                        new_path =  user.temp_root_dir + new_path
            else:
                # 'cd' 명령어만 입력된 경우 홈 디렉토리로 이동
                new_path = user.temp_home_dir
            os.chdir(new_path)  # 디렉토리 변경
            output_path = '/' if new_path == user.temp_root_dir else new_path.replace(user.temp_home_dir, '~').replace(user.temp_root_dir, '')  # 출력할 경로 설정
            return f"Changed directory to {new_path}"

        except Exception as e:
            error_message = 'No such file or directory: ' + command_parts[1] + '\''
            return error_message