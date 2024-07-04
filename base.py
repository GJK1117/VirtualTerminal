import os
import subprocess
import tempfile
import shutil
from typing import List

username: str = 'user'
hostname: str = 'host'
output_path: str = '$ '  # 터미널에 출력될 경로
temp_root_dir: str
temp_home_dir: str

def inspect_path(input_path: str) -> str:
    # 절대 경로가 주어진 경우 temp_root_dir을 앞에 붙여 제한된 디렉토리 내로 경로를 고정
    if os.path.isabs(input_path):
        # 절대 경로가 주어진 경우 temp_root_dir을 앞에 붙여 제한된 디렉토리 내로 경로를 고정
        return os.path.join(temp_root_dir, os.path.relpath(input_path, '/'))
    return input_path

def execute_command(input_command: str, allowed_commands: List[str]) -> str:
    """
    명령어를 실행하고 결과를 반환

    - params:
        - command: 사용자가 입력한 명령어
        - allowed_commands: 허용된 명령어 목록
    """
    global output_path
    try:
        current_dir_path: str = os.getcwd()  # 현재 작업 디렉토리의 절대경로 문자열로 반환

        # 입력받은 명령어를 공백을 기준으로 나누어 리스트로 변환
        command_parts: List[str] = input_command.split(' ')

        # 허용된 명령어인지 확인
        if command_parts[0] not in allowed_commands:
            return f"'{command_parts[0]}' 는 지원하지 않는 명령어 입니다."
        # cd 명령어인 경우
        elif command_parts[0] == 'cd':
            return command_cd(command_parts, current_dir_path)
        else:
            for i, part in enumerate(command_parts):
                if part.startswith('/'):
                    command_parts[i] = inspect_path(part)

            print(command_parts)

            # 명령어 실행
            result: subprocess.CompletedProcess = subprocess.run(command_parts, capture_output=True, text=True)
            # 명령어 실행 결과가 정상이 아닌 경우 에러 메세지 리턴
            if result.returncode != 0:
                return f"Error: {result.stderr}"

            # 명령어 실행 결과가 정상인 경우 결과 리턴
            return result.stdout
    except Exception as e:
        return str(e)
    finally:
        output_path = os.getcwd() + ' $ '


def command_cd(command_parts, current_dir_path):
    """
    'cd' 명령어를 처리하고 디렉토리를 변경

    - params:
        - command_parts: 'cd' 명령어와 인자를 포함하는 리스트
        - current_dir_path: 현재 작업 디렉토리의 절대경로 문자열

    - return:
        - 명령어 실행 결과 문자열
    """
    global output_path
    if len(command_parts) > 1:
        target_dir = command_parts[1]
        if target_dir == '/':
            # 'cd /' 명령어가 입력된 경우 temp_root_dir로 이동
            new_path = temp_root_dir
        elif target_dir == '~':
            # 'cd ~' 명령어가 입력된 경우 temp_root_dir/home/username으로 이동
            new_path = temp_home_dir
        else:
            # 상대 경로나 다른 절대 경로가 입력된 경우
            # os.path.join 함수는 입력된 경로들 중 가장 마지막에 위치한 절대 경로를 기준으로 그 이후의 경로들을 결합
            # 인자가 절대경로, 절대경로 순서로 왔을 경우 마지막 절대경로가 반환됨(앞의 절대경로는 무시)
            # 절대 경로는 파일 시스템의 루트 경로부터 시작하므로, 그 이후의 경로 결합은 의미가 없음 절대경로가 오면 다른 경로 무시
            # 인자가 상대경로, 절대경로, 절대경로, 상대경로 순서로 올 경우 마지막 절대경로 + 상대경로로 결합됨
            new_path = os.path.abspath(os.path.join(current_dir_path, target_dir))
            if not new_path.startswith(temp_root_dir):
                # 새로운 경로가 temp_root_dir 내에 있는지 확인
                return f"{new_path} 경로는 허용되지 않습니다."

        # 작업 디렉토리를 새로운 경로로 변경
        os.chdir(new_path)
        output_path = os.getcwd() + ' $ '
        return f"Changed directory to {new_path}"
    else:
        # 인자가 없는 'cd' 명령어의 경우 temp_home_dir로 이동
        os.chdir(temp_home_dir)
        output_path = os.getcwd() + ' $ '
        return f"Changed directory to {temp_home_dir}"


def main():
    global output_path, temp_root_dir, temp_home_dir

    # 제한된 디렉토리 경로
    restricted_dir: str = "/Users/kojinhyeok/linuxApp"

    # 임시 디렉토리 생성
    if not os.path.exists(restricted_dir):
        os.makedirs(restricted_dir)

    temp_dir: str = tempfile.mkdtemp(prefix=username+'_', dir=restricted_dir)
    home_dir: str = os.path.join(temp_dir, "home", username)
    os.makedirs(home_dir)
    os.chdir(home_dir)

    temp_root_dir = os.path.abspath(temp_dir)
    temp_home_dir = home_dir

    print("종료하려면 'exit'을 입력")

    # 허용된 명령어 목록 정의
    allowed_commands: List[str] = ['ifconfig', 'ls', 'pwd', 'echo', 'cat', 'touch', 'mkdir', 'cd']

    try:
        while True:
            input_command: str = input(username + '@' + hostname + ':' + output_path)
            if input_command.lower() == 'exit':
                print("종료")
                break
            output: str = execute_command(input_command, allowed_commands)
            print(output)
    finally:
        # 임시 디렉토리 삭제
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    main()