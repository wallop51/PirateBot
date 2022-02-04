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
    TRANSLATION_TABLE: dict = {
        0:'white_large_square',
        1:'one', 2:'two', 3:'three', 4:'four', 5:'five',
        6:'six', 7:'seven',
        'A':'regional_indicator_a', 'B':'regional_indicator_b', 'C':'regional_indicator_c', 'D':'regional_indicator_d',
        'E':'regional_indicator_e', 'F':'regional_indicator_f', 'G':'regional_indicator_g', 
    }
    def __init__(self):
        self.content: list = [[0, 'A', 'B', 'C', 'D', 'E', 'F', 'G']]
        self.content.extend( [ [i+1, 0,0,0,0,0,0,0] for i in range(7) ])

    def __str__(self) -> str:
        output = ''
        for row in self.content:
            for item in row:
                output += ':{}:'.format(self.TRANSLATION_TABLE[item])
            output += '\n'
        return output
    def __repr__(self) -> str:
        return self.__str__()