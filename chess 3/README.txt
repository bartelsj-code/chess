en passant missing. 
draw by 50 move rule, 3 fold repetition, and insufficient material are missing.
gamestates do not store previous move.
check-detection and mate-detection very slow.

engine 6 uses a alpha-beta minimax algorithm. 
It does this with iterative deepening. 
Each iteration, the children of gamestates are sorted by their previously determined levels of utility. This vastly improves the effectiveness of alpha beta pruning. 
Additionally a dictionary storing visited positions and their heuristic value is made to avoid evaluating the same position twice (this vastly improves performance when branching factor diminishes later in the game)

