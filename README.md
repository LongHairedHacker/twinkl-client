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

twinklclient.so
===============
If you like to use your stdout for other things then piping data to the
twinkl client binary you should consider using the twinkl client library.

It offers the following functions:
```C
/*
 * Functions for handling sockets
 */

// Opens a 'connected' upd socket for this host and port, returns the filedescriptor
int twinklsocket_open(const char *host, const char *port);

// Sends a twinkl message
void twinklsocket_send(int sockfd, const struct twinkl_message *message);

// Closes the socket
void twinklsocket_close(int sockfd);


/*
 * Wrappers for handling twinkl messages
 */

// Allocates memory for a twinkl message, returns the pointer
twinkl_message* twinklmsg_create();

// Reset a message to 0 (wrapper for memset)
void twinklmsg_reset(struct twinkl_message *msg);

// Sets the value and marks the channel as 'used' for messages priority level
void twinklmsg_set_value(struct twinkl_message *msg, uint16_t chan, uint8_t value);

// Resets the channel to 0 and unsets the 'used' flag
void twinklmsg_unset_value(struct twinkl_message *msg, uint16_t chan);

// Sets the priority level for the message
void twinklmsg_set_priority(struct twinkl_message *msg, uint8_t priority);

// Free the memory allocated for the message
void twinklmsg_destroy(struct twinkl_message* msg);
```

To use it from C just include `twinklsocket.h` and `message.h`,
then link against `twinklclient.so`.
Keep in mind that there is no need to use the wrapper functions for twinkl
messages included in `twinklclient.so`.
Just directly us the ones in `message.h` as they can be inlined by your compiler
for better performance.
Keep in mind that the functions in `twinklclient.so` are named different than the ones
in `message.h` to avoid accidentally using the slower versions. 

To use the twinkl client library in other languages than C,
the message wrapper function can be used to take of allocating,
deallocating and modifing twinkl messages.
This is especially usefull for languages without a concept for direct memory
management like python.
Using the wrapper functions it is only necessary to deal with integers and pointers
(which can be represented as integers as well).
See `animations/twinklclient.py` and the example below for details.

```C
twinkl_server = "127.0.0.1"
port = "1337";

fd = twinklsocket_open(twinkl_server, port)

msg = twinklmsg_create()

twinklmsg_set_priority(msg, 0);

twinklmsg_set_value(msg, 23, 42);
twinklmsg_set_value(msg, 46, 5);
// ... more stuff

twinklsocket_send(fd, msg);

// Tear down

twinklsocket_close(fd);

twinklmsg_destroy(msg);
```
