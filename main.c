#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <errno.h>
#include <unistd.h>
#include <limits.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>

#include "config.h"
#include "message.h"
#include "twinklsocket.h"

const char port[] = "1337";

int main(int argc, char *argv[])
{
	int twinklsocket;

	if(argc != 3) {
		fprintf(stderr,"usage: %s hostname priority\n", argv[0]);
		exit(1);
	}

	twinklsocket = twinklsocket_open(argv[1], port);

	struct twinkl_message msg;

	unsigned long priority;
	priority = strtoul(argv[2], NULL, 0);
	if(priority == ULONG_MAX || priority > TWINKL_LEVEL_COUNT) {
		fprintf(stderr, "Priority not in range 0..%d\n", TWINKL_LEVEL_COUNT);
		exit(1);
	}

	twinkl_init_message(&msg);
	twinkl_set_priority(&msg, priority);


	int linecount = 0;
	size_t len = 0;
	char *line = NULL;

	/*
	 * Line format: <channel> : <value>
	 * With abitrary many spaces btween the numbers and the colon
	 * Example: "5 :   42"
	 */
	while(!feof(stdin)) {
		
		// Try to read a line from stdin, if the line is empty send the packet
		if(getline(&line, &len, stdin) <= 1) {
			twinklsocket_send(twinklsocket, &msg);
			printf("Twinkl paket sent.\n");
			
			twinkl_init_message(&msg);
			twinkl_set_priority(&msg, priority);

			continue;
		}

		char *colon, *end;
		unsigned long chan, value; 

		linecount++;
		
		chan = strtoul(line, &end, 0);
		if(chan == ULONG_MAX || end == line) {
			fprintf(stderr, "Invalid channel number for line %d\n", linecount);
			continue;
		}
		if(chan > TWINKL_CHANNEL_COUNT) {
			fprintf(stderr, "Channel number %lu not in range 0..%d for line %d\n",
				chan, 
				TWINKL_CHANNEL_COUNT - 1, 
				linecount);

			continue;
		}
	
		colon = strchr(end, ':');
		if(colon == NULL) {
			fprintf(stderr, "Missing delimiter in line %d\n", linecount);
			continue;
		}

		// First char after the colon is value
		value = strtoul(colon + 1, &end, 0);
		if(value == ULONG_MAX || end == colon + 1) {
			fprintf(stderr, "Invalid value for line %d\n", linecount);
			continue;
		}
		if(value > 255) {
			fprintf(stderr, "Value %lu for channel %lu is not in range 1..255 in line %d\n",
				value,
				chan,
				linecount);

			continue;
		}

		if(*end != '\n') {
			fprintf(stderr, "Unecessary characters after value in line %d\n", linecount);
			continue;
		}

		twinkl_set_value(&msg, chan, value);
	}

	free(line);

	twinklsocket_close(twinklsocket);
	return 0;
}
