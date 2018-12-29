from StateMainMenu import StateMainMenu
from StatePlayGame import StatePlayGame

def get_state(state):
    states = {
        'STATE_PLAY_GAME': StatePlayGame,
        'STATE_MAIN_MENU': StateMainMenu,
    }
    return states[state]


def handle(state):
    get_state(state)()  
    # states[state]()
