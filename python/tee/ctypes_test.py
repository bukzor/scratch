from ctypes import c_void_p
import ctypes.util
libc_path = ctypes.util.find_library('c')
print libc_path
libc = ctypes.cdll.LoadLibrary(libc_path)
print libc

for name in (
    'stdout',  # glibc
    '__stdoutp',  # darwin
):
    try:
        stdout = c_void_p.in_dll(libc, name)
    except ValueError:
        continue
    else:
        break

print stdout
