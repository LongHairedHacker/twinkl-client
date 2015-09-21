#include "message.h"

#include <stdlib.h>

// Wrapper for the inline functions in message.h
// Also enforces a consistent naming scheme for symbols in twinklclient.so

struct twinkl_message* twinklmsg_create() {
	struct twinkl_message* msg = malloc(sizeof(struct twinkl_message));
	twinkl_init_message(msg);
	return msg;
}

void twinklmsg_reset(struct twinkl_message *msg) {
	twinkl_init_message(msg);
}

void twinklmsg_set_value(struct twinkl_message *msg, uint16_t chan, uint8_t value) {
	twinkl_set_value(msg, chan, value);
}

void twinklmsg_unset_value(struct twinkl_message *msg, uint16_t chan) {
	twinkl_unset_value(msg, chan);
}

void twinklmsg_set_priority(struct twinkl_message *msg, uint8_t priority) {
	twinkl_set_priority(msg, priority);
}

void twinklmsg_destroy(struct twinkl_message* msg) {
	free(msg);
}
