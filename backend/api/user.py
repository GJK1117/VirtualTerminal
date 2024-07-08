import os
import tempfile

class User:

    def __init__(self, username, hostname):
        self.username: str = username
        self.hostname: str = hostname
        self.restricted_dir: str = "."
        self.temp_root_dir = os.path.abspath(tempfile.mkdtemp(prefix=username + '_', dir=self.restricted_dir))
        self.temp_home_dir = os.path.join(self.temp_root_dir, "home", username)
        os.makedirs(self.temp_home_dir)
        os.chdir(self.temp_home_dir)
        print(f"restricted dir: {os.path.abspath(self.restricted_dir)}")