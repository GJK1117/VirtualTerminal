import os
import subprocess
import tempfile
import shutil
from typing import List, Dict
from abc import ABC, abstractmethod

class ShellState:
    def __init__(self, username: str, hostname: str):
        self.username: str = username
        self.hostname: str = hostname
        self.temp_root_dir: str = ''
        self.temp_home_dir: str = ''
        self.current_dir: str = ''
        self.output_path: str = ''

    def initialize_directories(self, restricted_dir: str):
        temp_dir: str = tempfile.mkdtemp(prefix=self.username+'_', dir=restricted_dir)
        self.temp_root_dir = os.path.abspath(temp_dir)
        self.temp_home_dir = os.path.join(self.temp_root_dir, "home", self.username)
        os.makedirs(self.temp_home_dir)
        self.current_dir = self.temp_home_dir
        self.output_path = '~'

    def set_output_path(self):
        if self.current_dir == self.temp_root_dir:
            self.output_path = '/'
        else:
            self.output_path = self.current_dir.replace(self.temp_home_dir, '~').replace(self.temp_root_dir, '')

    def get_prompt(self) -> str:
        return f"{self.username}@{self.hostname}:{self.output_path}$ "

class Command(ABC):
    @abstractmethod
    def execute(self, args: List[str], state: ShellState) -> str:
        pass

class CdCommand(Command):
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
    @staticmethod
    def get_command(command_name: str) -> Command:
        if command_name == 'cd':
            return CdCommand()
        else:
            return GenericCommand()

class ShellSimulator:
    def __init__(self, username: str, hostname: str):
        self.state = ShellState(username, hostname)
        self.allowed_commands: List[str] = ['dir', 'ifconfig', 'ls', 'pwd', 'echo', 'cat', 'touch', 'mkdir', 'cd']

    def run(self):
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