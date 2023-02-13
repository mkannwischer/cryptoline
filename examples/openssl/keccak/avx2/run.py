consts = [
#rhotates_left:
	3,	18,	36,	41,	# [2][0] [4][0] [1][0] [3][0]
	1,	62,	28,	27,	# [0][1] [0][2] [0][3] [0][4]
	45,	6,	56,	39,	# [3][1] [1][2] [4][3] [2][4]
	10,	61,	55,	8,	# [2][1] [4][2] [1][3] [3][4]
	2,	15,	25,	20,	# [4][1] [3][2] [2][3] [1][4]
	44,	43,	21,	14,	# [1][1] [2][2] [3][3] [4][4]
#rhotates_right:
	64-3,	64-18,	64-36,	64-41,
	64-1,	64-62,	64-28,	64-27,
	64-45,	64-6,	64-56,	64-39,
	64-10,	64-61,	64-55,	64-8,
	64-2,	64-15,	64-25,	64-20,
	64-44,	64-43,	64-21,	64-14,
#iotas:
	0x0000000000000001, 0x0000000000000001, 0x0000000000000001, 0x0000000000000001,
	0x0000000000008082, 0x0000000000008082, 0x0000000000008082, 0x0000000000008082,
	0x800000000000808a, 0x800000000000808a, 0x800000000000808a, 0x800000000000808a,
	0x8000000080008000, 0x8000000080008000, 0x8000000080008000, 0x8000000080008000,
	0x000000000000808b, 0x000000000000808b, 0x000000000000808b, 0x000000000000808b,
	0x0000000080000001, 0x0000000080000001, 0x0000000080000001, 0x0000000080000001,
	0x8000000080008081, 0x8000000080008081, 0x8000000080008081, 0x8000000080008081,
	0x8000000000008009, 0x8000000000008009, 0x8000000000008009, 0x8000000000008009,
	0x000000000000008a, 0x000000000000008a, 0x000000000000008a, 0x000000000000008a,
	0x0000000000000088, 0x0000000000000088, 0x0000000000000088, 0x0000000000000088,
	0x0000000080008009, 0x0000000080008009, 0x0000000080008009, 0x0000000080008009,
	0x000000008000000a, 0x000000008000000a, 0x000000008000000a, 0x000000008000000a,
	0x000000008000808b, 0x000000008000808b, 0x000000008000808b, 0x000000008000808b,
	0x800000000000008b, 0x800000000000008b, 0x800000000000008b, 0x800000000000008b,
	0x8000000000008089, 0x8000000000008089, 0x8000000000008089, 0x8000000000008089,
	0x8000000000008003, 0x8000000000008003, 0x8000000000008003, 0x8000000000008003,
	0x8000000000008002, 0x8000000000008002, 0x8000000000008002, 0x8000000000008002,
	0x8000000000000080, 0x8000000000000080, 0x8000000000000080, 0x8000000000000080,
	0x000000000000800a, 0x000000000000800a, 0x000000000000800a, 0x000000000000800a,
	0x800000008000000a, 0x800000008000000a, 0x800000008000000a, 0x800000008000000a,
	0x8000000080008081, 0x8000000080008081, 0x8000000080008081, 0x8000000080008081,
	0x8000000000008080, 0x8000000000008080, 0x8000000000008080, 0x8000000000008080,
	0x0000000080000001, 0x0000000080000001, 0x0000000080000001, 0x0000000080000001,
	0x8000000080008008, 0x8000000080008008, 0x8000000080008008, 0x8000000080008008
]

def header ():
    print ('proc main (')
    print ('uint64 A00, uint64 A01, uint64 A02, uint64 A03, uint64 A04,')
    print ('uint64 A10, uint64 A11, uint64 A12, uint64 A13, uint64 A14,')
    print ('uint64 A20, uint64 A21, uint64 A22, uint64 A23, uint64 A24,')
    print ('uint64 A30, uint64 A31, uint64 A32, uint64 A33, uint64 A34,')
    print ('uint64 A40, uint64 A41, uint64 A42, uint64 A43, uint64 A44')
    print (') =')
    print ('{ true && true }\n')

    print ('(* from keccak1600-avx2.pl ')
    print ('my ($A00,   # [0][0] [0][0] [0][0] [0][0]           # %ymm0')
    print ('    $A01,   # [0][4] [0][3] [0][2] [0][1]           # %ymm1')
    print ('    $A20,   # [3][0] [1][0] [4][0] [2][0]           # %ymm2')
    print ('    $A31,   # [2][4] [4][3] [1][2] [3][1]           # %ymm3')
    print ('    $A21,   # [3][4] [1][3] [4][2] [2][1]           # %ymm4')
    print ('    $A41,   # [1][4] [2][3] [3][2] [4][1]           # %ymm5')
    print ('    $A11) = # [4][4] [3][3] [2][2] [1][1]           # %ymm6')
    print ('*)\n')

    print ('mov ymm0_0 A00; mov ymm0_1 A00; mov ymm0_2 A00; mov ymm0_3 A00;')
    print ('mov ymm1_0 A01; mov ymm1_1 A02; mov ymm1_2 A03; mov ymm1_3 A04;')
    print ('mov ymm2_0 A20; mov ymm2_1 A40; mov ymm2_2 A10; mov ymm2_3 A30;')
    print ('mov ymm3_0 A31; mov ymm3_1 A12; mov ymm3_2 A43; mov ymm3_3 A23;')
    print ('mov ymm4_0 A21; mov ymm4_1 A42; mov ymm4_2 A13; mov ymm4_3 A34;')
    print ('mov ymm5_0 A41; mov ymm5_1 A32; mov ymm5_2 A23; mov ymm5_3 A14;')
    print ('mov ymm6_0 A11; mov ymm6_1 A22; mov ymm6_2 A33; mov ymm6_3 A34;')



