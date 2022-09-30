# Lean 4 Natural Number Game


This is a prototype Lean 4 version of the [Natural Number Game
(NNG)](https://www.ma.imperial.ac.uk/~buzzard/xena/natural_number_game/)
of Kevin Buzzard and Mohammad Pedramfar. It only has 5 levels so far. 
It uses the [Lean 4 game server](https://github.com/PatrickMassot/lean4-game-server) whose README has a lot more general information.

A temporary hack in `Main.lean` assumes you have the game-server library installed in a `game-server` folder sitting next to your `NNG4` folder. Hopefully this will be fixed soon. Until then you can either make sure you have this folder layout or modify `Main.lean` before building. Once this is done, you can build using `lake build` in the NNG4 root folder (this will build the game server if needed).
 
Then you can already "play" in text mode by running `build/bin/nng`. If you want to run the web interface you need to launch the `gameserver.py` python script (after installing the `websockets` python library). This will use port 8765 by default, but you can set the `PORT` environment variable to override this (or modify the python code...). 

Then you need to clone the [interface repository](https://github.com/PatrickMassot/nng4-interface) and build the interface. See instructions there.

