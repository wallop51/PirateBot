class Server:
    def __init__(self, voice, command):
        self.VOICE_CHANNEL_ID = voice
        self.COMMAND_CHANNEL_ID = command
        self.started = False
        self.broadcasts = []
        
    def message_recieved(self, author, content):
        outbound_message = None

        outbound_message = f'{author} sent a message saying {content}'

        return outbound_message

    def start_game(self):
        if self.started:
            return
        self.started = True
        self.broadcasts.append('GAME STARTING')
            
    
    def update(self):
        # send messages to everyone
        # other stuff
        
        outbound = []

        copy = self.broadcasts.copy()
        for broadcast_message in copy:
            outbound.append({'type':'message',
             'subject':'all',
             'content':broadcast_message})
            self.broadcasts.remove(broadcast_message)  
        if outbound:
            return outbound
        else:
            return []
        
