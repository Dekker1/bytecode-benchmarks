#pragma once

#if defined(USE_DYNAMIC_TRACE)

#include <minizinc/support/dtrace_probes.h>

#define DTRACE_ENABLED(name) MINIZINC_##name##_ENABLED()
#define DTRACE0(name) MINIZINC_##name()
#define DTRACE1(name, a0) MINIZINC_##name(a0)
#define DTRACE2(name, a0, a1) MINIZINC_##name((a0), (a1))
#define DTRACE3(name, a0, a1, a2) MINIZINC_##name((a0), (a1), (a2))
#define DTRACE4(name, a0, a1, a2, a3) MINIZINC_##name((a0), (a1), (a2), (a3))
#define DTRACE5(name, a0, a1, a2, a3, a4) MINIZINC_##name((a0), (a1), (a2), (a3), (a4))

#else

#define DTRACE_ENABLED(name) 0
#define DTRACE0(name) \
  do {                \
  } while (0)
#define DTRACE1(name, a0) \
  do {                    \
  } while (0)
#define DTRACE2(name, a0, a1) \
  do {                        \
  } while (0)
#define DTRACE3(name, a0, a1, a2) \
  do {                            \
  } while (0)
#define DTRACE4(name, a0, a1, a2, a3) \
  do {                                \
  } while (0)
#define DTRACE5(name, a0, a1, a2, a3, a4) \
  do {                                    \
  } while (0)

#endif
