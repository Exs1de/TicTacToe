from ButtonClickHandler import PlayGameButtons as P
from GUI import root, tk, MyButton
from datetime import datetime
import threading
import socket
import json
import time
import sys
import GUI


class Client(object):
    def __init__(self, game):
        try:
            self.game = game

            self.server = ('localhost', 9090)

            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.settimeout(3)
            self.s.connect(self.server)
            self.s.settimeout(None)

            self.disconnect = False
            self.init_client_on_server = False

            self.start()

        except Exception as e:
            print('AFTER WAITING 3 SECONDS')
            print('CONNECTION FAILED')
            print(e)
            P.main_menu_click()
            
            
    # receiving jsons from Server and apply specific actions to Game
    def receiving(self, name, sock):
        print('RECEIVING MODE')
        while not self.disconnect:
            try:
                while True:
                    if not self.init_client_on_server:
                        try:
                            self.s.settimeout(3)
                            data = self.s.recv(1024)
                            self.s.settimeout(None)
                            self.handle_server_response(data)

                            self.init_client_on_server = True
                        except Exception as e:
                            print('On init phase: ', e)
                            self.disconnect = True
                            break
                    else:
                        # normal mode
                        data = self.s.recv(1024)
                        self.handle_server_response(data)
             
            except Exception as e:
                print(f'while receiving an error occured: {e}')
                self.disconnect = True

        print('STOP RECEIVING DATA FROM SERVER')
        self.game.stop_thread_and_go_to_MainMenu()


    def response(self, player, used_cell):
        r = {
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'player': player,
            'used_cell': used_cell,
        }

        r = json.dumps(r, ensure_ascii=False).encode("utf-8")
        self.s.sendall(r)


    def handle_server_response(self, r):
        print('DATA RECEIVED FROM SERVER')

        f = r.decode("utf-8")
        if f == 'Are you connected?)':
            print(f'Server asked: {f}')
            self.init_client_on_server = True
            self.game.update_status(1)

        else:
            r = json.loads(r)
            print(json.dumps(r, indent=4, sort_keys=True, ensure_ascii=False))

            cmd = r['command']
            print(f'cmd = {cmd}')

            if cmd == 'init_player':
                self.game.me = r['player']
                GUI.root.title(f"[ID: {r['player']['addr'][1]}] {r['player']['nickname']} - {r['player']['symbol']}")
                GUI.root.update()
                print('client was successfuly initialized with')

            if 'loose' in cmd:  
                self.game.draw_BACK_TO_MAIN_MENU_button()
                self.game.update_status(3)
                self.game.highlight_win_combo(cmd[-1], 'red')
                    
            if 'victory' in cmd:
                self.game.draw_BACK_TO_MAIN_MENU_button()
                self.game.update_status(4)
                self.game.highlight_win_combo(cmd[-1], 'green')

            if cmd == 'draw':
                self.game.draw_BACK_TO_MAIN_MENU_button()
                self.game.update_status(5)

            if cmd == 'redraw_playboard':
                print('executing "redraw_playboard"')

                self.game.redraw_playboard(r['used_cells'])

            if cmd == 'unblock_playboard':
                print('executing "unblock_playboard"')
                self.game.update_status(2)
                self.game.unblock_playboard(r['used_cells'])

            if cmd == 'opponent left hte game':
                self.game.draw_BACK_TO_MAIN_MENU_button()
                self.game.update_status(7)


    def start(self):
        self.rT = threading.Thread(target=self.receiving, args=("SomeGoodFuncName", self.s))
        self.rT.daemon = False
        self.rT.start()


class StatePlayGame(object):
    def __init__(self):
        print('STATE_PLAYBOARD')
        self.me = {} # player info
        self.type = ''
        self.exit = False
        self.GAME_WIDTH = GUI.GAME_WIDTH
        self.GAME_HEIGHT = GUI.GAME_HEIGHT

        self.BTN_WIDTH = 0.45 * self.GAME_WIDTH
        self.BTN_HEIGHT = 0.14 * self.GAME_HEIGHT

        self.play_board_size = 500
        self.btn_size = 0.3 * self.play_board_size

        # playboard background
        self.container = tk.Label(GUI.SCREEN, bg='black')
        self.container.place(rely=0.5,
                             relx=0.5,
                             anchor=tk.CENTER,
                             width=self.play_board_size,
                             height=self.play_board_size
                             )
        self.container.update()

        formula = self.btn_size + 0.05 * self.play_board_size
        y = [-2, formula - 2, formula * 2]

        # placing buttons from right to left, 
        # naming buttons from left to rigth 
        fix = [2, 1, 0]
        self.btn_dict = {}
        for i in [1, 2, 3]:
            for j in [2, 1, 0]:
                self.btn_dict.update({
                    f'btn_{i*3 - fix[j]}': tk.Button(self.container,
                                                text='',
                                                font=('Helvetica', 100, 'bold'),
                                                borderwidth=0
                                                )
                })

                self.btn_dict[f'btn_{i*3 - fix[j]}'].place(x=(j * formula - 2),
                                                      y=y[i - 1],
                                                      width=int(self.btn_size),
                                                      height=int(self.btn_size)
                                                      )
                
        self.btn_dict['btn_1'].config(command=lambda: self.draw_X_O('btn_1'))
        self.btn_dict['btn_2'].config(command=lambda: self.draw_X_O('btn_2'))
        self.btn_dict['btn_3'].config(command=lambda: self.draw_X_O('btn_3'))
        self.btn_dict['btn_4'].config(command=lambda: self.draw_X_O('btn_4'))
        self.btn_dict['btn_5'].config(command=lambda: self.draw_X_O('btn_5'))
        self.btn_dict['btn_6'].config(command=lambda: self.draw_X_O('btn_6'))
        self.btn_dict['btn_7'].config(command=lambda: self.draw_X_O('btn_7'))
        self.btn_dict['btn_8'].config(command=lambda: self.draw_X_O('btn_8'))
        self.btn_dict['btn_9'].config(command=lambda: self.draw_X_O('btn_9'))

        style = tk.ttk.Style()
        style.configure('KEKOS.TButton', font=('Verdana', 20, 'bold'))

        style_enter = tk.ttk.Style()
        style_enter.configure('Enter.TButton',
                              foreground='green',
                              font=('Verdana', 20, 'bold')
                              )

        style_leave = tk.ttk.Style()
        style_leave.configure('Leave.TButton',
                              bakcground='red',
                              font=('Verdana', 20, 'bold')
                              )

        self.draw_win_loose_label()
        self.block_playboard()
        try:
            self.client = Client(self)
        except Exception as e:
           print('While trying to init Client() ->', e)
           self.connection_failed()

        # closing all connections and threads on WINDOW CLOSE
        GUI.root.protocol("WM_DELETE_WINDOW", lambda: on_closing_playgame(self))
        

    def connection_failed(self):
        print('Server refused connection')
        P.main_menu_click()


    def stop_thread_and_go_to_MainMenu(self):
        try:
            self.client.rT._delete()

            self.exit = True
            time.sleep(0.1)
            self.client.s.close()
            print(f'is Thread alive? -> {self.client.rT.is_alive()}')

            # del self.client
        except Exception as e:
            print('When try to delete Thread an error occured -> ', e)
     
        print('disconnected')
        P.main_menu_click()


    def draw_BACK_TO_MAIN_MENU_button(self):
        self.btn_main_menu = MyButton(GUI.SCREEN,
                                      text='Back to Main Menu',
                                      style='KEKOS.TButton',
                                      command=lambda: self.stop_thread_and_go_to_MainMenu()
                                      )

        self.btn_main_menu.place(relx=0.5,
                                 y=self.GAME_HEIGHT - (self.GAME_HEIGHT - self.play_board_size) / 4,
                                 height=50,
                                 width=300,
                                 anchor='center'
                                 )

        self.btn_main_menu.bind("<Enter>", self.on_enter)
        self.btn_main_menu.bind("<Leave>", self.on_leave)


    # events for BACK TO MAIN MENU BUTOON
    def on_enter(self, e):
        self.btn_main_menu._btn.config(style='Enter.TButton')
        self.btn_main_menu.update()


    def on_leave(self, e):
        self.btn_main_menu._btn.config(style='Leave.TButton')
        self.btn_main_menu.update()


    def draw_X_O(self, btn):
        if self.me['symbol'] is 'X':
            self.btn_dict[btn].config(text='X')

        if self.me['symbol'] is 'O':
            self.btn_dict[btn].config(text='O')

        self.block_playboard()
        self.update_status(6)

        self.client.response(self.me, btn)


    def draw_win_loose_label(self):
        self.l = tk.Label(GUI.SCREEN, font=('Helvetica', 20, 'bold'), fg='green')
        self.l.place(y=self.container.winfo_y() / 2,
                relx=0.5,
                anchor=tk.CENTER,
                width=self.container.winfo_width(),
                height=self.GAME_HEIGHT*0.15,
                )
        self.l.update()


    def update_status(self, status):
        if status == 1:
            self.l.config(text='WAITING FOR PLAYERS...', fg='green')
        if status == 2:
            self.l.config(text='Your turn!', fg='green')
        if status == 3:
            self.l.config(text='YOU LOOSE :(', fg='red')
        if status == 4:
            self.l.config(text='!!! YOU WIN !!!', fg='green')
        if status == 5:
            self.l.config(text='DRAW', fg='green')
        if status == 6:
            self.l.config(text='Opponent`s turn', fg='green')
        if status == 7:
            self.l.config(text='Opponent left the game :(', fg='red')


    def draw_X(self, btn):     
        self.btn_dict[btn].config(text='X')


    def draw_O(self, btn):     
        self.btn_dict[btn].config(text='O')


    def update_all_buttons(self):
        for btn in self.btn_dict.keys():
            self.btn_dict[btn].config(bg='SystemButtonFace')


    def block_playboard(self):
        self.container.config(bg='black')
        self.container.update()

        self.update_all_buttons()

        for btn in self.btn_dict.keys():
            self.btn_dict[btn].config(command=lambda: ())


    def unblock_playboard(self, buttons_to_block):
        self.container.config(bg='green')
        self.container.update()

        self.update_all_buttons()

        if buttons_to_block['btn_1'] is '': self.btn_dict['btn_1'].config(command=lambda: self.draw_X_O('btn_1'))
        if buttons_to_block['btn_2'] is '': self.btn_dict['btn_2'].config(command=lambda: self.draw_X_O('btn_2'))
        if buttons_to_block['btn_3'] is '': self.btn_dict['btn_3'].config(command=lambda: self.draw_X_O('btn_3'))
        if buttons_to_block['btn_4'] is '': self.btn_dict['btn_4'].config(command=lambda: self.draw_X_O('btn_4'))
        if buttons_to_block['btn_5'] is '': self.btn_dict['btn_5'].config(command=lambda: self.draw_X_O('btn_5'))
        if buttons_to_block['btn_6'] is '': self.btn_dict['btn_6'].config(command=lambda: self.draw_X_O('btn_6'))
        if buttons_to_block['btn_7'] is '': self.btn_dict['btn_7'].config(command=lambda: self.draw_X_O('btn_7'))
        if buttons_to_block['btn_8'] is '': self.btn_dict['btn_8'].config(command=lambda: self.draw_X_O('btn_8'))
        if buttons_to_block['btn_9'] is '': self.btn_dict['btn_9'].config(command=lambda: self.draw_X_O('btn_9'))


    def redraw_playboard(self, playboard):
        for btn in self.btn_dict:
            if playboard[btn] is not '':
                self.btn_dict[btn].config(text=playboard[btn])


    def highlight_win_combo(self, combo, color):
        combo = int(combo)
        if combo == 1: 
            self.btn_dict['btn_1'].config(fg=color)
            self.btn_dict['btn_2'].config(fg=color)
            self.btn_dict['btn_3'].config(fg=color)

        if combo == 2:
            self.btn_dict['btn_4'].config(fg=color)
            self.btn_dict['btn_5'].config(fg=color)
            self.btn_dict['btn_6'].config(fg=color)

        if combo == 3:
            self.btn_dict['btn_7'].config(fg=color)
            self.btn_dict['btn_8'].config(fg=color)
            self.btn_dict['btn_9'].config(fg=color)

        if combo == 4:
            self.btn_dict['btn_1'].config(fg=color)
            self.btn_dict['btn_4'].config(fg=color)
            self.btn_dict['btn_7'].config(fg=color)

        if combo == 5:
            self.btn_dict['btn_2'].config(fg=color)
            self.btn_dict['btn_5'].config(fg=color)
            self.btn_dict['btn_8'].config(fg=color)

        if combo == 6:
            self.btn_dict['btn_3'].config(fg=color)
            self.btn_dict['btn_6'].config(fg=color)
            self.btn_dict['btn_9'].config(fg=color)

        if combo == 7:
            self.btn_dict['btn_1'].config(fg=color)
            self.btn_dict['btn_5'].config(fg=color)
            self.btn_dict['btn_9'].config(fg=color)

        if combo == 8:
            self.btn_dict['btn_3'].config(fg=color)
            self.btn_dict['btn_5'].config(fg=color)
            self.btn_dict['btn_7'].config(fg=color)


    def __del__(self):
        del self
        print('Client instance deleted!')


def on_closing_playgame(obj):
    try:
        obj.exit = True
        print('closing window')

        try:
            obj.client.s.close()
        except Exception as e:
            print('while trying to CLOSE CONNECTION: ', e)

        print('disconnected')
        raise SystemExit(0)

    except Exception as e:
        print(f'while closing from STATE_PLAY_GAME: {e}')
        raise SystemExit(0)
