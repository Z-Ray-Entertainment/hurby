from character.character import Character
from twitch_hurby.cmd.abstract_command import AbstractCommand
from twitch_hurby.cmd.enums.cmd_response_realms import CMDResponseRealms
from twitch_hurby.cmd.enums.cmd_types import CMDType
from twitch_hurby.cmd.enums.permission_levels import PermissionLevels


class WhisperCommand(AbstractCommand):
    def __init__(self, json_data):
        trigger = json_data["cmd"]
        cmd_type = CMDType(json_data["type"])
        cmd_realm = CMDResponseRealms(json_data["realm"])
        cmd_perm = PermissionLevels(json_data["perm"])
        replies = json_data["reply"]
        description = json_data["description"]
        AbstractCommand.__init__(self, trigger, cmd_type, cmd_realm, replies, cmd_perm, description)

    def do_command(self, params: list, character: Character):
        pass
