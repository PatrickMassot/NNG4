# Lean 4 Natural Number Game


This is a prototype Lean 4 version of the [Natural Number Game
(NNG)](https://www.ma.imperial.ac.uk/~buzzard/xena/natural_number_game/)
of Kevin Buzzard and Mohammad Pedramfar. It only has 5 levels so far. 
It uses the [Lean 4 game server](https://github.com/PatrickMassot/lean4-game-server) whose README has a lot more general information.

## Building and running

A temporary hack in `Main.lean` assumes you have the game-server library installed in a `game-server` folder sitting next to your `NNG4` folder. Hopefully this will be fixed soon. Until then you can either make sure you have this folder layout or modify `Main.lean` before building. Once this is done, you can build using `lake build` in the NNG4 root folder (this will build the game server if needed).
 
Then you can already "play" in text mode by running `build/bin/nng`. If you want to run the web interface you need to launch the `gameserver.py` python script (after installing the `websockets` python library). This will use port 8765 by default, but you can set the `PORT` environment variable to override this (or modify the python code...). If you want the server to be accessible
from the outside you may need to use `gameserver_ssl.py` in order to satisfy
paranoid web browser. This requires some SSL certificate (see https://letsencrypt.org/ to get one if needed). There are more explanation at the top of that python script.

Then you need to clone the [interface repository](https://github.com/PatrickMassot/nng4-interface) and build the interface. See instructions there.

## Some game-play choices

Note that a lot of game-play decisions were made for this game on top of the general framework provided by [Lean 4 game server](https://github.com/PatrickMassot/lean4-game-server). In particular:
* All the wizard/rogue-like speak is completely specific to this game, not the framework.
* the game uses only the `rewrite` tactic from Lean 4 core, instead of the more usual `rw` tactic that does `rewrite` followed by (weak) `rfl`. This was already true in the original NNG except that Kevin redefined `rw` there. It happens that in Lean 4 core library the `rewrite` tactic was already available. At some point we may redefine `rw` in the game because typing `rewrite` is painful. Note also that in Lean 4, square bracket arguments of `rewrite` or `rw` are mandatory. Again this could be overridden in the game if people find it too painful.
* the game prevents "accidental" definitional equalities that were so confusing to beginners in the original NNG. The natural numbers used in that game have *no definitional properties whatsoever*. They are *not* defined using the calculus of inductive constructions. Even `0 + 0 = 0` cannot be proven using `rfl`.
