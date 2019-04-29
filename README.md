# TCP tic tac toe GAME (Python 3.6.4) 
# (PLEASE DO NOT WATCH TIHS)

## How to play?
1. run **start_server.py**
1. run 2 clients -> **start_client.py** twice
1. game possible only between 2 players!!!

### some info
* When 2 clients are connected to server, each client is given random nickname and symbol (X / O)
* do not even try to connect to the server from 3rd... nth client while it is handling game session, you will be redirect back to Main Menu :(

## Main Menu
![example](/images/example_5.png)

## Waiting for 2nd player
![waiting for players](/images/example_4.png)

## Some Gemaplay
![waiting for players](/images/example_1.png)

## Opponent left the game?
![waiting for players](/images/example_6.png)

## WIN / LOOSE
![example](/images/example_2.png)

## DRAW
![example](/images/example_3.png)

## Some server output
![server](/images/server_output_1.png)

## More server outputs
![server](/images/server_output_2.png)

## How to start a new game?
After your game has finished, not dependiong on event (you lose / won / your opponent has disconnected or you left the game)
server will automaticly restart itself and be ready for new game sessionm, just press play button (START) in your client

Unfortunately if smth went wrong, just run start_server.py one more time :)
![server](/images/server_output_3.png)

## Some client output
![server](/images/client_output_1.png)
