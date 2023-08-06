It's a Live
===========

It's a Live is a utility that helps you make live coding demos less error-prone by taking the "live" component and
killing it.


Installation
------------

You can install It's a Live with pip:

```
pip install itsalive
```


Usage
-----

Using It's a Live is pretty simple:
Just write some keystrokes or commands in a file and run `itsalive` with it:

```
itsalive <command_file>
```

It's a Live will wait for you to press a key, and, when you do, it will instead emit one character from the command
file. This way, you can type whatever old crap and it will look perfectly rehearsed, every time, with no backspaces
(unless you add them in).  It will also wait for you to press Enter at the end of commands, so you will never skip
ahead to the next command by mistake.

What's more, It's a Live is actually running the commands you're typing, so you have full interoperability with other
programs.

It's a Live also supports various commands:

* `Ctrl+d` will immediately terminate the playback.
* `Ctrl+p` will pause automatic playback and give you control of the terminal. This is useful for doing actually live
  stuff, just make sure to leave everything in a state so that playback can resume later.
* `Ctrl+f` will skip forward to the next command.
* `Ctrl+b` will skip back to the previous command.
* `Ctrl+u` will send a `Ctrl+u` keystroke (wiping anything on to the left of the cursor) and rewind the current command.


More stuff
----------

It's a Live supports sending the commands via UDP to another window, so you can see what will be typed while you
present. To see the commands, run netcat in UDP server mode on port 5345:

```
nc -kul 5345
```

If you want to leave yourself notes, you can add comments to the command file. Comments must start with `##` as the
first thing on the line, and they will not be typed. They will only be sent via UDP to the listening server.


License
-------

It's a Live is licensed under the GPL v3 or any later version.
