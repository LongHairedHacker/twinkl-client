HEADERS = include/twinklsocket.h
HEADERS += twinkl/include/twinkl.h twinkl/include/config.h twinkl/include/message.h
OBJDIR = bin

CC = clang
CFLAGS = -fPIC -Wall -O2 -I include -I twinkl/include
LDFLAGS =


all : start $(OBJDIR)/twinkl-client
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

$(OBJDIR)/twinklsocket.so : $(OBJDIR)/twinklsocket.o
	$(CC) $+ -shared $(LDFLAGS) -o $@

$(OBJDIR)/twinkl-client : $(OBJDIR)/main.o $(OBJDIR)/twinklsocket.so
	$(CC) $+ $(LDFLAGS) -o $@

clean :
	@rm -rf $(OBJDIR)

run : $(OBJDIR)/$(TARGET)
	$(OBJDIR)/$(TARGET)
