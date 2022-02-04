from constants import Constants
from general import List2D
from random import shuffle

class Server:
    def __init__(self, voice: int, command: int):
        # Create constants for channel IDs
        self.VOICE_CHANNEL_ID: int = voice
        self.COMMAND_CHANNEL_ID: int = command

        # Create game control properties
        self.started: bool = False

        # Create messaging lists
        self.broadcasts: list = []
        self.messages: list = []
        
    def message_recieved(self, author: str, content: str) -> str:
        outbound_message = None

        outbound_message: str = f'{author} sent a message saying {content}'

        return outbound_message

    def start_game(self):
        if self.started:
            return
        self.started: bool = True
        self.broadcasts.append('GAME STARTING')

    
    def direct_message(self, subject, content):
        self.messages.append((subject, content))
            
    
    def update(self):
        # send messages to everyone
        # other stuff
        
        outbound: list = []

        copy = self.messages.copy()
        for message in copy:
            outbound.append(
                {
                    'type':'message',
                    'subject':message[0],
                    'content':message[1],
                }
            )
            #TODO discord client side

        copy = self.broadcasts.copy()
        for broadcast_message in copy:
            outbound.append(
                {
                    'type':'message',
                    'subject':'all',
                    'content':broadcast_message,
                }
            )
            self.broadcasts.remove(broadcast_message)  
        if outbound:
            return outbound
        else:
            return []
        
class GameBoard:
    
    def __init__(self, grid_values='RANDOM'):
        if grid_values.upper() == 'RANDOM':
            squares = list()
            for k, v in Constants.ITEM_PROPORTIONS.items():
                for i in range(v):
                    squares.append(k)
            shuffle(squares)
            self.grid = List2D(7, 7, values=tuple(squares))

        self.content: list = [[10, 'A', 'B', 'C', 'D', 'E', 'F', 'G']]
        self.content.extend( [ [i+1, 0,0,0,0,0,0,0] for i in range(7) ])

    def update_content(self):
        for y, row in enumerate(self.grid):
            for x, item in enumerate(row):
                self.content[y+1][x+1] = item

    def __str__(self) -> str:
        self.update_content()
        output = ''
        for row in self.content:
            for item in row:
                output += ':{}:'.format(Constants.TRANSLATION_TABLE[item])
            output += '\n'
        return output
    def __repr__(self) -> str:
        return self.__str__()
