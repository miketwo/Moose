Moose On The Move
=================

**The following will be a complete rambling stream of conciousness until I can organize it better.**

I want to create a top-down, 2d arcade game in which you walk a dog.  Not just any dog, but my dog -- Sheamus Jefferson Cooper III ("Moose"). He's a crazyface snugglebug, and that's what will make this fun.

The player will be connected to the dog by a leash, but will only have control over the player. The dog will do its own thing. The goal of each level is to reach the end within the time allotted. Too much time and you'll be late for work.

Game Mechanics
--------------
Moose is attracted to trees, squirrels, cats, birds, hydrants, people, and anything else I might add in the future. I will probably model the attraction using a magnetic model (a function of r-squared). Points are awarded for marking territory (trees/hydrants), and damage occurs when the dog attacks anything (people, cats, squirrels).  Different things have varying levels of attractiveness to the dog.

The player is connected to the dog via a leash, and this leash can get caught on things.  It can also be let out or reeled in.  The leash mechanics will probably be the most complicated part of the game.

A whistle is a multi-use rechargeable powerup that calls the dog back to you. The whistle recharges slowly, and although it can be used at any time, if it's not at full power, the dog won't come all the way back.

A treat bag is used for keeping the dog very close to the player.  It's a mutli-use, fuel-gauge style powerup. Once it's empty, it can no longer be used.  The dog stays in close proximity so long as treats are being shoved down his throat.

The Ball is the ultimate powerup - like a star in Mario. When used, the dog returns, is unleashed, and then the player can use the mouse to throw the ball anywhere on the screen.  Moose chases the ball, ignoring all other distractions, and then returns it to the player, again ignoring distractions. This allows for gameplay in which the player must run through an obstacle course in the time it takes for the dog to retrieve a ball.

Leash Mechanics
---------------
The leash will probably have to be modelled with a full physics engine in order to make it look good. It can get caught on things, and can also clothesline things (like maybe a flock of birds or something).  Getting caught is punishment in the form of lost time, clotheslining birds is extra points, but clotheslining people is damage to the player.  We want to encourage a long, loose leash, as that gives the dog AI more ability to surprise the player.  So there's a minimum length below which the dog will not come in.

The dog is stronger than the player and can drag him while chasing a cat.  Though for small distractions like trees and hydrants, the dog only slows the player down a bit.

I'm taking some inspiration here on the leash mechanics from the excellent Cut The Rope game. AFAIK, they used Box2d. I'm going to experiment with pymunk and pybox2d.

Training
--------
I want there to be training minigames that can be accessed between rounds to make the dog better behaved.  Not sure yet how this should play out...

Saving
------
Checkpoints are standard errand destinations, like coffeeshops or banks. Approaching these will cause an animation of tieing the dog to a tree and walking inside. Then we save the player's progress.

Momentum
--------
The momentum of the game should never stop, and we should be able to play fast or slow, similar to Mario. Puzzles in the game should be obvious, but require special timing to complete.  No brain teasers or complex sequences. The dog needs to be well tuned so that it can keep up with a running player (marking trees without slowing the player down), but not hyperactive so that a slower player feels overwhelmed.

Walls
-----
    - Impermeable: parked cars, fences. The street with moving cars can be an instant death zone to keep the map contained.

    - Semi-permeable: streams, mud, tall grass, construction zone ditches? (we'll need some more here). To make a variety of puzzles, we'll need things that only dogs can pass through, and things that only the player can pass through. Maybe a see-through bridge (dogs are scared of those).

    - Permeable: normal concrete, grass

Player Mechanics
----------------
Player can move in all cardinal directions using arrow keys. They can also run -- not sure if I want that to be a combo key (Shift + arrow) or a double-tapped arrow.

Levels
------
All levels (except some early training levels) are timed. We'll start with linear levels, but want to get bigger quickly (crossing streets, construction zones, dog parks).  Ideally during the later levels there will be many paths to complete the level.

[Level Editor](http://www.mapeditor.org/)


Contributing
------------
See [HACKING.md](HACKING.md)


Todo
----
    - stand up basic demo
    - get 1st unit test up
    - installation/usage instructions
    - setup pip packaging?
    - many other things...


Resources
---------
Box2d Ropes:
    - http://www.emanueleferonato.com/2009/10/05/basic-box2d-rope/
    - https://www.youtube.com/watch?v=3bpme0MsTYA
    - http://www.raywenderlich.com/14793/how-to-make-a-game-like-cut-the-rope-part-1

PyMunk
    - https://github.com/viblo/pymunk
    - Discussion on ropes/chains: http://www.idevgames.com/forums/thread-8631.html

MVC Pattern applied to Pygame
    - http://ezide.com/games/writing-games.html

Map Editor
    - http://www.mapeditor.org/

Notes
-----

Installing pygame in virtualenv is a pain, I need to switch to Virtualbox.


