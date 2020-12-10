import json
import socket
import game
from model import Message
import model

BUFFER_SIZE = 2 ** 10
PORT = 1234
CLOSING = "Application closing..."
CONNECTION_ABORTED = "Connection aborted"
CONNECTED_PATTERN = "Client connected: {}:{}"
ERROR_OCCURRED = "Error Occurred"
RUNNING = "Server is running..."
JSON_FILE_PATH = "data.json"


class Server(object):

    def __init__(self):
        self.players = list()
        self.current = None
        self.port = PORT
        self.socket = None

    def broadcast(self, message):
        for player in self.players:
            player.client_socket.sendall(message.marshal())

    def receive(self, client_socket):
        buffer = ""
        while not buffer.endswith(model.END_CHARACTER):
            buffer += client_socket.recv(BUFFER_SIZE).decode(model.TARGET_ENCODING)
        return buffer[:-1]

    def send(self, client_socket, message):
        client_socket.sendall(message.marshal())

    def close_client_sockets(self):
        self.socket.close()
        for player in self.players:
            player.client_socket.close()

    def run(self):

        # INITIALIZE

        print(RUNNING)

        # Initialize the game state
        success, data = game.load_game_state_from_json(JSON_FILE_PATH)
        if success:
            self.players = game.parse_data(data)
            self.current = data['current']
        else:
            self.players = game.init_players()
            self.current = 1
        new_game = not success

        # Initialize the socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("", self.port))

        # LISTEN

        self.socket.listen(1)
        connected_clients_count = 0

        # Get the client sockets in the quantity equal to the game.NUMBER_OF_PLAYERS
        # and assign them to their Player instances.
        while connected_clients_count != game.NUMBER_OF_PLAYERS:
            try:
                client_socket, address = self.socket.accept()
            except OSError:
                print(CONNECTION_ABORTED)
                return
            print(CONNECTED_PATTERN.format(*address))
            player = self.players[connected_clients_count]
            player.client_socket = client_socket
            self.send(client_socket, Message(username=player.username, operations=player.operations))
            connected_clients_count += 1

        if new_game:
            try:
                message = Message(game_begin=True)
                self.broadcast(message)
                print(message)
            except ConnectionResetError:
                print(CONNECTION_ABORTED)
                return
        else:
            for player in self.players:
                try:
                    message = Message(game_continue=True, current=self.current)
                    self.send(player.client_socket, message)
                    print(message)
                except ConnectionResetError:
                    print(CONNECTION_ABORTED)
                    return

        for player in self.players:
            print(player)

        game.dump_game_state_to_json(self.players, self.current, JSON_FILE_PATH)

        # HANDLE

        cont = True
        while cont:
            # Receive and handle the moves of the players in a row
            for player in self.players:
                client_socket = player.client_socket
                message_from_server = Message(can_move=True,current = self.current)
                self.send(client_socket, message_from_server)
                try:
                    message = Message(**json.loads(self.receive(client_socket)))
                except(ConnectionAbortedError, ConnectionResetError):
                    print(CONNECTION_ABORTED)
                    return
                if message.quit:
                    cont = False
                    break
                oldcurrent = self.current
                self.current = player.move(message.operation,self.current)
                if self.current != 42:
                    message.username = player.username.upper()
                    message.current = oldcurrent
                    self.broadcast(message)
                    print(message)
                else:
                    message = Message(won=True, username=player.username, current = oldcurrent)
                    self.broadcast(message)
                    print(message)
                    self.players = list()
                    self.current = 1
                    cont = False
                    break

            for player in self.players:
                print(player)

            game.dump_game_state_to_json(self.players, self.current, JSON_FILE_PATH)

        # CLOSE

        self.close_client_sockets()
        game.dump_game_state_to_json(self.players, self.current, JSON_FILE_PATH)
        print(CLOSING)


if __name__ == "__main__":
    try:
        Server().run()
    except RuntimeError as error:
        print(ERROR_OCCURRED)
        print(str(error))