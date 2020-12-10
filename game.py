import math
from random import *
import json
import jsonschema
from jsonschema import validate

NUMBER_OF_PLAYERS = 2
MAX_INITIAL_DISTANCE = 10
MIN_INITIAL_DISTANCE = 2
MAX_ANGLE = 360

schema = {
    "type": "object",
    "properties": {
        "players": {
            "type": "array",
            "minItems": NUMBER_OF_PLAYERS,
            "maxItems": NUMBER_OF_PLAYERS,
            "items": [
                {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string"},
                        "operations": {

                            "type": "array",
                            "items": [
                                {
                                    "operation": {"type": "string"}
                                }
                            ]

                        }
                    },
                    "required": [
                        "username",
                        "operations"
                    ],
                    "additionalProperties": False
                }
            ]

        },
        "current": {"type": "number"}
    },
    "required": [
        "players",
        "current"
    ]
}

def generate_operation():
    all_operations = ['+', '-', '*', '/', '%']
    return choice(all_operations)+str(randint(1,100))

def generate_operations():
    operations = list()
    for i in range(5):
        operations.append(generate_operation())
    return operations


def create_player(username, operations, client):
    return Player(username, operations, client)


def parse_data(data):
    players = list()
    for player_data in data['players']:
        operations = list()
        for operation in player_data['operations']:
            operations.append(operation)
        player = Player(player_data['username'],
                        operations,
                        None)
        players.append(player)
    return players



def init_players():
    players = list()
    for i in range(0, NUMBER_OF_PLAYERS):
        players.append(
            create_player(
                f"player{i}", generate_operations(), None
            )
        )
    return players


def validate_json(data):
    try:
        validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True


def load_game_state_from_json(json_file_path):
    with open(json_file_path) as json_file:
        try:
            data = json.load(json_file)
            if validate_json(data):
                return True, data
        except json.decoder.JSONDecodeError:
            pass
    return False, None


def dump_game_state_to_json(players, current, json_file_path):
    data = {'players': [], "current": current}
    for player in players:
        data['players'].append(player.dict())
    with open(json_file_path, 'w') as outfile:
        json.dump(data, outfile, indent=4)


class Player:

    def __init__(self, username, operations, client_socket):
        self.username = username
        self.operations = operations
        self.client_socket = client_socket

    def __str__(self):
        return f"Player username: {self.username}"

    def move(self, operation, current):
        if operation[0] == '+':
            return current+int(operation[1:])
        if operation[0] == '-':
            return current-int(operation[1:])
        if operation[0] == '*':
            return current*int(operation[1:])
        if operation[0] == '/':
            return current//int(operation[1:])
        if operation[0] == '%':
            return current%int(operation[1:])

    def won(self, current):
        return current == 42

    def dict(self):
        return {
            'username': self.username,
            'operations': self.operations
        }
