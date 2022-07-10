import framework
global LANG
LANG = LangContatiner()

global LOGGER
LOGGER = logging.getLogger(__name__)
LOGGER.info(f'{__name__} logger has been initialised.')

class Grid:
    def __init__(self, selection, size=7):
        self.items = [[None for i in range(size)] for j in range(size)]
    def __getitem__(self, coords):
        x, y = coords
        return self.items[x][y]
    def __setitem__(self, coords, value):
        x, y = coords
        self.items[x][y] = value

    def __str__(self) -> str:
        # TODO A function that returns the board as a string that can be sent to the player.
        return 

class App(framework.BaseClass):
    def __init__(self, debug=True):
        super().__init__(debug)
    def recieved_group_channel(self, message):

    async def recieved_group_channel(self, message):
        pass
    async def recieved_command(self, message):
        content = message.content
        parts = content.split(' ')
        if parts[1].upper() == 'HELP':
            await message.channel.send(self.lang.pirate.help.message)
        elif parts[1].upper() == 'START':
            self.start_game()

    async def recieved_direct_message(self, message):
        pass

    def start_game(self):
        self.current_game = Game(self.voice_channel.members)

a=Grid(0)
print(a.items)