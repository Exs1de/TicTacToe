import GUI
from GUI import root, tk, MyButton
import ButtonClickHandler as BH
from ButtonClickHandler import MainMenuButtons as M


class StateMainMenu(object):
    def __init__(self):
        GUI.root.title("TIC TAC TOE")
        self.GAME_WIDTH = GUI.GAME_WIDTH
        self.GAME_HEIGHT = GUI.GAME_HEIGHT

        self.BTN_WIDTH = 0.45 * self.GAME_WIDTH
        self.BTN_HEIGHT = 0.14 * self.GAME_HEIGHT
        print('STATE_MAIN_MENU')

        self.container = tk.Label(GUI.SCREEN)
        self.container.place(x=self.GAME_WIDTH / 2 - self.BTN_WIDTH / 2,
                             y=self.GAME_HEIGHT / 2 - 0.54 * self.GAME_HEIGHT / 2,
                             width=self.BTN_WIDTH,
                             height=0.54 * self.GAME_HEIGHT
                             )

        self.btn_play = MyButton(self.container,
                                 height=self.BTN_HEIGHT,
                                 text='START',
                                 command=lambda: M.btn_play_click()
                                 )
        
        self.btn_play.pack(fill=tk.X, pady=0.08 * self.GAME_HEIGHT)

        # self.btn_settings = MyButton(self.container,
        #                              height=self.BTN_HEIGHT,
        #                              text='SETTINGS'
        #                              )

        # self.btn_settings.pack(fill=tk.X,
        #                        pady=0.06 * self.GAME_HEIGHT
        #                        )

        self.btn_exit = MyButton(self.container,
                                 height=self.BTN_HEIGHT,
                                 text='EXIT',
                                 command=lambda: root.destroy()
                                 )

        self.btn_exit.pack(fill=tk.X)
        GUI.root.protocol('WM_DELETE_WINDOW', lambda: BH.on_closing())
