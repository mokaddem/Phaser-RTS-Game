import configparser

#config
cfg = configparser.ConfigParser()
cfg.read('config.cfg')

#server related
app = None
socketio = None
login_manager = None

#game related
startGame = False
gameFinished = False
players = []
the_map = {}
all_requests = []
all_updates = set()
all_creation_updates = set()
actionEventManager = None
