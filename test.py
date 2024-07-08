import os
import subprocess
import tempfile
import shutil
from typing import List, Dict
from abc import ABC, abstractmethod

class ShellState:
    """
    Shell의 상태 관리

    Attributes
    ----------
    username : str
        사용자 이름
    hostname : str
        호스트 이름
    temp_root_dir : str
        임시 루트 디렉토리 경로
    temp_home_dir : str
        임시 홈 디렉토리 경로
    current_dir : str
        현재 작업 디렉토리 경로
    output_path : str
        출력될 경로 문자열

    Methods
    -------
    initialize_directories(restricted_dir: str)
        임시 디렉토리를 초기화하고 생성
    set_output_path()
        현재 디렉토리를 기반으로 출력 경로 설정
    get_prompt() -> str
        현재 상태를 기반으로 prompt 문자열 반환
    """
    def __init__(self, username: str, hostname: str):
        self.username: str = username
        self.hostname: str = hostname
        self.temp_root_dir: str = ''
        self.temp_home_dir: str = ''
        self.current_dir: str = ''
        self.output_path: str = ''

    def initialize_directories(self, restricted_dir: str):
        """
        임시 디렉토리 초기화 및 생성

        Parameters
        ----------
        restricted_dir : str
            임시 디렉토리가 생성될 제한된 디렉토리 경로
        """
        temp_dir: str = tempfile.mkdtemp(prefix=self.username+'_', dir=restricted_dir)
        self.temp_root_dir = os.path.abspath(temp_dir)
        self.temp_home_dir = os.path.join(self.temp_root_dir, "home", self.username)
        os.makedirs(self.temp_home_dir)
        self.current_dir = self.temp_home_dir
        self.output_path = '~'

    def set_output_path(self):
        """
        현재 디렉토리를 기반으로 출력 경로 설정
        """
        if self.current_dir == self.temp_root_dir:
            self.output_path = '/'
        else:
            self.output_path = self.current_dir.replace(self.temp_home_dir, '~').replace(self.temp_root_dir, '')

    def get_prompt(self) -> str:
        """
        현재 상태를 기반으로 프롬프트 문자열 반환

        Returns
        -------
        str
            현재 사용자와 경로를 포함한 프롬프트 문자열
        """
        return f"{self.username}@{self.hostname}:{self.output_path}$ "

class Command(ABC):
    """
    모든 명령어 class가 상속받아야 할 기본 클래스 정의

    Methods
    -------
    execute(args: List[str], state: ShellState) -> str
        명령어를 실행하고 결과를 반환하는 추상 메소드
    """
    @abstractmethod
    def execute(self, args: List[str], state: ShellState) -> str:
        pass

class CdCommand(Command):
    """
    'cd' 명령어를 처리 class

    Methods
    -------
    execute(args: List[str], state: ShellState) -> str
        'cd' 명령어를 실행하고 결과 반환
    """
    def execute(self, args: List[str], state: ShellState) -> str:
        if len(args) > 1:
            target_dir = args[1]
            if target_dir == '/':
                new_path = state.temp_root_dir
            elif target_dir == '~':
                new_path = state.temp_home_dir
            else:
                new_path = os.path.abspath(os.path.join(state.current_dir, target_dir))
                if not new_path.startswith(state.temp_root_dir):
                    return f"{new_path} 경로는 허용되지 않습니다."
        else:
            new_path = state.temp_home_dir

        os.chdir(new_path)
        state.current_dir = new_path
        state.set_output_path()
        return f"Changed directory to {new_path}"

class GenericCommand(Command):
    """
    'cd' 이외의 명령어를 처리하는 class

    Methods
    -------
    execute(args: List[str], state: ShellState) -> str
        일반 명령어를 실행하고 결과를 반환함
    """
    def execute(self, args: List[str], state: ShellState) -> str:
        try:
            for i, part in enumerate(args):
                if part.startswith('/'):
                    args[i] = os.path.join(state.temp_root_dir, os.path.relpath(part, '/'))
            
            result: subprocess.CompletedProcess = subprocess.run(args, 
                                                                 capture_output=True, 
                                                                 text=True,
                                                                 shell=False,
                                                                #  executable="/bin/bash",
                                                                 )
            if result.returncode != 0:
                return f"Error: {result.stderr}"
            else:
                return result.stdout
        except Exception as e:
            return str(e)

class CommandFactory:
    """
    명령어 이름에 따라 적절한 Command 객체를 생성함

    Methods
    -------
    get_command(command_name: str) -> Command
        명령어 이름을 받아 적절한 Command 객체를 반환함
    """
    @staticmethod
    def get_command(command_name: str) -> Command:
        if command_name == 'cd':
            return CdCommand()
        else:
            return GenericCommand()

class ShellSimulator:
    """
    Shell simulator 실행

    Attributes
    ----------
    state : ShellState
        쉘의 현재 상태를 관리하는 ShellState 객체
    allowed_commands : List[str]
        허용된 명령어 리스트

    Methods
    -------
    run()
        쉘 시뮬레이터를 실행하고 명령어 입력을 처리함
    execute_command(input_command: str) -> str
        입력된 명령어를 실행하고 결과를 반환함
    """
    def __init__(self, username: str, hostname: str):
        self.state = ShellState(username, hostname)
        self.allowed_commands: List[str] = ['dir', 'ifconfig', 'ls', 'pwd', 'echo', 'cat', 'touch', 'mkdir', 'cd']

    def run(self):
        """
        쉘 시뮬레이터를 실행하고 명령어 입력을 처리함
        """
        restricted_dir: str = "."
        self.state.initialize_directories(restricted_dir)

        print(f"Temporary Home Directory: {self.state.temp_home_dir}")
        print(f"Temporary Root Directory: {self.state.temp_root_dir}")
        print("종료하려면 'exit'을 입력")

        try:
            while True:
                input_command: str = input(self.state.get_prompt())
                if input_command.lower() == 'exit':
                    print("종료")
                    break
                output: str = self.execute_command(input_command)
                print(output)
        finally:
            shutil.rmtree(self.state.temp_root_dir)

    def execute_command(self, input_command: str) -> str:
        """
        입력된 명령어를 실행하고 결과를 반환함

        Parameters
        ----------
        input_command : str
            사용자가 입력한 명령어 문자열

        Returns
        -------
        str
            명령어 실행 결과 문자열 또는 에러 메세지
        """
        command_parts: List[str] = input_command.split()
        if not command_parts:
            return ""
        
        command_name = command_parts[0]
        if command_name not in self.allowed_commands:
            return f"'{command_name}' 는 지원하지 않는 명령어 입니다."
        
        command = CommandFactory.get_command(command_name)
        return command.execute(command_parts, self.state)

if __name__ == "__main__":
    simulator = ShellSimulator('tmp', 'host')
    simulator.run()
