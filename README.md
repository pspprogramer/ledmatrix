Full Read me comming later.
(currently for windows only) requirements - using PIP you will need serial and keyboard. no other API is required for this so far.
linux guys you might be able to change the input library and serial ports to the correct names for your system but i currently dont support it.

this script(s) are currently made to interact and play the built in games on the led matrix for the framwork 16. these scrips have no game logic what so ever and just pass your key presses to the matrix so you can interact with the built in game.
note that currently this script has no idea on the current game state so you will need to reset the script to reset the game. (planned feature to add this to a simple key press) 

on snake the game will just freeze when you die. also some fruit will spawn over your snake so you have to travel around to reveal it. through my gameplay i have noticed most fruit spawn on the top of the matrix.

pong sends no serial feedback that i can find when one or the other player scores. the game seems to just run forever reguardless of how many points is scored.

the orignal API/commands for the matrix that this script uses. (https://github.com/FrameworkComputer/inputmodule-rs/blob/main/commands.md)

there are some refrences for a tetris game but i cycled through all 256 bytes for game id's and only found snake and pong.

known bugs to fix. 
script doent exit properly yet (ctrl+c work around)
