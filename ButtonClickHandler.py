import StateHandler as SH
import GUI
import sys

# delete our Frame "Wrapper" SCREEN and creates a new one
def clear_screen():
    GUI.SCREEN.destroy()
    GUI.SCREEN = GUI.tk.Frame()
    GUI.SCREEN.pack(side='top', fill='both', expand = True)


def on_closing():
    try:
        raise SystemExit(0)
    except RuntimeError:
        raise SystemExit(0)
    except Exception as e:
        print("While executing \"on_closing\" an error occured ->", e)


class MainMenuButtons():
    def btn_play_click():
        clear_screen()
        SH.handle('STATE_PLAY_GAME')


class PlayGameButtons():
    def main_menu_click():
        GUI.root.protocol('WM_DELETE_WINDOW', lambda: on_closing())
        clear_screen()
        SH.handle('STATE_MAIN_MENU')

