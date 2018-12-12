HACKING
=================================
If you want to help, here's how.

### Dependencies

- Ubuntu 16.04 (not technically required, but bash scripts might need tweaking other distros/versions)
- Docker


### Installation
Right now, I got it running in docker. (Which is admittedly a little weird for a UI app, but go with it.)

Just do:
```
./run.sh
```

This will build and run the game. If it doesn't work, it's probably a problem with mounting the X11 DISPLAY or `/dev/snd` -- you'll need to tweak the docker run command for your system.

### Development
```
./dev.sh
```
This mounts the current directory inside the container so that changes are reflected inside. So you can make a change and run the game in a tight loop.

### Map Editor
```
./map.sh
```

It's also available from within the dev container.


### Coding Style
As much as we can, we're trying to use [the Google Python Style Guide](https://google-styleguide.googlecode.com/svn/trunk/pyguide.html)

As the project gets underway, we'll focus on unit testing and PEP8 linting.


### Level Editor
We are using Tiled.  See [here](http://www.mapeditor.org/)
