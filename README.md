# Laser Jetman

## Introduction
Laser Jetman is a short arcade shooter inspired by Defender by Williams Electronics (1981). It is written in Python and uses the Pyxel game engine.

You can play the game on itch.io [here](https://helpcomputer.itch.io/laser-jetman).

![](/images/prev01.gif?raw=true "")

## Dependencies
- [Python](https://www.python.org/) 3.7.10 or higher.
- [Pyxel](https://github.com/kitao/pyxel) 2.3.4 or higher.

## Build & Run
- Inside the "src" directory, run "python main.py"

## Controls
- WASD keys, Arrow keys, or gamepad D-pad to move.
- Left & Right to move and Up to use Jetpack.
- J key or gamepad Button 1 to fire laser.
- K key or gamepad Button 2 to exit in pause menu.
- Return key or gamepad button Start to pause.
- ESC key to exit.

## Comments
In this project I aimed to use no external assets. The sprites and sounds are created at run-time using Pyxel functions to import strings of data.

The terrain is generated using Perlin noise and most other effects use a particle emitter.

## Credits
- Game design and art by [badcomputer](https://twitter.com/badcomputer0)
- Font by [Damien Guard](https://damieng.com/)

## License
[MIT license](http://en.wikipedia.org/wiki/MIT_License)
