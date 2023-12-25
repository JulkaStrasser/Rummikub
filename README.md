The game includes:
- Drag and drop tiles
- Multiselect and autosorting tiles to a new user-selected location on the board or player board when they are clicked and highlighted in orange (multiselect), this allows "tidying up" on the user board, making it much easier to find sequences
- analogue timer
- highlighting of wrong sequences (in red)
- Checking for correct movement - messageboxes when an incorrect sequence is found on the board,
detects both sequences consisting of 1, 2 tiles as well as incorrect sequences - not matching any of the rules and at the beginning of the game when the sum of digits on the tiles is less than 30
- Dragging tiles to a grid - the board consists of grids
- QGraphicsScene
- Inheritance from QGraphicsItem
- Graphics created in code
- Logger to display messages in a new window in the QTextEdit control and on the console and to file
- Tile selection button for each player with lock (1 tile can be selected per turn)
- A counter for the remaining tiles in the bag, once the tiles have been dealt out, no more tiles can be selected.
- End of turn button, this allows a player to think about their move while the rest of the players are blocked from playing.
- Messages when one of the players wins
- Test.log file with a record of the entire game

