import socket

from twitch_hurby.irc.threads.cron_jobs import CronJobs
from twitch_hurby.irc.threads.read_chat import ReadChat
from twitch_hurby.twitch_config import TwitchConfig
from utils import logger


class IRCConnector:
    def __init__(self, botname: str, botpassword: str, receiver, tick, twitch_conf: TwitchConfig, hurby):
        self.host = TwitchConfig.HOST
        self.port = TwitchConfig.PORT
        self.twitch_conf = twitch_conf
        self.username = botname
        self.password = botpassword
        self.connection = None
        self.tick = tick
        self.receiver = receiver
        self.thread = None
        self.cron_jobs_thread = None
        self.channel = None
        self.hurby = hurby

    def connect(self):
        self.connection = socket.socket()
        self.connection.connect((self.host, self.port))
        self.connection.send(bytes('PASS %s\r\n' % self.password, 'UTF-8'))
        self.connection.send(bytes('NICK %s\r\n' % self.username, 'UTF-8'))

    def join_channel(self, channel: str):
        self.connection.send(bytes('JOIN %s\r\n' % channel, 'UTF-8'))

    def cap(self):
        self.connection.send(bytes('CAP REQ :twitch.tv/commands', 'UTF-8'))

    def start(self, channel: str):
        self.channel = channel
        self.connect()
        self.join_channel(self.channel)
        # self.cap()
        self.thread = ReadChat(self, self.tick, self.receiver)
        self.cron_jobs_thread = CronJobs(self.twitch_conf, self.receiver, self)
        self.thread.start()
        self.cron_jobs_thread.start()

    def check_viewers(self):
        self.connection.send(bytes('WHO %s\r\n' % self.channel, 'UTF-8'))

    def send_message(self, msg):
        # output = 'PRIVMSG %s :%s\r\n' % (self.channel, msg)
        output = "PRIVMSG " + self.channel + " :" + msg + "\r\n"
        logger.log(logger.INFO, output)
        self.connection.send(bytes(output, 'UTF-8'))
        # self.connection.send(bytes('PRIVMSG %s :%s\r\n' % (self.channel, msg), 'UTF-8'))

    def send_whisper(self, user, msg):
        output = "PRIVMSG " + self.channel + " :/w " + user + " " + msg + "\r\n"
        logger.log(logger.INFO, output)
        self.connection.send(bytes(output, 'UTF-8'))

    def ping_pong(self, msg: str):
        output = "PONG " + msg + "\r\n"
        self.connection.send(bytes(output, 'UTF-8'))