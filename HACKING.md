HACKING
=================================
If you want to help, here's how.

Pre-reqs
------------
You will need to have vagrant and virtualbox installed.

`apt-get vagrant virtualbox`

(Tested with vagrant 1.4.1 and VirtualBox 4.1.12_Ubuntu)


Setup Dev Environment
--------------------------
#. `cp Vagrantfile-template Vagrantfile`
#. Modify the Vagrantfile as necessary for your hardware (change memory, cpus, etc...)
#. `vagrant up`


Coding Style
---------------
As much as we can, we're trying to use [the Google Python Style Guide](https://google-styleguide.googlecode.com/svn/trunk/pyguide.html)

As the project gets underway, we'll focus on unit testing and PEP8 linting.


Level Editor
--------------
We are using Tiled.  See [here](http://www.mapeditor.org/)
