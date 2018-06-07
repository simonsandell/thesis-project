import os
import ycm_core

flags = [
        '-Wall',
        '-Wextra',
        '-Werror',
        '-Wno-long-long',
        '-Wno-variadic-macros',
        '-fexceptions',
        '-ferror-limit=10000',
        '-DNDEBUG',
        '-std=c++11',
        '-x c++',
        '-isystem/usr/include/c++/5.4.0',
        '-isystem/usr/include/x86_64-linux-gnu/c++/5.4.0',
        '-isystem/usr/include/c++/5.4.0/backward',
        '-isystem/usr/local/include',
        '-isystem/usr/lib/llvm-3.8/lib/clang/3.8.0/include',
        '-isystem/usr/include/x86_64-linux-gnu',
        '-isystem/usr/include/'
        ]

SOURCE_EXTENSIONS = [ '.cpp', '.cxx', '.cc', '.c', ]

def FlagsForFile( filename, **kwargs ):
    return {
            'flags':[ '-x', 'c++', '-Wall', '-Wextra', '-Werror' ]
            }
