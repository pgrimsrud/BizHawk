AUTOMAKE_OPTIONS = subdir-objects
DEFS = -DLOCALEDIR=\"$(datadir)/locale\" @DEFS@  @MMX_CFLAGS@ @SSE_CFLAGS@ @SSE2_CFLAGS@ -funroll-loops
DEFAULT_INCLUDES = -I$(top_builddir)/include -I$(top_srcdir)/include -I$(top_srcdir)/intl

noinst_LIBRARIES	=	libpsx.a
libpsx_a_SOURCES 	= 	psx.cpp irq.cpp timer.cpp dma.cpp frontio.cpp sio.cpp cpu.cpp gte.cpp dis.cpp cdc.cpp spu.cpp mdec.cpp
libpsx_a_SOURCES	+=	gpu.cpp gpu_polygon.cpp gpu_line.cpp gpu_sprite.cpp
libpsx_a_SOURCES	+=	input/gamepad.cpp input/dualanalog.cpp input/dualshock.cpp input/memcard.cpp input/multitap.cpp input/mouse.cpp input/negcon.cpp input/guncon.cpp input/justifier.cpp

if WANT_DEBUGGER
libpsx_a_SOURCES	+=	debug.cpp
endif
