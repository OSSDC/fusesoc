#Generated by FuseSoC
CC ?= gcc
CFLAGS := -c -std=c99 -fPIC -fno-stack-protector -g -m32

LD ?= ld
LDFLAGS := -shared -E -melf_i386

RM ?= rm
INCS := -I$(MODEL_TECH)/../include

all: elf-loader_0

clean: clean_elf-loader_0

elf-loader_0_ROOT := ../../../cores/elf-loader
elf-loader_0_OBJS := elf-loader.o vpi_wrapper.o
elf-loader_0_LIBS := -lelf
elf-loader_0_INCS := $(INCS) 

$(elf-loader_0_OBJS): %.o : $(elf-loader_0_ROOT)/%.c
	$(CC) $(CFLAGS) $(elf-loader_0_INCS) $<

elf-loader_0: $(elf-loader_0_OBJS)
	$(LD) $(LDFLAGS) -o $@ $? $(elf-loader_0_LIBS)

clean_elf-loader_0:
	$(RM) $(elf-loader_0_OBJS) elf-loader_0
