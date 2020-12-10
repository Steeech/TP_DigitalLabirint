import json

END_CHARACTER = "\0"
MOVE_PATTERN = "{username}> {current}{operation}"
GAME_BEGIN = "GAME BEGIN! Starting number: 1"
GAME_CONTINUE = "GAME CONTINUE! Last number: {current}"
YOUR_MOVE = "You move. Current number: {current}"
MOVE_AGAIN = "INCORRECT MOVE! The city must start with a letter {letter} and should not contain characters " \
             "uncharacteristic for the city name "
NICHYA = "Nichya!"
WON_PATTERN = "{username} won!  {current}{operation}=42"
TARGET_ENCODING = "utf-8"


class Message(object):
    def __init__(self, **kwargs):
        self.username = None
        self.operation = None
        self.operations = None
        self.current = None
        self.game_begin = False
        self.game_continue = False
        self.can_move = False
        self.quit = False
        self.nichya = False
        self.won = False
        self.__dict__.update(kwargs)

    def __str__(self):
        if self.game_begin:
            return GAME_BEGIN.format(**self.__dict__)
        if self.game_continue:
            return GAME_CONTINUE.format(**self.__dict__)
        if self.can_move:
            return YOUR_MOVE.format(**self.__dict__)
        if self.nichya:
            return NICHYA
        if self.won:
            return WON_PATTERN.format(**self.__dict__)
        return MOVE_PATTERN.format(**self.__dict__)

    def marshal(self):
        return (json.dumps(self.__dict__) + END_CHARACTER).encode(TARGET_ENCODING)
