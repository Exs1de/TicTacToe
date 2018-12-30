from datetime import datetime
from random import randint
import socket
import json
import time


class Server(object):
    def __init__(self):
        self.host = 'localhost'
        self.port = 9090
        self.server = (self.host, self.port)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(self.server)
        self.s.listen(5)

        self.players = {} # dict of players, key: (ip, port)| value: player 
        self.player = {}  # dict, check -> init_player()
        self.nicknames = ['Mr.Duck', 'SuperbananA', 'DevilCacke', 'Ultrac@t', 'GlobalKEK', '4nrealCrab', 'Zzzips']
        self.shutdown = False      

        self.STATES = {
            'STATE_WAITING_FOR_PLAYERS': self.waiting_for_players,
            'STATE_PLAY_GAME': self.play_game,
        }

        self.play_game_entry = True
        self.current_state = 'STATE_WAITING_FOR_PLAYERS'

        self.victory = ''   # contains "victory symbol"
        self.combo = 0      # combo id in range (1, 9), used for highliting combo on client side

        self.playboard = {}
        for i in range(1, 10):
            self.playboard.update({f'btn_{i}': ''})


    def handle_state(self, state):
        self.STATES[state]()


    def run(self):
        print(f'[!!! Server Started !!!] >> {self.host}:{self.port}')  
        self.handle_state(self.current_state)

        
    # Generate server`s own response, which will be sent to clients
    def response(self, player, command):
        r = {
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'command': command,
            'used_cells': self.playboard,
            'player': self.players[player],
        }

        r = json.dumps(r, ensure_ascii=False).encode("utf-8")
        player.sendall(r)

        
    # Receive and proccess client response
    def client_response(self, client):
        data = client.recv(1024)
        r = json.loads(data)

        # some fancy output of client response / player action
        print(f"[id: {r['player']['addr'][1]}][{r['player']['nickname']}] >> pressed ",
              f"{r['used_cell']} -> {r['player']['symbol']}")
        print(json.dumps(r, indent=4, ensure_ascii=False), end='\n\n')

        used_cell = r['used_cell']

        self.playboard[used_cell] = r['player']['symbol']
        
        # print(f"{r['player']['nickname']} pressed {r['used_cell']}")
        print('current playboard: ', 
              json.dumps(self.playboard, indent=4, sort_keys=True, ensure_ascii=False),
              end='\n\n')


    def init_player(self, addr, nickname='', symbol=''):
        self.player = {
            'addr': addr,
            'nickname': nickname,
            'symbol': symbol,
        }

        return self.player


    def waiting_for_players(self):
        err = False
        two_players = False
        while not two_players:
            try:
                print('waiting for players...')

                client, addr = self.s.accept()

                if client not in self.players:
                    self.players.update({client: self.init_player(addr)})
                    print(f"[id: {self.players[client]['addr']}] >> joined server!")
                
                # check if the clients connected:
                for player in self.players:
                    try:
                        player.sendall(b'Are you connected?)')
                        time.sleep(0.1)
                    except Exception as e:
                        print('while checking whether client is connected ->', e)
                        print(f"[id: {self.players[player]['addr']}] >> disconnected")
                        self.players.pop(player)

                        # send test message in order to "initialize client"
                        # if after connection client doesn`t recieve response 
                        # from server in 3 second, connection closes and client returns to STATE_MAIN_MENU
                        list(self.players.keys())[0].sendall(b'Are you connected?)')
                        break

                print('Current players on the server:')
                for x in self.players:
                    print(self.players[x]['addr'])

                if len(self.players) == 2:
                    print('2 Players Already on server, START GAME!!!')
                    two_players = True

            except Exception as e:
                print(f'\n[!!! While Waiting for Players !!] > {e}')
                err = True
                break

        if not err:
            self.current_state = 'STATE_PLAY_GAME'
            self.handle_state(self.current_state)


    def play_game(self):
        print('STATE_PLAY_GAME')

        keys = list(self.players.keys())
        X_PLAYER = keys[randint(0, 1)]
        keys.remove(X_PLAYER)
        O_PLAYER = keys[0]

        print('X_PLAYER ->', X_PLAYER)
        print('O_PLAYER ->', O_PLAYER)

        for player in self.players:
            nickname = self.nicknames[randint(0, len(self.nicknames)-1)]
            self.players[player]['nickname'] = nickname
            self.nicknames.remove(nickname)

            if player is X_PLAYER:
                self.players[player]['symbol'] = 'X'
                X_PLAYER = player

            if player is O_PLAYER:
                self.players[player]['symbol'] = 'O'
                O_PLAYER = player
     
        self.response(X_PLAYER, 'init_player')
        time.sleep(0.1)
        self.response(O_PLAYER, 'init_player')

        print('Starting game cycle...')
        self.used_playboard_cells = []
        self.game_not_finished = True
        while self.game_not_finished:
            try:
                # X_PLAYER makes step
                self.response(X_PLAYER, 'unblock_playboard') 
                    
                # Catch X_PLAYER step (get btn)
                self.client_response(X_PLAYER)
                    
                # Draw X on O_Player playboard
                self.response(O_PLAYER, 'redraw_playboard')

                # check WIN condition (if X_PLAYER won)
                if self.check_win_cond('X'):
                    self.response(X_PLAYER, f'victory-{self.combo}')
                    self.response(O_PLAYER, f'loose-{self.combo}')
                    break

                # check DRAW condition
                if '' not in list(self.playboard.values()):
                    print('DRAW') 
                    self.response(X_PLAYER, 'draw')
                    self.response(O_PLAYER, 'draw')
                    break  

                # O_PLAYER makes step
                self.response(O_PLAYER, 'unblock_playboard') 
               
                # Catch O_PLAYER step (get btn)
                self.client_response(O_PLAYER)

                # Draw O on X_Player playboard
                self.response(X_PLAYER, 'redraw_playboard')
                
                
                # check WIN condition (if O_PLAYER won)
                if self.check_win_cond('O'):
                    self.response(X_PLAYER, f'loose-{self.combo}')
                    self.response(O_PLAYER, f'victory-{self.combo}')
                    break

            except ConnectionResetError:
                print('Somebody of clients disconnected :(')
                for player in self.players:
                    try:
                        self.response(player, 'opponent left hte game')
                    except:
                        continue
                break

                print('next step')

        print('Game has Finished, Good Bye :)')
        self.s.close()


    def check_win_cond(self, symbol):
        k = self.playboard

        # ROW COMBOS
        if k['btn_1'] == symbol and k['btn_2'] == symbol and k['btn_3'] == symbol:
            self.victory = symbol
            self.combo = 1

        if k['btn_4'] == symbol and k['btn_5'] == symbol and k['btn_6'] == symbol:
            self.victory = symbol
            self.combo = 2

        if k['btn_7'] == symbol and k['btn_8'] == symbol and k['btn_9'] == symbol:
            self.victory = symbol
            self.combo = 3

        # COLUMN COMBOS
        if k['btn_1'] == symbol and k['btn_4'] == symbol and k['btn_7'] == symbol:
            self.victory = symbol
            self.combo = 4

        if k['btn_2'] == symbol and k['btn_5'] == symbol and k['btn_8'] == symbol:
            self.victory = symbol
            self.combo = 5

        if k['btn_3'] == symbol and k['btn_6'] == symbol and k['btn_9'] == symbol:
            self.victory = symbol
            self.combo = 6

        # DIAGONAL COMBOS
        if k['btn_1'] == symbol and k['btn_5'] == symbol and k['btn_9'] == symbol:
            self.victory = symbol
            self.combo = 7

        if k['btn_3'] == symbol and k['btn_5'] == symbol and k['btn_7'] == symbol:
            self.victory = symbol
            self.combo = 8

        if len(self.victory) == 1:
            print(f'!!!{symbol} PLAYER WON!!!')
            self.game_not_finished = False
            return True
            
        return False
              

    def stop(self):
        self.__del__()


    def __del__(self):
        self.s.close()
        del self
        print('GAME SERVER instance was deleted')


while True:
    server = Server()
    server.run()

    server.stop()
    print('===================')
    print('READY FOR NEW GAME')
    print('===================')

