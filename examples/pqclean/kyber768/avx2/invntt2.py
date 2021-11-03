#!/usr/bin/python3

zeta     = 1678
R        = 2**16
Q        = 3329
QINV     = -3327  # mod R
MONT     = -1044  # R mod Q
V        = 20159  # floor(2^26/q + 0.5)
FHI      = 1441   # mont^2/128
FLO      = -10079 # qinv*FHI
MONTSQHI = 1353   # mont^2
MONTSQLO = 20553  # qinv*MONTSQHI
MASK     = 4095
SHIFT    =   32

input_base = 0x7fffffffaee0
const_base = 0x5555556395e0
output_base = 0x7fffffffaee0

consts = [       Q, Q, Q, Q, Q, Q, Q, Q, Q, Q, Q, Q, Q, Q, Q, Q,

# //#define _16XQINV 16
        QINV, QINV, QINV, QINV, QINV, QINV, QINV, QINV,
        QINV, QINV, QINV, QINV, QINV, QINV, QINV, QINV,

# //#define _16XV 32
        V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V,

# //#define _16XFLO 48
        FLO, FLO, FLO, FLO, FLO, FLO, FLO, FLO,
        FLO, FLO, FLO, FLO, FLO, FLO, FLO, FLO,

# //#define _16XFHI 64
        FHI, FHI, FHI, FHI, FHI, FHI, FHI, FHI,
        FHI, FHI, FHI, FHI, FHI, FHI, FHI, FHI,

# //#define _16XMONTSQLO 80
        MONTSQLO, MONTSQLO, MONTSQLO, MONTSQLO,
        MONTSQLO, MONTSQLO, MONTSQLO, MONTSQLO,
        MONTSQLO, MONTSQLO, MONTSQLO, MONTSQLO,
        MONTSQLO, MONTSQLO, MONTSQLO, MONTSQLO,

# //#define _16XMONTSQHI 96
        MONTSQHI, MONTSQHI, MONTSQHI, MONTSQHI,
        MONTSQHI, MONTSQHI, MONTSQHI, MONTSQHI,
        MONTSQHI, MONTSQHI, MONTSQHI, MONTSQHI,
        MONTSQHI, MONTSQHI, MONTSQHI, MONTSQHI,

# //#define _16XMASK 112
        MASK, MASK, MASK, MASK, MASK, MASK, MASK, MASK,
        MASK, MASK, MASK, MASK, MASK, MASK, MASK, MASK,

# //#define _REVIDXB 128
        3854, 3340, 2826, 2312, 1798, 1284, 770, 256,
        3854, 3340, 2826, 2312, 1798, 1284, 770, 256,

# //#define _REVIDXD 144
        7, 0, 6, 0, 5, 0, 4, 0, 3, 0, 2, 0, 1, 0, 0, 0,

# //#define _ZETAS_EXP 160
        31498,  31498,  31498,  31498,   -758,   -758,   -758,   -758,
        5237,   5237,   5237,   5237,   1397,   1397,   1397,   1397,
        14745,  14745,  14745,  14745,  14745,  14745,  14745,  14745,
        14745,  14745,  14745,  14745,  14745,  14745,  14745,  14745,
        -359,   -359,   -359,   -359,   -359,   -359,   -359,   -359,
        -359,   -359,   -359,   -359,   -359,   -359,   -359,   -359,
        13525,  13525,  13525,  13525,  13525,  13525,  13525,  13525,
        -12402, -12402, -12402, -12402, -12402, -12402, -12402, -12402,
        1493,   1493,   1493,   1493,   1493,   1493,   1493,   1493,
        1422,   1422,   1422,   1422,   1422,   1422,   1422,   1422,
        -20907, -20907, -20907, -20907,  27758,  27758,  27758,  27758,
        -3799,  -3799,  -3799,  -3799, -15690, -15690, -15690, -15690,
        -171,   -171,   -171,   -171,    622,    622,    622,    622,
        1577,   1577,   1577,   1577,    182,    182,    182,    182,
        -5827,  -5827,  17363,  17363, -26360, -26360, -29057, -29057,
        5571,   5571,  -1102,  -1102,  21438,  21438, -26242, -26242,
        573,    573,  -1325,  -1325,    264,    264,    383,    383,
        -829,   -829,   1458,   1458,  -1602,  -1602,   -130,   -130,
        -5689,  -6516,   1496,  30967, -23565,  20179,  20710,  25080,
        -12796,  26616,  16064, -12442,   9134,   -650, -25986,  27837,
        1223,    652,   -552,   1015,  -1293,   1491,   -282,  -1544,
        516,     -8,   -320,   -666,  -1618,  -1162,    126,   1469,
        -335, -11477, -32227,  20494, -27738,    945, -14883,   6182,
        32010,  10631,  29175, -28762, -18486,  17560, -14430,  -5276,
        -1103,    555,  -1251,   1550,    422,    177,   -291,   1574,
        -246,   1159,   -777,   -602,  -1590,   -872,    418,   -156,
        11182,  13387, -14233, -21655,  13131,  -4587,  23092,   5493,
        -32502,  30317, -18741,  12639,  20100,  18525,  19529, -12619,
        430,    843,    871,    105,    587,   -235,   -460,   1653,
        778,   -147,   1483,   1119,    644,    349,    329,    -75,
        787,    787,    787,    787,    787,    787,    787,    787,
        787,    787,    787,    787,    787,    787,    787,    787,
        -1517,  -1517,  -1517,  -1517,  -1517,  -1517,  -1517,  -1517,
        -1517,  -1517,  -1517,  -1517,  -1517,  -1517,  -1517,  -1517,
        28191,  28191,  28191,  28191,  28191,  28191,  28191,  28191,
        -16694, -16694, -16694, -16694, -16694, -16694, -16694, -16694,
        287,    287,    287,    287,    287,    287,    287,    287,
        202,    202,    202,    202,    202,    202,    202,    202,
        10690,  10690,  10690,  10690,   1358,   1358,   1358,   1358,
        -11202, -11202, -11202, -11202,  31164,  31164,  31164,  31164,
        962,    962,    962,    962,  -1202,  -1202,  -1202,  -1202,
        -1474,  -1474,  -1474,  -1474,   1468,   1468,   1468,   1468,
        -28073, -28073,  24313,  24313, -10532, -10532,   8800,   8800,
        18426,  18426,   8859,   8859,  26675,  26675, -16163, -16163,
        -681,   -681,   1017,   1017,    732,    732,    608,    608,
        -1542,  -1542,    411,    411,   -205,   -205,  -1571,  -1571,
        19883, -28250, -15887,  -8898, -28309,   9075, -30199,  18249,
        13426,  14017, -29156, -12757,  16832,   4311, -24155, -17915,
        -853,    -90,   -271,    830,    107,  -1421,   -247,   -951,
        -398,    961,  -1508,   -725,    448,  -1065,    677,  -1275,
        -31183,  25435,  -7382,  24391, -20927,  10946,  24214,  16989,
        10335,  -7934, -22502,  10906,  31636,  28644,  23998, -17422,
        817,    603,   1322,  -1465,  -1215,   1218,   -874,  -1187,
        -1185,  -1278,  -1510,   -870,   -108,    996,    958,   1522,
        20297,   2146,  15355, -32384,  -6280, -14903, -11044,  14469,
        -21498, -20198,  23210, -17442, -23860, -20257,   7756,  23132,
        1097,    610,  -1285,    384,   -136,  -1335,    220,  -1659,
        -1530,    794,   -854,    478,   -308,    991,  -1460,   1628,

# //#define _16XSHIFT 624
        SHIFT, SHIFT, SHIFT, SHIFT, SHIFT, SHIFT, SHIFT, SHIFT,
        SHIFT, SHIFT, SHIFT, SHIFT, SHIFT, SHIFT, SHIFT, SHIFT
]

def num_to_bits (n, w):
    r = []
    for i in range (w):
        r.append (n % 2)
        n //= 2
    return (r)

def bits_to_num (l):
    r = 0
    for i in range (len(l) - 1, -1, -1):
        r = r * 2 + l[i]
    return (r)

# convert ymm registers of the given indices to coefficient list
def ymm2coeffs (indices, slice_size):
    idxs = []
    for i in range (len (indices)):
        cur = []
        for j in range (16):
            cur.append ('ymm' + str(indices[i]) + '_' + '{0:x}'.format (j))
        idxs.append (cur)
    ret = []
    for k in range (16//slice_size):
        for i in range (len (indices)):
            ret = ret + idxs[i][(k*slice_size):((k+1)*slice_size)]
    return (ret)

def coeff_bounds (bounds, slice_size):
    idxs = []
    for i in range (len (bounds)):
        cur = [ bounds[i] for j in range (16)]
        idxs.append (cur)
    ret = []
    for k in range (16//slice_size):
        for i in range (len (bounds)):
            ret = ret + idxs[i][(k*slice_size):((k+1)*slice_size)]
    return (ret)

# kyber768 uses 7-level invntt with 128 linear polynomials

def print_inputs (cname):
    print ('bit x,')
    for i in range (0, 256, 4):
        print ('sint16 {0}{1:03}, sint16 {0}{2:03}, sint16 {0}{3:03}, sint16 {0}{4:03}{5}'.
               format (cname, i, i+1, i+2, i+3, ',' if i < 256 - 4 else ''))

def print_ghosts (poly_name):
    for i in range (128):
        print ('{0}{1:02x}@bit'.format (poly_name, i),
               end = '\n' if i == 127 else
                     (',\n' if i % 4 == 3 else ', '))
        
def print_range_precondition (cname):
    for i in range (0, 256, 2):
        print ('({0})@16 <s {4}{1:03}, {4}{1:03} <s ({3})@16, ({0})@16 <s {4}{2:03}, {4}{2:03} <s ({3})@16{5}'.
               format (-Q, i, i+1, Q, cname, ',' if i < 256 - 2 else ''))
    
        
def print_initialization (cname):
    for i in range (0, 256 - 3, 3):
        print ('mov L0x{0:x} {6}{1:03}; mov L0x{2:x} {6}{3:03};  mov L0x{4:x} {6}{5:03};'.
               format (input_base + i * 2, i,
                       input_base + (i+1)*2, i+1,
                       input_base + (i+2)*2, i+2, cname))
    for i in range (i + 3, 256):
        print ('mov L0x{0:x} {2}{1:03};'.
               format (input_base + i * 2, i, cname), end=' ')
    
def print_consts ():
    for i in range (0, len (consts), 2):
        print ('mov L0x{0:x} ({1:6d})@sint16; mov L0x{2:x} ({3:6d})@sint16;'.
               format (const_base + i * 2, consts [i],
                       const_base + (i+1)*2, consts [i+1]))

def print_inp_poly (poly_name, cname, offset):
    exps = [ i for i in range (64) ]
    exprevbits = map (lambda e : [1, offset] + list (reversed (num_to_bits (e, 6))),
                      exps)
    revexps = list (map (lambda b : (zeta**(bits_to_num (b)*(Q-1)//256))%Q, exprevbits))
    for i in range (64):
        print ('eqmod ({0}{1:02x}**2) ({2}{3:03} + {2}{4:03}*x) [{5}, x**2 - {6}]'.
               format (poly_name, i + 64*offset, cname,
                       i//4+(i*32)%128+128*offset,
                       i//4+(i*32)%128+16+128*offset,
                       Q, revexps[i]),
               end = '\n' if i == 63 else ',\n')

def print_range_condition (indices, slice_size, bounds):
    coefficients = ymm2coeffs (indices, slice_size)
    print ('and [')
    for i in range (len (coefficients)):
        print ('({0})@16 <s {1}, {1} <s ({2})@16{3}'.
               format (-bounds[i % len (bounds)],
                        coefficients[i],
                        bounds[i % len (bounds)],
                       ',' if i < len (coefficients) - 1 else ']'))
        
def print_algebraic_condition (poly_name, indices, slice_size, level, offset):
    exps = [ i for i in range (64) ]
    exprevbits = map (lambda e : [1, offset] + list (reversed (num_to_bits (e, 6))),
                      exps)
    revexps = list (map (lambda b : (zeta**(bits_to_num (b)*(Q-1)//256))%Q, exprevbits))
    coefficients = ymm2coeffs (indices, slice_size)
    factor = 2**(10+level)
    degree = 2**(2+level)
    print ('and [')
    for i in range (64):
        modulus = revexps[i]
        coeffidx = degree * (i//(degree//2))
        print ('eqmod ({0}*({1}{2:02x}**2))'.
               format (factor, poly_name, i + 64*offset))
        for j in range (0, degree):
            print ('{2}{0}*(x**{1})'.
                   format (coefficients[coeffidx], j,
                           '(' if j == 0 else ''),
                   end = ')\n' if j == degree - 1 else
                              (' +\n ' if j % 4 == 3 else ' + '))
            coeffidx += 1
        print ('[{0}, x**2 - {1}]'.format (Q, modulus),
               end = ',\n' if i < 63 else ']\n')

def _print_algebraic_condition5 (poly_name, offset):
    exps = [ i for i in range (64) ]
    exprevbits = map (lambda e : [1, offset] + list (reversed (num_to_bits (e, 6))),
                      exps)
    revexps = list (map (lambda b : (zeta**(bits_to_num (b)*(Q-1)//256))%Q, exprevbits))
    factor = 2**15
    print ('and [')
    for i in range (64):
        modulus = revexps[i]
        print ('eqmod ({0}*({1}{2:02x}**2))'.
               format (factor, poly_name, i + 64*offset))
        for j in range (128):
            print ('{0}L0x{1:x}*(x**{2})'.
                   format ('(' if j == 0 else ' ', output_base + j*2 + offset * 256, j),
                   end = ')\n' if j == 127 else
                         (' +\n' if j % 3 == 2 else ' +'))
        print ('[{0}, x**2 - ({1})]'.format (Q, modulus),
               end = ',\n' if i < 63 else ']\n')

def print_condition5_ghosts (poly_name, offset):
    for i in range (4):
        print ('{0}{1}**2 ='.format (poly_name, i))
        for j in range (128//4):
            print ('L0x{0:x}*(x**{1})'.
                   format (output_base + i*(128//4)*2 + j*2 + offset*256, j),
                   end = '\n' if j == 128//4 - 1 else
                         ('+\n' if j % 3 == 2 else '+'))
        print (',' if i < 3 else '')
        
def print_algebraic_condition5 (poly_name, ghost_name, offset):
    exps = [ i for i in range (64) ]
    exprevbits = map (lambda e : [1, offset] + list (reversed (num_to_bits (e, 6))),
                      exps)
    revexps = list (map (lambda b : (zeta**(bits_to_num (b)*(Q-1)//256))%Q, exprevbits))
    factor = 2**15
    print ('and [')
    print_condition5_ghosts (ghost_name, offset)
    print (',')
    for i in range (64):
        modulus = revexps[i]
        print ('eqmod ({0}*({1}{2:02x}**2))'.
               format (factor, poly_name, i + 64*offset))
        print ('(', end = '')
        for j in range (4):
            print ('({0}{1}**2)*(x**{2})'.
                   format (ghost_name, j, j*128//4),
                   end = ')\n' if j == 3 else ' + ')
        print ('[{0}, x**2 - ({1})]'.format (Q, modulus),
               end = ',\n' if i < 63 else ']\n')
        
def print_algebraic_condition6 (poly_name):
    exps = [ i for i in range (128) ]
    exprevbits = map (lambda e : [1] + list (reversed (num_to_bits (e, 7))),
                      exps)
    revexps = list (map (lambda b : (zeta**(bits_to_num (b)*(Q-1)//256))%Q, exprevbits))
    factor = 2**16
    print ('and [')
    for i in range (128):
        print ('eqmod ({0}*({1}{2:02x}**2))'.format (factor, poly_name, i))
        for j in range (256):
            print ('{0}L0x{1:x}*(x**{2})'.
                   format ('(' if j == 0 else ' ', output_base + j*2, j),
                   end = ')\n' if j == 255 else
                         (' +\n' if j % 3 == 2 else ' +'))
        print ('[{0}, x**2 - ({1})]'.format (Q, revexps[i]),
               end = ',\n' if i < 127 else ']\n')

def print_range_condition6 (bound):
    print ('and [')
    for i in range (256):
        print ('(-{0})@16 <s L0x{1:x}, L0x{1:x} <s ({0})@16'.
               format (bound, output_base + i*2),
               end = ']' if i == 255 else
                     (',\n' if i % 3 == 2 else ', '))

print ('(*********** parameters ***********)\n\n\n')
print_inputs ('c')

print ('\n\n\n(*********** precondition ***********)\n\n\n')
print ('true && and [')
print_range_precondition ('c')
print (']')
               
print ('\n\n\n(*********** initialization ***********)\n\n\n')
print_initialization ('c')

print ('\n\n\n(*********** constants ***********)\n\n\n')
print_consts()

print ('\n\n\n(************* ghosts ************)\n\n\n')
print ('ghost ')
print_ghosts ('inp_poly')
print (' : and [')
print_inp_poly ('inp_poly', 'c', 0)
print (',')
print_inp_poly ('inp_poly', 'c', 1)
print ('] && true;')

print ('\n\n\n(*********** CUT 0, - ***********)\n\n\n')
print ('ecut and [')
print_inp_poly ('inp_poly', 'c', 0)
print ('] prove with [ precondition ];')

print ('\n\n\n(*********** CUT 1, - ***********)\n\n\n')
print ('ecut and [')
print_inp_poly ('inp_poly', 'c', 1)
print ('] prove with [ precondition ];')

print ('\n\n\n(*********** SUMMARY OF LEVEL 0 0 **********)')
print ('(****************** CUT 2, - ******************)\n\n\n')
print ('ecut ')
print_algebraic_condition ('inp_poly', [4, 5, 6, 7, 8, 9, 10, 11], 1,
                           0, 0)
print ('prove with [ cuts [ 0 ] ];')

print ('\n\n\n(*********** SUMMARY OF LEVEL 1 0 **********)')
print ('(****************** CUT 3, - ******************)\n\n\n')
print ('ecut ')
print_algebraic_condition ('inp_poly', [3, 4, 6, 8, 5, 7, 9, 11], 2,
                           1, 0)
print (';')

print ('\n\n\n(*********** SUMMARY OF LEVEL 2 0 **********)')
print ('(****************** CUT 4, - ******************)\n\n\n')
print ('ecut ')
print_algebraic_condition ('inp_poly', [10, 3, 6, 5, 4, 8, 7, 11], 4,
                           2, 0)
print (';')

print ('\n\n\n(*********** SUMMARY OF LEVEL 3 0 **********)')
print ('(****************** CUT 5, - ******************)\n\n\n')
print ('ecut ')
print_algebraic_condition ('inp_poly', [9, 10, 6, 4, 3, 5, 8, 11], 8,
                           3, 0)
print (';')

print ('\n\n\n(*********** SUMMARY OF LEVEL 4 0 **********)')
print ('(****************** CUT 6, - ******************)\n\n\n')
print ('ecut ')
print_algebraic_condition ('inp_poly', [7, 9, 6, 3, 10, 4, 5, 11], 16,
                           4, 0)
print (';')

print ('\n\n\n(*********** SUMMARY OF LEVEL 5 0 **********)')
print ('(****************** CUT 7, - ******************)\n\n\n')
print ('ghost F0@bit, F1@bit, F2@bit, F3@bit : and [')
print_condition5_ghosts ('F', 0)
print ('] && true;')
print ('ecut ')
print_algebraic_condition5 ('inp_poly', 'F', 0)
print (';')

print ('\n\n\n(****************** CUT 8, - ******************)\n\n\n')
print ('ecut true;')

print ('\n\n\n(*********** SUMMARY OF LEVEL 0 1 **********)')
print ('(****************** CUT 9, - ******************)\n\n\n')
print ('ecut ')
print_algebraic_condition ('inp_poly', [4, 5, 6, 7, 8, 9, 10, 11], 1,
                           0, 1)
print ('prove with [ cuts [ 1 ] ];')

print ('\n\n\n(*********** SUMMARY OF LEVEL 1 1 **********)')
print ('(****************** CUT 10, - ******************)\n\n\n')
print ('ecut ')
print_algebraic_condition ('inp_poly', [3, 4, 6, 8, 5, 7, 9, 11], 2,
                           1, 1)
print (';')

print ('\n\n\n(*********** SUMMARY OF LEVEL 2 1 **********)')
print ('(****************** CUT 11, - *****************)\n\n\n')
print ('ecut ')
print_algebraic_condition ('inp_poly', [10, 3, 6, 5, 4, 8, 7, 11], 4,
                           2, 1)
print (';')

print ('\n\n\n(*********** SUMMARY OF LEVEL 3 1 **********)')
print ('(****************** CUT 12, - *****************)\n\n\n')
print ('ecut ')
print_algebraic_condition ('inp_poly', [9, 10, 6, 4, 3, 5, 8, 11], 8,
                           3, 1)
print (';')

print ('\n\n\n(*********** SUMMARY OF LEVEL 4 1 **********)')
print ('(****************** CUT 13, - *****************)\n\n\n')
print ('ecut ')
print_algebraic_condition ('inp_poly', [7, 9, 6, 3, 10, 4, 5, 11], 16,
                           4, 1)
print (';')

print ('\n\n\n(*********** SUMMARY OF LEVEL 5 1 **********)')
print ('(****************** CUT 14, - *****************)\n\n\n')
print ('ghost G0@bit, G1@bit, G2@bit, G3@bit : and [')
print_condition5_ghosts ('G', 1)
print ('] && true;')
print ('ecut ')
print_algebraic_condition5 ('inp_poly', 'G', 1)
print (';')

print ('\n\n\n(*********** SUMMARY OF LEVEL 6 **********)')
print ('(****************** CUT 15, 0 *****************)\n\n\n')
print ('cut')
print_algebraic_condition6 ('inp_poly')
print (' prove with [ cuts [ 7 ] ] &&')
print_range_condition6 (8*Q)
print ('\nprove with [ precondition ];')

print ('\n\n\n(*********** postcondition **********)\n\n\n')
print_algebraic_condition6 ('inp_poly')
print ('&&')
print_range_condition6 (8*Q)
