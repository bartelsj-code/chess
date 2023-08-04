To run Chess 3, run chessGame.py
To run Chess 5, run game.py

Details about status of project are below.

Chess 1 and chess 2 were simple and incomplete and chess 4 was a failed experiment. They have not been included here.

Chess 3 had my best chess interface and engine until start of June. At the start of June (2023) I decided to do a complete rehaul and rewrite everything from scratch.
the result is chess 5, which is currently incomplete.
the reason for starting from scratch with chess 5 is that I gained a lot of knowledge regarding time complexity, AI algorithms and realized there were many things that could be improved in chess 3 if it was redone from the ground up.
As of 8/3/23, chess 5 is already superior to chess 3 in a variety of ways:
1. It can successfully perform en-passant (a major hurdle I failed to implement in chess 3)
2. Position/Gamestate objects have become significantly more streamlined
3. The moves for any piece starting from any square are precalculated when the program is started and stored in a large hashmap. This results in much faster move collection.
4. MCTS has been implemented
5. Interface is more user-friendly
6. Separation of front-end and back-end that was completely lacking in chess 3
Chess 3 currently still has the stronger engine. As of 8/3/23, the focus has been on improving chess 5 as a whole i.e. making the foundations more efficient. The algorithm that chess 3's best engine (engine 6) uses, has not yet been implemented in chess 5. 
