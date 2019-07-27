from config.bot_config import BotConfig
from twitch_hurby.cmd import simple_response
from twitch_hurby.cmd.actions.search_command import SearchCommand
from twitch_hurby.cmd.actions.shutdown_command import ShutdownCommand
from twitch_hurby.cmd.actions.whisper_command import WhisperCommand
from twitch_hurby.cmd.enums.cmd_types import CMDType
from utils import logger


class CMDLoader:
    def __init__(self):
        pass

    def create_cmd(self, json_data, bot_config: BotConfig, hurby):
        cmd_type = CMDType(json_data["type"])

        if cmd_type == CMDType.REPLY:
            # Logger.log(Logger.INFO, "CMD: " + json["cmd"] + " is SimpleReply")
            simpleCMD = simple_response.SimpleResponse(json_data, hurby)
            return simpleCMD
        elif cmd_type == CMDType.ACTION:
            if json_data["minigame"]:
                if bot_config.modules[bot_config.MODULE_MINIGAME] == "enabled":
                    pass
                    # Logger.log(Logger.INFO, "CMD: " + json["cmd"] + " is Mini game")
                else:
                    pass
                    # Logger.log(Logger.INFO, "Skip mini game: " + json["cmd"] + " mini games are disabled")
            else:
                logic_trigger = json_data["reply"]
                if logic_trigger == "$search":
                    return SearchCommand(json_data, hurby)
                if logic_trigger == "$whisper":
                    return WhisperCommand()
                if logic_trigger == "$shutdown":
                    return ShutdownCommand()
                if logic_trigger == "$credits":
                    pass
        else:
            logger.log(logger.INFO, "Unknown command type: " + json_data["type"] + " for command: " + json_data["cmd"])
