from cffi import FFI

ffi = FFI()
ffi.cdef('''
    typedef ... magic_set;
    typedef struct magic_set *magic_t;
    magic_t magic_open(int);
    void magic_close(magic_t);
//  const char *magic_getpath(const char *, int);
    const char *magic_file(magic_t, const char *);
//  const char *magic_descriptor(magic_t, int);
    const char *magic_buffer(magic_t, const void *, size_t);
    const char *magic_error(magic_t);
    int magic_setflags(magic_t, int);
    int magic_load(magic_t, const char *);
    int magic_compile(magic_t, const char *);
    int magic_check(magic_t, const char *);
//  int magic_list(magic_t, const char *);
    int magic_errno(magic_t);
''')
ffi.set_source(
    'magicfile._libmagic',
    '#include <magic.h>',
    libraries=['magic'],
)

if __name__ == '__main__':
    ffi.compile()
