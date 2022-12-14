from twitch_hurby.cmd.events.find import EventFind
from twitch_hurby.cmd.events.rob import EventRob


def create_event(json_data, hurby):
    trigger = json_data["trigger"]
    if trigger == "$rob":
        return EventRob(json_data, hurby)
    if trigger == "$find":
        return EventFind(json_data, hurby)
    return None
