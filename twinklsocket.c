#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>

#include "twinklsocket.h"


int twinklsocket_open(const char *host, const char *port) {
	int sockfd;
	struct addrinfo hints, *servinfo, *p;
	int result;

	memset(&hints, 0, sizeof hints);
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_DGRAM;

	result = getaddrinfo(host, port, &hints, &servinfo);
	if(result != 0) {
		fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(result));
		exit(1);
	}

	// loop through all the results and make a socket
	for(p = servinfo; p != NULL; p = p->ai_next) {
		sockfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
		if(sockfd != -1) {
			break;
		}
	}

	if (p == NULL) {
		fprintf(stderr, "failed to create socket\n");
		exit(1);
	}
	
	result = connect(sockfd, p->ai_addr, p->ai_addrlen);
	if(result != 0) {
		perror("connect");
		exit(1);
	}

	freeaddrinfo(servinfo);	

	return sockfd;
}

void twinklsocket_send(int sockfd, const struct twinkl_message *message) {
	int numbytes;

	numbytes = send(sockfd, message, sizeof(struct twinkl_message), 0);
	if (numbytes == -1) {
		perror("sendto");
		exit(1);
	}
}

void twinklsocket_close(int sockfd) {
	close(sockfd);
}
