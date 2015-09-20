#ifndef _TWINKLSOCKET_H
#define _TWINKLSOCKET_H

#include "message.h"

extern int twinklsocket_open(const char *host, const char *port);

extern void twinklsocket_send(int sockfd, const struct twinkl_message *message);

extern void twinklsocket_close(int sockfd);

#endif
