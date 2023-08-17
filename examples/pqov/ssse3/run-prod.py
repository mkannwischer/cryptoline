#!/usr/bin/env python3

masks0 = [0x1,0x1,0x1,0x1,0x1,0x1,0x1,0x1,
          0x1,0x1,0x1,0x1,0x1,0x1,0x1,0x1]
masks1 = [0xf,0xf,0xf,0xf,0xf,0xf,0xf,0xf,
          0xf,0xf,0xf,0xf,0xf,0xf,0xf,0xf]
masks2 = [0xf0,0xf0,0xf0,0xf0,0xf0,0xf0,0xf0,0xf0,
          0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0]
masks3 = [0xf0,0xf0,0xf0,0xf0,0x0,0x0,0x0,0x0,
          0xf0,0xf0,0xf0,0xf0,0x0,0x0,0x0,0x0]
masks4 = [0xf0,0xf0,0x0,0x0,0xf0,0xf0,0x0,0x0,
          0xf0,0xf0,0x0,0x0,0xf0,0xf0,0x0,0x0]
masks5 = [0xf0,0x0,0xf0,0x0,0xf0,0x0,0xf0,0x0,
          0xf0,0x0,0xf0,0x0,0xf0,0x0,0xf0,0x0]
        
__gf256_mulbase = [0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07, 0x08,0x09,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f, 0x00,0x10,0x20,0x30,0x40,0x50,0x60,0x70, 0x80,0x90,0xa0,0xb0,0xc0,0xd0,0xe0,0xf0,
0x00,0x02,0x04,0x06,0x08,0x0a,0x0c,0x0e, 0x10,0x12,0x14,0x16,0x18,0x1a,0x1c,0x1e, 0x00,0x20,0x40,0x60,0x80,0xa0,0xc0,0xe0, 0x1b,0x3b,0x5b,0x7b,0x9b,0xbb,0xdb,0xfb,
0x00,0x04,0x08,0x0c,0x10,0x14,0x18,0x1c, 0x20,0x24,0x28,0x2c,0x30,0x34,0x38,0x3c, 0x00,0x40,0x80,0xc0,0x1b,0x5b,0x9b,0xdb, 0x36,0x76,0xb6,0xf6,0x2d,0x6d,0xad,0xed,
0x00,0x08,0x10,0x18,0x20,0x28,0x30,0x38, 0x40,0x48,0x50,0x58,0x60,0x68,0x70,0x78, 0x00,0x80,0x1b,0x9b,0x36,0xb6,0x2d,0xad, 0x6c,0xec,0x77,0xf7,0x5a,0xda,0x41,0xc1,
0x00,0x10,0x20,0x30,0x40,0x50,0x60,0x70, 0x80,0x90,0xa0,0xb0,0xc0,0xd0,0xe0,0xf0, 0x00,0x1b,0x36,0x2d,0x6c,0x77,0x5a,0x41, 0xd8,0xc3,0xee,0xf5,0xb4,0xaf,0x82,0x99,
0x00,0x20,0x40,0x60,0x80,0xa0,0xc0,0xe0, 0x1b,0x3b,0x5b,0x7b,0x9b,0xbb,0xdb,0xfb, 0x00,0x36,0x6c,0x5a,0xd8,0xee,0xb4,0x82, 0xab,0x9d,0xc7,0xf1,0x73,0x45,0x1f,0x29,
0x00,0x40,0x80,0xc0,0x1b,0x5b,0x9b,0xdb, 0x36,0x76,0xb6,0xf6,0x2d,0x6d,0xad,0xed, 0x00,0x6c,0xd8,0xb4,0xab,0xc7,0x73,0x1f, 0x4d,0x21,0x95,0xf9,0xe6,0x8a,0x3e,0x52,
0x00,0x80,0x1b,0x9b,0x36,0xb6,0x2d,0xad, 0x6c,0xec,0x77,0xf7,0x5a,0xda,0x41,0xc1, 0x00,0xd8,0xab,0x73,0x4d,0x95,0xe6,0x3e, 0x9a,0x42,0x31,0xe9,0xd7,0x0f,0x7c,0xa4]

def print_paramters (matA, b, c):
    for i in range (0x44):
        for j in range (0x2c):
            print ('uint8 {0}{1:02x}{2:02x}'.format (matA, i, j),
                   end = ',' if j%6 < 5 and j < 0x2b else ',\n')
    for j in range (0x2c):
        print ('uint8 {0}{1:02x}'.format (b, j),
               end = ',' if j%7 < 6 and j < 0x2b else
                     ',\n' if j < 0x2b else ';\n')
    for j in range (0x44):
        print ('uint8 {0}{1:02x}'.format (c, j),
               end = ',' if j%7 < 6 and j < 0x43 else
                     ',\n' if j < 0x43 else '\n')

def print_constants (base, vals):
    l = len (vals)
    for i in range (l):
        print ('mov L0x{0:x} (0x{1:02x})@uint8;'.format (base + i, vals[i]),
               end = '\n' if i%2 == 1 or i == l - 1 else ' ')

def print_nondet (base, l):
    for i in range (l):
        print ('nondet L0x{0:x}@uint8;'.format (base + i),
               end = '\n' if i % 2 == 1 or i == l - 1 else ' ')
    
def print_nondet_vec (n):
    print ('nondet m0@uint8;nondet m1@uint8;nondet m2@uint8;nondet m3@uint8;')
    print ('nondet m4@uint8;nondet m5@uint8;nondet m6@uint8;nondet m7@uint8;')
    print ('mov %{0} [m0, m1, m2, m3, m4, m5, m6, m7];'.format (n))

def print_initialization (base_matA, matA, base_b, b, base_c):
    for i in range (0x2c):
        for j in range (0x44):
            print ('mov L0x{0:x} {1}{2:02x}{3:02x};'.
                   format (base_matA + 0x44*i + j, matA, j, i),
                   end = '' if j%3 < 2 and j < 0x43 else '\n')
    for j in range (0x2c):
        print ('mov L0x{0:x} {1}{2:02x};'.
               format (base_b + j, b, j),
               end = ' ' if j%3 < 2 and j < 0x2b else '\n')
    for j in range (0x44):
        print ('nondet L0x{0:x}@uint8;'.format (base_c + j),
               end = ' ' if j%2 < 1 and j < 0x43 else '\n')

    for n in ['r8', 'r13', 'r15', 'rax', 'rcx', 'rdx', 'rdi', 'rsi']:
        print_nondet_vec (n)
    print_nondet (0x7fffffffc6e4, 12)
    print_nondet (0x7fffffffc684, 12)
    print_nondet (0x7fffffffc750, 4)

def print_outputs (base_c, c):
    for j in range (0x44):
        print ('mov {1}{2:02x} L0x{0:x};'.
               format (base_c + j, c, j),
               end = ' ' if j%3 < 2 and j < 0x43 else '\n')
    
print ('\n\n\n(*************** input parameters ***************)\n')
print_paramters ('A', 'b', 'c')

print ('\n\n\n(*************** constants ***************)\n')
print_constants (0x555555566020, masks0)
print_constants (0x555555566030, masks1)
print_constants (0x555555566040, masks2)
print_constants (0x555555566050, masks3)
print_constants (0x555555566060, masks4)
print_constants (0x555555566070, masks5)
print_constants (0x555555568080, __gf256_mulbase)

print ('\n\n\n(*************** initialization ***************)\n')
print_initialization (0x7ffff78bb030, 'A', 0x7fffffffcb00, 'b', 0x7fffffffcb80)

print ('\n\n\n(*************** outputs ***************)\n')
print_outputs (0x7fffffffcb80, 'c')

