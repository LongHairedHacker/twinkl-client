twinkl-client
=============

Compile
-------
```
git clone git@github.com:LongHairedHacker/twinkl-client.git
cd twinkl-client
git submodule init
git submodule update
make
```

Usage
-----
```
twinkle-client <twinkl server> <priority>
```

* **twinkle server**: The ip or hostname of the twinkl-server
* **priority**: Priority of your packet 0 is highest 7 is lowest

twinkl-client reads a list of channel value pairs from stdin.
One pair per line in the format `<channel> : <value>`.
Channels range from 0 to 511 while values range from 0 to 255.
Both can be entered in decimal or hexadecimal (prefix with *0x*).
An empty line sends the twinkl packet containing all values since the last empty line.
An EOF (Ctrl-D) also sends the twinkel packet and terminates the client.

Only channels that have been assigned a value before sending the packet will
be reserved for usage by your priority level.
This implies that if you want a channel to stay at 0 without a lower priority level
being able to override it you have to set it to 0 in every packet you send.
It is also a good Idea to send an empty packet (newline directly followed by a EOF) 
before killing the client, as it will clear any leftover reserved channels
for your priority level.


Example Animations
------------------
Some example animations can be found in the animation folder.
They can be connected to a twinkle-client process using a pipe.

* `randomvalues.py` Sets all channels to a random value and quits
* `fullwhite.py` Set the lightwall to full white (use *lightwall.lan* as host) and quits
* `gradient.py` Displays a red/green gradient on the lightwall and quits
* `matrix.py` Matrix animation for the lightwall (use *lightwall.lan* as host)

**Examples:**

```
python2 fullwithe.py | ../bin/twinkl-client lightwall.lan 7
python2 gradient.py | ../bin/twinkl-client lightwall.lan 7
python2 matrix.py | ../bin/twinkl-client lightwall.lan 7

python2 random.py | ../bin/twinkl-client ampel.lan 7
```
