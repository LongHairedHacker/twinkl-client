#ifndef _TWINKLSOCKET_H
#define _TWINKLSOCKET_H

#include "message.h"

int twinklsocket_open(const char *host, const char *port);

int twinklsocket_send(int sockfd, const struct twinkl_message *message);

void twinklsocket_close(int sockfd);

#endif
