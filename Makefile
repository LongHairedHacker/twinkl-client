TARGET = twinkl-client
SRC = main.c twinklsocket.c
HEADERS = include/twinklsocket.h 
OBJDIR = bin

CC = clang
CFLAGS = -Wall -O2 -I include -I twinkl/include 
LDFLAGS = 

OBJ = $(SRC:%.c=$(OBJDIR)/%.o)


all : start $(OBJDIR)/$(TARGET)
	@echo ":: Done !"

start :
	@echo "twinkl-client"
	@echo "============="
	@echo ":: Building using $(CC)"
	@echo ":: Twinkl revision $(shell cd twinkl; git rev-parse --short HEAD)"
	@echo ":: Twinkel-client revision $(shell git rev-parse --short HEAD)"


$(OBJDIR)/%.o : %.c Makefile $(HEADERS)
	mkdir -p $$(dirname $@)
	$(CC) $(CFLAGS) -c $< -o $@

$(OBJDIR)/$(TARGET) : $(OBJ)
	$(CC) $+ $(LDFLAGS) -o $@

clean :
	@rm -rf $(OBJDIR)

run : $(OBJDIR)/$(TARGET)
	$(OBJDIR)/$(TARGET)
