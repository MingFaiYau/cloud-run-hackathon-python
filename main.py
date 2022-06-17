
# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
import logging
import random
from flask import Flask, request

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

#test
app = Flask(__name__)
non_attack_moves = ['F','L','R']
moves = ['F', 'T', 'L', 'R']

@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"

def convert_arena_state_to_board(arena_state):
    xdim, ydim = arena_state['arena']['dims']
    board = [[0 for _ in range(ydim)] for _ in range(xdim)]
    players = list(arena_state['arena']['state'].values())
    for player in players:
        x = player['x']
        y = player['y']
        board[x][y] = player
    return board

def get_me(arena_state):
    my_url = arena_state['_links']['self']['href']
    return arena_state['arena']['state'][my_url]

def check_has_person_in_coord(x, y, board):
    if (x < 0 or x > len(board[0]) or y < 0 or y > len(board)):
        return False
    return board[x][y] != 0

def check_is_hit():

def check_has_person_in_direction_and_range(x, y, dir, board):
    if (dir == 'N'):
        for i in range(1, 4):
            if (check_has_person_in_coord(x, y -i, board)): return True
    if (dir == 'S'):
        for i in range(1, 4):
            if (check_has_person_in_coord(x, y + i, board)): return True
    if (dir == 'E'):
        for i in range(1, 4):
            if (check_has_person_in_coord(x + i, y, board)): return True
    if (dir == 'W'):
        for i in range(1, 4):
            if (check_has_person_in_coord(x - i, y, board)): return True
    return False


@app.route("/", methods=['POST'])
def move():
    try:
        arena_state = json.loads(request.data)
        board = convert_arena_state_to_board(arena_state)
        me = get_me(arena_state)
        logger.info(me)
        ##if (me['wasHit']):
        ##    return moves[random.randrange(len(non_attack_moves))]
        if (check_has_person_in_direction_and_range(me['x'], me['y'], me['direction'], board)):
            return 'T'
    except Exception:
        return moves[random.randrange(len(moves))]
    return moves[random.randrange(len(moves))]

if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
  
