from api.command.command_cd import Command_CD
from api.command.command_mkdir import Command_MKDIR
from api.command.command_pwd import Command_PWD
from api.command.command_ls import Command_LS
from api.command.command_touch import Command_TOUCH

COMMAND_DICT = {
    'cd': Command_CD(),
    'pwd': Command_PWD(),
    'mkdir': Command_MKDIR(),
    'ls': Command_LS(),
    'touch': Command_TOUCH(),
}