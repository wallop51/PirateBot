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
        
