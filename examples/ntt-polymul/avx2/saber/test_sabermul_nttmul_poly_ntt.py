#!/usr/bin/env python3

# 1. to_zdsl.py --no-main --no-pre --no-post nttmul_poly_ntt.gas > nttmul_poly_ntt_preprocessed.cl
# 2. ./nttmul_poly_ntt.py nttmul_poly_ntt_preprocessed.cl > nttmul_poly_ntt.cl

# q1 = 7681, root1 = 62, 2^(-16)%7681 = 900
# q2 = 10753, root = 10

# Inputs:
# %rdx = 0x55555555f7c0
# L0x555555560700-L0x55555556071e (全都是_16XP = 7681, 16個)
# L0x555555560780-L0x55555556079e (全都是_16XMONT_PINV = -9, 16個)
# L0x5555555607a0-L0x5555555607be (全都是_16XMONT = -3593 = 2^16 mod 7681, 16個)
# L0x555555560800-L0x55555556093e (_ZETAS, 160個)
# L0x555555560940-L0x555555560b3e (_TWIST32, 256個, off=0)
# L0x555555560b40-L0x555555560d3e (_TWIST32, 256個, off=1, note: _TWIST32共有512個)
# L0x555555560d50-L0x555555560dbe (_TWISTS4的第三個開始, 56個)
# L0x7fffffffaee0-L0x7fffffffb0de (input coefficients, 256個)
# L0x7fffffffb4e0-L0x7fffffffb6de (output coefficients, 256個)

import re, math
from argparse import ArgumentParser

ORIGINAL_N = 256
ORIGINAL_P = 8192
P = 7681
PINV = -7679   # p^-1 mod 2^16, -7679 * 7681 = 1 (mod 2^16)
MONT = -3593   # 2^16 mod p, -3593 = 4088 (mod 7681)
MONT_PINV = -9 # (MONT * p^-1) mod 2^16, -9*7681 = -3593 (mod 2^16)
ROOT = 62      # 62**256 = -1 (mod 7681)
# 2^(-16) mod 7681 = 900
_16XP_BASE = 0x555555560700
_16XP_NUM = 16
_16XMONT_PINV_BASE = 0x555555560780
_16XMONT_PINV_NUM = 16
_16XMONT_BASE = 0x5555555607a0
_16XMONT_NUM = 16
_ZETAS_BASE = 0x555555560800
_ZETAS_NUM = 160
_TWIST32_BASE = 0x555555560940
_TWIST32_NUM = 512
_TWISTS4_BASE = 0x555555560d50
_TWISTS4_NUM = 56
INPUT_BASE = 0x7fffffffaee0
INPUT_NUM = 256
ANS_BASE = 0x7fffffffb4e0
ANS_NUM = 256
LEVEL3_ZETA_BASE = [62, 4236, 4600, 5805, 217, 7145, 738, 1115]

ENABLE_CUT_LEVEL0 = True
ENABLE_CUT_LEVEL1 = True
ENABLE_CUT_LEVEL2 = True
ENABLE_CUT_LEVEL3 = True
ENABLE_CUT_LEVEL4 = True
ENABLE_CUT_LEVEL5 = True
ENABLE_CUT_LEVEL6 = False
ENABLE_CUT_LEVEL7 = False

CUT_LEVEL = [ENABLE_CUT_LEVEL0, ENABLE_CUT_LEVEL1, ENABLE_CUT_LEVEL2, ENABLE_CUT_LEVEL3, ENABLE_CUT_LEVEL4, ENABLE_CUT_LEVEL5, ENABLE_CUT_LEVEL6, ENABLE_CUT_LEVEL7]


# The ranges are obtained from test_range256n
FINED_BOUNDS_7681 = [
  #0
  [8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134, 8134],
  #1
  [12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12312, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408, 12408],
  #2
  [16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16812, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16350, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16709, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658, 16658],
  #3
  [8308, 7722, 8770, 9467, 8719, 8999, 8416, 8810, 8787, 8782, 8602, 8690, 8970, 9114, 8472, 9407, 8308, 7722, 8770, 9467, 8719, 8999, 8416, 8810, 8787, 8782, 8602, 8690, 8970, 9114, 8472, 9407, 8842, 8900, 8789, 9149, 8578, 8816, 8580, 8951, 8493, 8690, 9444, 8348, 7833, 8494, 8266, 8242, 8842, 8900, 8789, 9149, 8578, 8816, 8580, 8951, 8493, 8690, 9444, 8348, 7833, 8494, 8266, 8242, 8408, 8968, 8970, 9393, 7935, 8351, 8043, 8538, 8204, 9326, 8902, 8215, 8319, 8570, 8961, 8484, 8408, 8968, 8970, 9393, 7935, 8351, 8043, 8538, 8204, 9326, 8902, 8215, 8319, 8570, 8961, 8484, 8896, 9199, 8561, 8491, 9006, 8937, 8296, 8341, 8968, 8460, 8249, 9498, 8532, 7890, 8666, 8718, 8896, 9199, 8561, 8491, 9006, 8937, 8296, 8341, 8968, 8460, 8249, 9498, 8532, 7890, 8666, 8718, 8842, 9498, 8380, 8470, 8644, 8656, 9381, 9268, 8604, 8223, 8144, 8512, 8173, 8120, 8887, 8684, 8842, 9498, 8380, 8470, 8644, 8656, 9381, 9268, 8604, 8223, 8144, 8512, 8173, 8120, 8887, 8684, 8995, 8760, 9021, 8692, 8563, 8398, 7730, 8828, 8571, 9172, 9128, 7771, 9476, 8233, 9157, 8698, 8995, 8760, 9021, 8692, 8563, 8398, 7730, 8828, 8571, 9172, 9128, 7771, 9476, 8233, 9157, 8698, 8702, 8915, 9040, 8627, 8645, 9319, 8750, 8439, 8880, 8801, 9432, 8963, 8867, 8631, 8560, 7902, 8702, 8915, 9040, 8627, 8645, 9319, 8750, 8439, 8880, 8801, 9432, 8963, 8867, 8631, 8560, 7902, 8633, 8921, 8032, 9225, 8596, 8819, 8558, 8984, 8651, 8331, 9289, 8128, 8136, 7811, 8359, 9019, 8633, 8921, 8032, 9225, 8596, 8819, 8558, 8984, 8651, 8331, 9289, 8128, 8136, 7811, 8359, 9019],
  #4
  [12348, 11762, 12810, 13507, 12759, 13039, 12456, 12850, 12348, 11762, 12810, 13507, 12759, 13039, 12456, 12850, 12629, 12043, 13075, 13788, 13040, 13336, 12721, 13172, 12629, 12043, 13075, 13788, 13040, 13336, 12721, 13172, 12882, 12940, 12829, 13189, 12618, 12856, 12620, 12991, 12882, 12940, 12829, 13189, 12618, 12856, 12620, 12991, 13147, 13221, 13151, 13454, 12851, 13121, 12869, 13240, 13147, 13221, 13151, 13454, 12851, 13121, 12869, 13240, 12448, 13008, 13010, 13433, 11975, 12391, 12083, 12578, 12448, 13008, 13010, 13433, 11975, 12391, 12083, 12578, 12697, 13330, 13291, 13682, 12224, 12656, 12364, 12843, 12697, 13330, 13291, 13682, 12224, 12656, 12364, 12843, 12936, 13239, 12601, 12531, 13046, 12977, 12336, 12381, 12936, 13239, 12601, 12531, 13046, 12977, 12336, 12381, 13217, 13504, 12850, 12869, 13311, 13210, 12601, 12662, 13217, 13504, 12850, 12869, 13311, 13210, 12601, 12662, 12882, 13538, 12420, 12510, 12684, 12696, 13421, 13308, 12882, 13538, 12420, 12510, 12684, 12696, 13421, 13308, 13147, 13787, 12669, 12775, 12933, 12945, 13702, 13589, 13147, 13787, 12669, 12775, 12933, 12945, 13702, 13589, 13035, 12800, 13061, 12732, 12603, 12438, 11770, 12868, 13035, 12800, 13061, 12732, 12603, 12438, 11770, 12868, 13300, 13122, 13383, 12965, 12925, 12687, 12092, 13149, 13300, 13122, 13383, 12965, 12925, 12687, 12092, 13149, 12742, 12955, 13080, 12667, 12685, 13359, 12790, 12479, 12742, 12955, 13080, 12667, 12685, 13359, 12790, 12479, 13023, 13236, 13402, 12948, 12966, 13624, 13055, 12712, 13023, 13236, 13402, 12948, 12966, 13624, 13055, 12712, 12673, 12961, 12072, 13265, 12636, 12859, 12598, 13024, 12673, 12961, 12072, 13265, 12636, 12859, 12598, 13024, 12938, 13226, 12394, 13514, 12885, 13092, 12863, 13305, 12938, 13226, 12394, 13514, 12885, 13092, 12863, 13305],
  #5
  [16787, 16201, 17249, 17946, 16787, 16201, 17249, 17946, 16904, 16334, 17350, 18063, 16904, 16334, 17350, 18063, 17036, 16525, 17482, 18195, 17036, 16525, 17482, 18195, 17165, 16604, 17586, 18324, 17165, 16604, 17586, 18324, 17321, 17379, 17268, 17628, 17321, 17379, 17268, 17628, 17438, 17496, 17385, 17761, 17438, 17496, 17385, 17761, 17554, 17628, 17558, 17861, 17554, 17628, 17558, 17861, 17683, 17757, 17687, 18015, 17683, 17757, 17687, 18015, 16887, 17447, 17449, 17872, 16887, 17447, 17449, 17872, 16947, 17548, 17509, 17989, 16947, 17548, 17509, 17989, 17104, 17737, 17698, 18089, 17104, 17737, 17698, 18089, 17183, 17841, 17777, 18218, 17183, 17841, 17777, 18218, 17375, 17678, 17040, 16970, 17375, 17678, 17040, 16970, 17508, 17811, 17141, 17071, 17508, 17811, 17141, 17071, 17699, 17911, 17257, 17276, 17699, 17911, 17257, 17276, 17778, 18065, 17361, 17380, 17778, 18065, 17361, 17380, 17321, 17977, 16859, 16949, 17321, 17977, 16859, 16949, 17438, 18094, 17008, 17098, 17438, 18094, 17008, 17098, 17554, 18194, 17151, 17257, 17554, 18194, 17151, 17257, 17683, 18323, 17255, 17361, 17683, 18323, 17255, 17361, 17474, 17239, 17500, 17171, 17474, 17239, 17500, 17171, 17591, 17340, 17560, 17288, 17591, 17340, 17560, 17288, 17707, 17529, 17790, 17372, 17707, 17529, 17790, 17372, 17836, 17633, 17869, 17501, 17836, 17633, 17869, 17501, 17181, 17394, 17519, 17106, 17181, 17394, 17519, 17106, 17298, 17543, 17636, 17207, 17298, 17543, 17636, 17207, 17430, 17718, 17809, 17355, 17430, 17718, 17809, 17355, 17559, 17822, 17938, 17459, 17559, 17822, 17938, 17459, 17112, 17400, 16511, 17704, 17112, 17400, 16511, 17704, 17229, 17517, 16628, 17837, 17229, 17517, 16628, 17837, 17345, 17633, 16801, 17996, 17345, 17633, 16801, 17996, 17474, 17762, 16930, 18075, 17474, 17762, 16930, 18075],
  #6
  [8878, 8878, 8878, 8878, 9262, 9355, 9262, 9355, 9075, 9216, 9075, 9216, 9212, 8502, 9212, 8502, 9238, 8338, 9238, 8338, 8563, 8762, 8563, 8762, 8924, 8844, 8924, 8844, 8859, 8724, 8859, 8724, 8878, 8878, 8878, 8878, 9262, 9434, 9262, 9434, 9075, 9284, 9075, 9284, 9212, 8544, 9212, 8544, 9238, 8315, 9238, 8315, 8563, 8781, 8563, 8781, 8924, 8884, 8924, 8884, 8859, 8729, 8859, 8729, 8878, 8878, 8878, 8878, 9262, 9434, 9262, 9434, 9075, 9284, 9075, 9284, 9212, 8548, 9212, 8548, 9265, 8338, 9265, 8338, 8563, 8781, 8563, 8781, 8924, 8887, 8924, 8887, 8859, 8729, 8859, 8729, 8878, 8878, 8878, 8878, 9221, 9403, 9221, 9403, 9075, 9276, 9075, 9276, 9206, 8544, 9206, 8544, 9224, 8292, 9224, 8292, 8563, 8796, 8563, 8796, 8915, 8891, 8915, 8891, 8859, 8700, 8859, 8700, 8878, 8878, 8878, 8878, 9221, 9478, 9221, 9478, 9075, 9303, 9075, 9303, 9206, 8545, 9206, 8545, 9224, 8296, 9224, 8296, 8563, 8796, 8563, 8796, 8897, 8891, 8897, 8891, 8844, 8711, 8844, 8711, 8878, 8878, 8878, 8878, 9278, 9403, 9278, 9403, 9075, 9257, 9075, 9257, 9212, 8529, 9212, 8529, 9265, 8315, 9265, 8315, 8563, 8767, 8563, 8767, 8924, 8868, 8924, 8868, 8859, 8689, 8859, 8689, 8878, 8878, 8878, 8878, 9278, 9403, 9278, 9403, 9075, 9249, 9075, 9249, 9237, 8544, 9237, 8544, 9265, 8315, 9265, 8315, 8563, 8767, 8563, 8767, 8924, 8868, 8924, 8868, 8860, 8689, 8860, 8689, 8878, 8878, 8878, 8878, 9205, 9434, 9205, 9434, 9075, 9284, 9075, 9284, 9181, 8548, 9181, 8548, 9197, 8338, 9197, 8338, 8550, 8781, 8550, 8781, 8889, 8884, 8889, 8884, 8829, 8729, 8829, 8729],
  #7
  [17756, 17756, 13199, 13199, 18617, 18617, 13624, 13624, 18291, 18291, 13437, 13437, 17714, 17714, 13517, 13517, 17576, 17576, 13543, 13543, 17325, 17325, 12884, 12884, 17768, 17768, 13245, 13245, 17583, 17583, 13180, 13180, 17756, 17756, 13199, 13199, 18696, 18696, 13624, 13624, 18359, 18359, 13437, 13437, 17756, 17756, 13517, 13517, 17553, 17553, 13527, 13527, 17344, 17344, 12884, 12884, 17808, 17808, 13245, 13245, 17588, 17588, 13180, 13180, 17756, 17756, 13199, 13199, 18696, 18696, 13624, 13624, 18359, 18359, 13437, 13437, 17760, 17760, 13517, 13517, 17603, 17603, 13570, 13570, 17344, 17344, 12884, 12884, 17811, 17811, 13245, 13245, 17588, 17588, 13180, 13180, 17756, 17756, 13199, 13199, 18624, 18624, 13583, 13583, 18351, 18351, 13437, 13437, 17750, 17750, 13511, 13511, 17516, 17516, 13513, 13513, 17359, 17359, 12884, 12884, 17806, 17806, 13236, 13236, 17559, 17559, 13180, 13180, 17756, 17756, 13199, 13199, 18699, 18699, 13583, 13583, 18378, 18378, 13437, 13437, 17751, 17751, 13511, 13511, 17520, 17520, 13513, 13513, 17359, 17359, 12884, 12884, 17788, 17788, 13218, 13218, 17555, 17555, 13165, 13165, 17756, 17756, 13199, 13199, 18681, 18681, 13640, 13640, 18332, 18332, 13437, 13437, 17741, 17741, 13517, 13517, 17580, 17580, 13554, 13554, 17330, 17330, 12884, 12884, 17792, 17792, 13245, 13245, 17548, 17548, 13180, 13180, 17756, 17756, 13199, 13199, 18681, 18681, 13640, 13640, 18324, 18324, 13437, 13437, 17781, 17781, 13542, 13542, 17580, 17580, 13554, 13554, 17330, 17330, 12884, 12884, 17792, 17792, 13245, 13245, 17549, 17549, 13181, 13181, 17756, 17756, 13199, 13199, 18639, 18639, 13567, 13567, 18359, 18359, 13437, 13437, 17729, 17729, 13486, 13486, 17535, 17535, 13502, 13502, 17331, 17331, 12871, 12871, 17773, 17773, 13210, 13210, 17558, 17558, 13150, 13150]
]

def join_chunks(xs, glue, n, indent=0):
    return [" " * indent + glue.join(xs[i:i + n]) for i in range(0, len(xs), n)]

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

def str_main_args ():
    return "\n".join([
        "(* parameters *)\n",
        ",\n".join(join_chunks(["sint16 f{:03d}".format(i) for i in range(INPUT_NUM)], ", ", 4))])

def str_precondition_algebra ():
    return "\n".join([
        "(* algebraic precondition *)\n",
        "true"])

def str_precondition_range ():
    return "\n".join([
        "(* range precondition *)\n",
        "and [",
        format(",\n".join(join_chunks(["(-{0})@16 <s f{1:03d}, f{1:03d} <s {0}@16".format(4096, i) for i in range(INPUT_NUM)], ", ", 4))),
        "]"])

def str_twiddles ():
    _16XP = [ P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P ]
    _16XMONT_PINV = [
  MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV,
  MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV
        ]
    _16XMONT = [
  MONT, MONT, MONT, MONT, MONT, MONT, MONT, MONT,
  MONT, MONT, MONT, MONT, MONT, MONT, MONT, MONT
        ]
    _ZETAS = [
   28865,  28865,  28865,  28865,  28865,  28865,  28865,  28865,
   28865,  28865,  28865,  28865,  28865,  28865,  28865,  28865,
    3777,   3777,   3777,   3777,   3777,   3777,   3777,   3777,
    3777,   3777,   3777,   3777,   3777,   3777,   3777,   3777,
  -10350, -10350, -10350, -10350, -10350, -10350, -10350, -10350,
  -10350, -10350, -10350, -10350, -10350, -10350, -10350, -10350,
   -3182,  -3182,  -3182,  -3182,  -3182,  -3182,  -3182,  -3182,
   -3182,  -3182,  -3182,  -3182,  -3182,  -3182,  -3182,  -3182,
    4496,   4496,   4496,   4496,   4496,   4496,   4496,   4496,
   -7244,  -7244,  -7244,  -7244,  -7244,  -7244,  -7244,  -7244,
   -3696,  -3696,  -3696,  -3696,  -3696,  -3696,  -3696,  -3696,
   -1100,  -1100,  -1100,  -1100,  -1100,  -1100,  -1100,  -1100,
   16425,  16425,  16425,  16425,  16425,  16425,  16425,  16425,
   16425,  16425,  16425,  16425,  16425,  16425,  16425,  16425,
    3625,   3625,   3625,   3625,   3625,   3625,   3625,   3625,
    3625,   3625,   3625,   3625,   3625,   3625,   3625,   3625,
   14744,  14744,  14744,  14744,  14744,  14744,  14744,  14744,
   -4974,  -4974,  -4974,  -4974,  -4974,  -4974,  -4974,  -4974,
    2456,   2456,   2456,   2456,   2456,   2456,   2456,   2456,
    2194,   2194,   2194,   2194,   2194,   2194,   2194,   2194
        ]
    _TWIST32 = [
      -9,   -529,  32738,  -1851,     -9,  29394,  -7508, -20435,
      -9,  26288,   9855, -19215,     -9,  16006, -12611,   -964,
   -3593,    -17,  -1054,   3781,  -3593,   3794,   2732,  -2515,
   -3593,   1712,   2175,  -3343,  -3593,  -3450,  -2883,   1084,
   16279,  26288,  -8558,  -6297,  11783, -25648,  14351, -25733,
   21066, -23882, -17440,  -7304, -26279,  16791,  22124, -20435,
   -3689,   1712,  -1390,  -1689,      7,  -1072,  -1521,   1403,
    -438,  -2378,  -1056,  -3208,   1881,  -3177,   -404,  -2515,
    2816, -22039,   9855,  21168, -19394,  30255, -27132,  17013,
   23489, -18506,   1869,  10145,  -3114,   9650, -15358, -24232,
    2816,  -2071,   2175,  -3408,  -1986,  -2001,   3588,  -1931,
   -1599,   2998,   3405,   1441,   2006,    434,      2,  -3752,
    1724, -24214,   6032, -19215, -21467,  29453, -16655,  32124,
    4505,  13686, -25946, -12790, -23668, -31518,  14351,  12449,
    3772,   3434,  -2160,  -3343,    549,  -1779,   -783,   1404,
    -103,   2422,   3750,  -1526,   2956,    226,  -1521,   3745,
  -11655,  -1715,  24743,  26766,  23754,  22943,  -2722,   4880,
   18242,  26621, -32329, -10333, -22593, -16715,  30426,   2858,
     121,   -179,  -3417,   3214,   2250,  -1121,  -1698,  -3312,
     834,   3581,  -3145,  -3677,   2495,  -2891,    730,  -2262,
   21066,  -4624, -24573, -16186,  29667, -30597,  23225,  10333,
  -15998,   6510,  -3558,  17491,  11792,  30255,  -4693,  21723,
    -438,   3568,  -1533,  -2874,   3555,  -3461,   2233,   3677,
    -638,   -658,   -486,   -429,   3600,  -2001,  -2133,   -293,
  -20469, -23882,  26663,  14718,  -9488, -16885, -26220,  17636,
  -19351, -17082,   2722,   2807,  10972,  -5990,  29871,  -5299,
   -1525,  -2378,  -1497,   -642,  -1296,   2059,  -3692,   -796,
     617,  -3770,   1698,   -777,  -3364,  -2918,  -2385,  -3763,
   -4983,  18745, -17440, -32695,  -4505, -12261, -32252,  23933,
    2073, -30938,  30136,  16083, -21467, -32414,  -8908,   -947,
   -1399,  -2247,  -1056,   3657,    103,  -1509,  -1532,    893,
   -2535,  -1242,   1464,  -1837,    549,   -670,  -2764,    589,
      -9,  -1851,  -8558, -22039,     -9,   4573, -26441,  16791,
      -9,  -6297,   6032,  -4624,     -9,  -9513,   9360,  16006,
   -3593,   3781,  -1390,  -2071,  -3593,  -2083,   2743,  -3177,
   -3593,  -1689,  -2160,   3568,  -3593,   3287,   1168,  -3450,
    1724, -19215,  24743,  -4624, -21766,   1007, -15358, -25648,
   -4983,  -7304, -16092, -13711,  21399,   4573, -12611,  29394,
    3772,  -3343,  -3417,   3568,  -2310,   1519,      2,  -1072,
   -1399,  -3208,  -1756,   2161,   1431,  -2083,  -2883,   3794,
  -20469,  14718, -17440,  16638, -15307,  12449,  12269, -22764,
  -26382,  -5452, -25946, -11996,   5759,   -964, -26441,   9087,
   -1525,   -642,  -1056,   1278,  -1483,   3745,  -2579,   -236,
   -2830,    692,   3750,   2340,  -1921,   1084,   2743,   1407,
    5930, -23933, -16092, -18506,  11792, -28805, -27132,  -5990,
   -5913,  27243, -13933,   6510, -26279,  -6766,  -7508,  16791,
     810,   -893,  -1756,   2998,   3600,  -1669,   3588,  -2918,
   -1305,  -2965,    915,   -658,   1881,    402,   2732,  -3177,
  -18191, -15221, -26262,   2739,   -828, -15145,  -8908,  -9633,
   20315, -15111, -10478,    802, -20870,  -4565,  22124,  26783,
   -2319,   3723,   1386,   1203,  -2876,  -2345,  -2764,   -929,
   -1701,  -3335,  -3310,   -222,  -1414,  -2005,   -404,   2719,
    4505,  -5452,  -3456, -28958, -14121,  32124,  17602,   2526,
    2073,  22790, -24052,   9633, -21766, -20435,  21868,   3524,
    -103,    692,  -3456,   2786,  -1321,   1404,    194,   3550,
   -2535,   3334,   2572,    929,  -2310,  -2515,   -660,   1476,
    7491, -12790, -22875,  16885,  22568,  27858,  10478,  20119,
   31177,   5299, -21860, -10495,  -3114,   1007,   8472,   9650,
   -2237,  -1526,   -859,  -2059,   2088,   2258,   3310,    151,
    1993,   3763,  -3428,  -2815,   2006,   1519,  -3816,    434,
   -5913,  27636, -32329,  -2952,  29667,  23984, -10409,   8831,
  -11792,  14138,  13541,  31518,  11783,  30844, -15358, -19274,
   -1305,   1012,  -3145,   1144,   3555,   -592,   2391,   1151,
   -3600,    826,   2789,   -226,      7,    124,      2,   2230
        ]
    _TWISTS4 = [
      -9, -16425, -28865,  10350,  -3593,  -3625,  -3777,   3182,
      -9, -10350,  28865,  16425,  -3593,  -3182,   3777,   3625,
      -9,   4496, -10350,  14744,  -3593,  -3696,  -3182,   2456,
      -9,   4974, -16425,   7244,  -3593,  -2194,  -3625,   1100,
      -9, -11655,   4496, -18191,  -3593,    121,  -3696,  -2319,
      -9, -22593,   7244, -20315,  -3593,   2495,   1100,   1701,
      -9, -18191,  14744, -23754,  -3593,  -2319,   2456,  -2250,
      -9, -20870,   4974, -22593,  -3593,  -1414,  -2194,   2495
        ]
    twiddles = [
        ("_16XP", _16XP, _16XP_BASE),
        ("_16XMONT", _16XMONT, _16XMONT_BASE),
        ("_16XMONT_PINV", _16XMONT_PINV, _16XMONT_PINV_BASE),
        ("_16XMONT", _16XMONT, _16XMONT_BASE),
        ("_ZETAS", _ZETAS, _ZETAS_BASE),
        ("_TWIST32", _TWIST32, _TWIST32_BASE),
        ("_TWISTS4", _TWISTS4, _TWISTS4_BASE)
        ]
    res = []
    for (name, arr, base) in twiddles:
        res.append("\n(* {} *)\n".format(name))
        res.append("\n".join(join_chunks(["mov L0x{:x} ({:4d})@sint16;".format(base + 2*i, arr[i]) for i in range (len(arr))], " ", 4)))
    return "\n".join(res)

def ntt_mod(num_ans, prime, mont, root, negacyclic, stage):
    num_rings = 2**stage
    num_coeffs = num_ans // num_rings
    n_expn = int(math.log(num_ans, 2))
    num_bits = n_expn + 1 if negacyclic else n_expn
    res = []
    for i in range (num_rings):
        if negacyclic:
            l = num_to_bits(i, stage)
            l.reverse()
            l.insert(0, 1)
            l = [0 for i in range(num_bits - stage - 1)] + l
        else:
            l = num_to_bits(i, num_bits)
            l.reverse()
        e = bits_to_num(l)
        modulo = (root**e) % prime
        modulo_mont = (modulo * mont) % prime
        modulo = modulo - prime if modulo > prime / 2 else modulo
        modulo_mont = modulo_mont - prime if modulo_mont > prime / 2 else modulo_mont
        res.append(dict(modulo = modulo, mont = modulo_mont))
    return res

def str_inits ():
    return "\n".join([
        "(* inits *)\n",
        "\n".join(join_chunks(["mov L0x{:x} f{:03d};".format(INPUT_BASE + 2 * i, i) for i in range(INPUT_NUM)], " ", 4))])

def str_init_poly_var(poly_var):
    return ("ghost {}@sint16 : true && true;").format(poly_var)

def str_init_poly (poly, poly_var, prefix, num):
    return "\n".join([
        "(* {} *)\n".format(poly),
        "ghost {}@bit :".format(poly),
        "{0} * {0} =".format(poly),
        "{} && true;".format(" +\n".join(join_chunks(["{0}{1:03d}*({2}**{1})".format (prefix, i, poly_var) for i in range(num)], " + ", 4)))])

def str_level0_algebraic_condition_ith (poly, poly_var, base, addr_off, stage, num_ans, num_bits, negacyclic, q, root, ith):
    res = []
    num_rings = 2**stage
    num_coeffs = num_ans // num_rings
    i = ith
    if negacyclic:
        l = num_to_bits(i, stage)
        l.reverse()
        l.insert(0, 1)
        l = [0 for i in range(num_bits - stage - 1)] + l
    else:
        l = num_to_bits(i, num_bits)
        l.reverse()
    e = bits_to_num(l)
    modulo = (root**e) % q
    res.append("eqmod")
    ring_base = num_coeffs * i
    res.append("({0} * {0})\n(".format(poly))
    res.append(" +\n".join(join_chunks(["L0x{0:x}*({2}**{1})".format(base + addr_off*j, j - ring_base, poly_var) for j in range (ring_base, ring_base + num_coeffs)], " + ", 2)))
    res.append(")")
    res.append("[{0}, {3}**{1} - {2}]".format (q, num_coeffs, modulo, poly_var))
    return "\n".join(res)

def str_level0_algebraic_condition (poly, poly_var, base, addr_off, stage, num_ans, num_bits, negacyclic, q, root):
    res = []
    num_rings = 2**stage
    num_coeffs = num_ans // num_rings
    for i in range (num_rings):
        res.append("{0}{1}".format (str_level0_algebraic_condition_ith (poly, poly_var, base, addr_off, stage, num_ans, num_bits, negacyclic, q, root, i), ',' if i < num_rings - 1 else ''))
    return "\n".join(res)

def str_levels1t7_algebraic_condition_ith (poly, poly_var, ymms, ymms_off, ymms_count, stage, num_ans, num_bits, negacyclic, q, root, ith):
    res = []
    num_rings = 2**stage
    num_coeffs = num_ans // num_rings
    i = ith
    if negacyclic:
        l = num_to_bits(i, stage)
        l.reverse()
        l.insert(0, 1)
        l = [0 for i in range(num_bits - stage - 1)] + l
    else:
        l = num_to_bits(i, num_bits)
        l.reverse()
    e = bits_to_num(l)
    modulo = (root**e) % q
    res.append("eqmod")
    ring_base = num_coeffs * i
    res.append("({0} * {0})\n(".format(poly))
    res.append(" +\n".join(join_chunks(["ymm{0}_{1:1x}*({3}**{2})".format(ymms[(j - ring_base) // ymms_count], (j - ring_base) % ymms_count + ymms_off, j - ring_base, poly_var) for j in range (ring_base, ring_base + num_coeffs)], " + ", 4)))
    res.append(")")
    res.append("[{0}, {3}**{1} - {2}]".format (q, num_coeffs, modulo, poly_var))
    return "\n".join(res)

def str_level0_range_condition (base, addr_off, m, num_ans, q):
    return ",\n".join(join_chunks(["(-(4096 + {0} * {2}))@16 <s L0x{1:x}, L0x{1:x} <s (4096 + {0} * {2})@16".format(q, base + addr_off * i, m) for i in range(num_ans)], ", ", 2))

def str_levels1t7_range_condition (ymms, m, q):
    def range_ymm(ymm):
        return ",\n".join(join_chunks(["(-(4096 + {0} * {1}))@16 <s ymm{2}_{3:1x}, ymm{2}_{3:1x} <s (4096 + {0} * {1})@16".format(q, m, ymm, i) for i in range(16)], ", ", 2))
    return ",\n".join([range_ymm(ymm) for ymm in ymms])

def str_level0_fined_range_condition (base, addr_off, ranges, num_ans):
    return ",\n".join(join_chunks(["(-({0}))@16 <s L0x{1:x}, L0x{1:x} <s ({0})@16".format(ranges[i], base + addr_off * i) for i in range(num_ans)], ", ", 2))

def str_levels1t7_fined_range_condition (ymms, ranges, ymms_off, ymms_count, left_rel, right_rel):
    def range_ymm(rs, ymm):
        return ",\n".join(join_chunks(["(-({0}))@16 {3} ymm{1}_{2:1x}, ymm{1}_{2:1x} {4} ({0})@16".format(rs[i], ymm, i + ymms_off, left_rel, right_rel) for i in range(ymms_count)], ", ", 2))
    return ",\n".join([range_ymm(rs, ymm) for rs, ymm in zip(ranges, ymms)])

def make_ymms(ymms, off, num):
    return ["ymm{}_{:x}".format(ymm, off + i) for ymm in ymms for i in range(num)]

def make_eqmod(poly_name, ymms, coefs, mods):
    return "\n".join([
        "eqmod",
        "  ({0} * {0})".format(poly_name),
        "  (",
        " +\n".join(join_chunks(["{0}*({1}**{2})".format(ymms[i], coefs[i], i) for i in range(len(ymms))], " + ", 4, indent=4)),
        "  )",
        "  [{}]".format(", ".join(mods))
    ])

def str_level3_twist(ecut_id, rcut_id, poly_name, args):
    res = "\n".join([
        "ghost {} :".format(", ".join(["{}@sint16, {}@sint16".format(zeta_name, y_name) for (zeta, zeta_name, y_name, ymms) in args])),
        "and [",
        "  {}".format(",\n  ".join(["{} = {}".format(zeta_name, zeta) for (zeta, zeta_name, y_name, ymms) in args])),
        "] && true;",
        "",
        "\n(* ecut {0} *)\n".format(ecut_id),
        "ecut and [",
        ",\n".join([make_eqmod(poly_name, ymms, ["({0} * {1})".format(zeta_name, y_name) for i in range(32)], [str(P), "x0 - {0} * {1}".format(zeta_name, y_name), "{0}**32 - 1".format(y_name)]) for (zeta, zeta_name, y_name, ymms) in args]),
        "];"
    ])
    return (ecut_id + 1, rcut_id, res)

def str_level3to7_algebra(poly_name, args, expn):
    return ",\n".join([
        make_eqmod(poly_name, ymms, [y_name] * len(ymms), [str(P), "x0 - {0} * {1}".format(zeta_name, y_name), "{0}**{2} - ({1})".format(y_name, m, expn)]) for (zeta_name, y_name, ymms, m) in args
    ])

def get_ntt_mod_level3to7(i):
    if i < 2:
        return 1 if i % 2 == 0 else -1
    else:
        s = 0
        j = 0
        n = int(math.log(ORIGINAL_N, 2))
        for k in range(2, n + 1):
            if i < math.pow(2, k):
                s = k - 1
                break
        j = i % pow(2, s)
        return ntt_mod(num_ans=ANS_NUM, prime=P, mont=MONT, root=ROOT, negacyclic=True, stage=s)[j]["modulo"]
    return 0

def str_assertions(pairs):
    equalities = []
    for (ymm1, ymm2) in pairs:
        for i in range(0, 16):
            equalities.append("mulLymm{0}_{2:x} = mulLymm{1}_{2:x}".format(ymm1, ymm2, i))
    return "assert true && and [\n{0}\n];\nassume and [\n{0}\n] && true;".format(",\n".join(join_chunks(equalities, ", ", 2)))

level = 0
off = 0
ecut_id = 0
rcut_id = 0

def print_comment(str):
    print("(* {} *)".format(str))

def str_levels1t7_fined_range_condition_tmp(ymms, r):
    return ",\n".join(join_chunks(["(-({0}))@16 <=s ymm{1}_{2:1x}, ymm{1}_{2:1x} <=s ({0})@16".format(r, ymm, i) for i in range(16) for ymm in ymms], ", ", 2))

def print_instr(instr):
    global level, off, ecut_id, rcut_id

    # ==================== Initial ====================
    if instr.startswith("(* vmovdqa (%rdx),%ymm0"):
        print_comment("Loading _16XP")
    elif instr.startswith("(* vmovdqa 0x100(%rdx),%ymm1"):
        print_comment("Loading _ZETAS 0~15")
    elif instr.startswith("(* vmovdqa 0x120(%rdx),%ymm2"):
        print_comment("Loading _ZETAS 16~31")

    # ==================== Level 0 ====================
    elif instr.startswith("(* vmovdqa 0x100(%rsi),%ymm8") and level == 0:
        print_comment("level 0, off 0, loading inputs f128-f191")
    elif instr.startswith("(* vpmullw %ymm1,%ymm8,%ymm12") and level == 0:
        print_comment("level 0, mul		8,9,10,11,1,1,2,2, f(64*\off+128)-f(64*\off+191) * _ZETAS[0]")
    elif instr.startswith("(* vpmulhw %ymm2,%ymm8,%ymm8") and level == 0:
        print_comment("level 0, mul		8,9,10,11,1,1,2,2, f(64*\off+128)-f(64*\off+191) * _ZETAS[16]")
    elif instr.startswith("(* vmovdqa (%rsi),%ymm4") and level == 0:
        print_comment("level 0, off 0, loading inputs f000-f063")
    elif instr.startswith("(* vpmulhw %ymm0,%ymm12,%ymm12") and level == 0:
        print_comment("level 0, reduce		8,9,10,11")
    elif instr.startswith("(* vpaddw %ymm8,%ymm4,%ymm3") and level == 0:
        # Verified
        print(str_assertions([(8, 12), (9, 13), (10, 14), (11, 15)]))
        print_comment("level 0, update		3,4,5,6,7,8,9,10,11")
    elif instr.startswith("(* vmovdqa %ymm3,(%rdi)") and level == 0:
        print_comment("level 0, off 0, store results")
    elif instr.startswith("(* vmovdqa 0x180(%rsi),%ymm8") and level == 0:
        print_comment("level 0, off 1, loading inputs f192-f255")
    elif instr.startswith("(* vmovdqa 0x80(%rsi),%ymm4") and level == 0:
        print_comment("level 0, off 1, loading inputs f064-f127")
    elif instr.startswith("(* vmovdqa %ymm3,0x80(%rdi)") and level == 0:
        print_comment("level 0, off 1, store results")

    # ==================== Level 1 ====================
    elif instr.startswith("(* vmovdqa 0x140(%rdx),%ymm15") and level == 0:
        # # End of level 0 (Verified: algebra, range)
        print_comment("===== End of level 0 =====")
        if CUT_LEVEL[level]:
            print("\n(* ecut {0}, rcut {1} *)\n".format(ecut_id, rcut_id))
            print("cut")
            print("and [")
            print(str_level0_algebraic_condition(poly='inp_poly', poly_var='x0', base=ANS_BASE, addr_off=2, stage=1, num_ans=ANS_NUM, num_bits=9, negacyclic=True, q=P, root=ROOT))
            print("] && and [")
            # print(str_level0_range_condition (base=ANS_BASE, addr_off=2, m=1, num_ans=ANS_NUM, q=P))   # Verified
            print(str_level0_fined_range_condition(base=ANS_BASE, addr_off=2, ranges=FINED_BOUNDS_7681[0], num_ans=ANS_NUM))   # Verified
            print("];\n")
            ecut_id = ecut_id + 1
            rcut_id = rcut_id + 1
        print_comment("Start of level 1, off {}".format(off))
        level = level + 1
    elif instr.startswith("(* vpaddw %ymm8,%ymm4,%ymm3") and level == 1:
        # Verified
        print(str_assertions([(8, 12), (9, 13), (10, 14), (11, 15)]))
        print_comment("level 1, off {}, update          3,4,5,6,7,8,9,10,11".format(off))

    # ==================== Level 2 ====================
    elif instr.startswith("(* vperm2i128 $0x20,%ymm10,%ymm5,%ymm7") and level == 1:
        # End of level 1 (Verified: algebra, range)
        print_comment("===== End of level 1, off {} =====".format(off))
        if CUT_LEVEL[level]:
            print("\n(* ecut {0}, rcut {1} *)\n".format(ecut_id, rcut_id))
            print("cut")
            print("and [")
            print(str_levels1t7_algebraic_condition_ith (poly='inp_poly', poly_var='x0', ymms=[3, 4, 5, 6], ymms_off=0, ymms_count=16, stage=2, num_ans=ANS_NUM, num_bits=9, negacyclic=True, q=P, root=ROOT, ith=(0 if off == 0 else 2)), end='')
            print(",")
            print(str_levels1t7_algebraic_condition_ith (poly='inp_poly', poly_var='x0', ymms=[8, 9, 10, 11], ymms_off=0, ymms_count=16, stage=2, num_ans=ANS_NUM, num_bits=9, negacyclic=True, q=P, root=ROOT, ith=(1 if off == 0 else 3)))
            print ("] && and [")
            # print(str_levels1t7_range_condition (ymms=[3, 4, 5, 6, 8, 9, 10, 11], m=2, q=P))   # Verified
            print(str_levels1t7_fined_range_condition (ymms=[3, 4, 5, 6, 8, 9, 10, 11], ranges=[FINED_BOUNDS_7681[1][(128*off + i*16):(128*off + i*16 + 16)] for i in range(8)], ymms_off=0, ymms_count=16, left_rel="<s", right_rel="<s"))   # Verified
            print("];\n")
            ecut_id = ecut_id + 1
            rcut_id = rcut_id + 1
        print_comment("===== Start of level 2, off {} =====".format(off))
        level = level + 1
    elif instr.startswith("(* vpaddw %ymm7,%ymm6,%ymm4") and level == 2:
        # Verified
        print(str_assertions([(7, 12), (10, 13), (5, 14), (11, 15)]))
        print_comment("level 2, off {}, update          4,6,8,3,9,7,10,5,11".format(off))

    # ==================== Level 3 ====================
    elif instr.startswith("(* vpunpcklqdq %ymm7,%ymm4,%ymm9") and level == 2:
        # End of level 2 (Verified: algebra, range)
        print_comment("===== End of level 2, off {} =====".format(off))
        if CUT_LEVEL[level]:
            print("\n(* ecut {0}, rcut {1} *)\n".format(ecut_id, rcut_id))
            print ("cut")
            print ("and [")
            for i in range(2):
                print(str_levels1t7_algebraic_condition_ith (poly='inp_poly', poly_var='x0', ymms=[4, 6, 8, 3], ymms_off=(8*i), ymms_count=8,
                                                             stage=3, num_ans=ANS_NUM, num_bits=9, negacyclic=True, q=P, root=ROOT, ith=(i*2 + off*4)), end='')
                print(",")
                print(str_levels1t7_algebraic_condition_ith (poly='inp_poly', poly_var='x0', ymms=[7, 10, 5, 11], ymms_off=(8*i), ymms_count=8,
                                                             stage=3, num_ans=ANS_NUM, num_bits=9, negacyclic=True, q=P, root=ROOT, ith=(i*2 + off*4 + 1)), end='')
                print("," if i < 1 else "")
            print ("] && and [")
            # print(str_levels1t7_range_condition (ymms=[4, 6, 8, 3, 7, 10, 5, 11], m=3, q=P))   # Verified
            # First low 8 16-bit of ymms and then high 8 16-bit of ymms
            for i in range(2):
                print(str_levels1t7_fined_range_condition (ymms=[4, 6, 8, 3, 7, 10, 5, 11],
                                                           ranges=[FINED_BOUNDS_7681[2][(64*i + 128*off + j*8):(64*i + 128*off + j*8 + 8)] for j in range(8)],
                                                           ymms_off=(8*i), ymms_count=8, left_rel="<s", right_rel="<s"), end='')   # Verified
                print("," if i < 1 else "")
            print("];\n")
            ecut_id = ecut_id + 1
            rcut_id = rcut_id + 1
            (ecut_id, rcut_id, cut_str) = str_level3_twist(ecut_id, rcut_id, "inp_poly",
                                                           [
                                                               [LEVEL3_ZETA_BASE[i+off*4], "zeta_0_{}".format(i+off*4), "y_0_{}".format(i+off*4),
                                                                make_ymms([[4, 6, 8, 3], [7, 10, 5, 11]][i%2], (i//2)*8, 8)] for i in range(4)
                                                           ])
            print(cut_str)
            print()
        print_comment("===== Start of level 3, off {} =====".format(off))
        level = level + 1
    elif (instr.startswith("(* vpmullw 0x340(%rdx),%ymm6,%ymm12") or instr.startswith("(* vpmullw 0x540(%rdx),%ymm6,%ymm12")) and level == 3:
        # Verified
        print(str_assertions([(9, 12), (7, 13), (4, 14), (10, 15)]))
        print_comment("level 3, off {}, end of reduce          9,7,4,10,0".format(off))
    elif instr.startswith("(* vpaddw %ymm6,%ymm9,%ymm3") and level == 3:
        # Verified
        print(str_assertions([(6, 12), (5, 13), (8, 14), (11, 15)]))
        print_comment("level 3, off {}, end of reduce          6,5,8,11,0".format(off))

    # ==================== Level 4 ====================
    elif instr.startswith("(* vmovdqa 0x80(%rdx),%ymm14") and level == 3:
        # End of level 3 (Verified: algebra for off=0, range)
        print_comment("===== End of level 3, off {} =====".format(off))
        # All failed
        if CUT_LEVEL[level]:
            print("\n(* ecut {0}, rcut {1} *)\n".format(ecut_id, rcut_id))
            print("cut")
            print("and [")
            print(str_level3to7_algebra(poly_name="inp_poly", args=[
                ("zeta_0_{}".format(0+4*off), "y_0_{}".format(0+4*off), make_ymms([3, 9, 7, 4], 0, 4), 1),
                ("zeta_0_{}".format(0+4*off), "y_0_{}".format(0+4*off), make_ymms([6, 5, 8, 11], 0, 4), -1),
                ("zeta_0_{}".format(1+4*off), "y_0_{}".format(1+4*off), make_ymms([3, 9, 7, 4], 4, 4), 1),
                ("zeta_0_{}".format(1+4*off), "y_0_{}".format(1+4*off), make_ymms([6, 5, 8, 11], 4, 4), -1),
                ("zeta_0_{}".format(2+4*off), "y_0_{}".format(2+4*off), make_ymms([3, 9, 7, 4], 8, 4), 1),
                ("zeta_0_{}".format(2+4*off), "y_0_{}".format(2+4*off), make_ymms([6, 5, 8, 11], 8, 4), -1),
                ("zeta_0_{}".format(3+4*off), "y_0_{}".format(3+4*off), make_ymms([3, 9, 7, 4], 12, 4), 1),
                ("zeta_0_{}".format(3+4*off), "y_0_{}".format(3+4*off), make_ymms([6, 5, 8, 11], 12, 4), -1)
            ], expn=16))
            print("] prove with [all ghosts] && and [")
            num_ymms_per_poly = 4
            num_coefs_per_ymm = 4
            num_polys = 16 // num_coefs_per_ymm
            for i in range(num_polys):
                print(str_levels1t7_fined_range_condition (ymms=[3, 9, 7, 4, 6, 5, 8, 11], ranges=[FINED_BOUNDS_7681[level][((128//num_polys)*i + 128*off + j*num_coefs_per_ymm):((128//num_polys)*i + 128*off + (j+1)*num_coefs_per_ymm)] for j in range(8)], ymms_off=(num_coefs_per_ymm*i), ymms_count=num_coefs_per_ymm, left_rel="<=s", right_rel="<=s"), end='') # Verified
                print("," if i < num_polys - 1 else "")
            print("];\n")
            ecut_id = ecut_id + 1
            rcut_id = rcut_id + 1
        print_comment("===== Start of level 4, off {} =====".format(off))
        level = level + 1
    elif instr.startswith("(* vpsubw %ymm13,%ymm7,%ymm7") and level == 4:
        print(str_assertions([(7, 13)]))   # Verified
    elif instr.startswith("(* vpsubw %ymm13,%ymm4,%ymm4") and level == 4:
        print(str_assertions([(4, 13)]))   # Verified
    elif instr.startswith("(* vpaddw %ymm8,%ymm6,%ymm9") and level == 4:
        print(str_assertions([(8, 12), (11, 13)]))   # Verified

    # ==================== Level 5 ====================
    elif instr.startswith("(* vpmullw %ymm14,%ymm3,%ymm13") and level == 4:
        # End of level 4 (Verified: algebra)
        print_comment("===== End of level 4, off {} =====".format(off))
        if CUT_LEVEL[level]:
            print("\n(* ecut {0}, rcut {1} *)\n".format(ecut_id, rcut_id))
            print("cut")
            print("and [")
            print(str_level3to7_algebra(poly_name="inp_poly", args=
                                        [("zeta_0_{}".format(0+4*off), "y_0_{}".format(0+4*off),
                                         make_ymms([[10, 3], [7, 4], [9, 6], [8, 11]][i%4], 0, 4), get_ntt_mod_level3to7(i)) for i in range(4)] +
                                        [("zeta_0_{}".format(1+4*off), "y_0_{}".format(1+4*off),
                                         make_ymms([[10, 3], [7, 4], [9, 6], [8, 11]][i%4], 4, 4), get_ntt_mod_level3to7(i)) for i in range(4)] +
                                        [("zeta_0_{}".format(2+4*off), "y_0_{}".format(2+4*off),
                                         make_ymms([[10, 3], [7, 4], [9, 6], [8, 11]][i%4], 8, 4), get_ntt_mod_level3to7(i)) for i in range(4)] +
                                        [("zeta_0_{}".format(3+4*off), "y_0_{}".format(3+4*off),
                                         make_ymms([[10, 3], [7, 4], [9, 6], [8, 11]][i%4], 12, 4), get_ntt_mod_level3to7(i)) for i in range(4)], expn=8))
            # [
            #     ("zeta_0_0", "y_0_0", make_ymms([10, 3], 0, 4), 1),
            #     ("zeta_0_0", "y_0_0", make_ymms([7, 4], 0, 4), -1),
            #     ("zeta_0_0", "y_0_0", make_ymms([9, 6], 0, 4), ntt_mod(num_ans=ANS_NUM, prime=P, mont=MONT, root=ROOT, negacyclic=True, stage=1)[0]["modulo"]),
            #     ("zeta_0_0", "y_0_0", make_ymms([8, 11], 0, 4), ntt_mod(num_ans=ANS_NUM, prime=P, mont=MONT, root=ROOT, negacyclic=True, stage=1)[1]["modulo"]),
            #     ("zeta_0_1", "y_0_1", make_ymms([10, 3], 4, 4), 1),
            #     ("zeta_0_1", "y_0_1", make_ymms([7, 4], 4, 4), -1),
            #     ("zeta_0_1", "y_0_1", make_ymms([9, 6], 4, 4), ntt_mod(num_ans=ANS_NUM, prime=P, mont=MONT, root=ROOT, negacyclic=True, stage=1)[0]["modulo"]),
            #     ("zeta_0_1", "y_0_1", make_ymms([8, 11], 4, 4), ntt_mod(num_ans=ANS_NUM, prime=P, mont=MONT, root=ROOT, negacyclic=True, stage=1)[1]["modulo"]),
            #     ("zeta_0_2", "y_0_2", make_ymms([10, 3], 8, 4), 1),
            #     ("zeta_0_2", "y_0_2", make_ymms([7, 4], 8, 4), -1),
            #     ("zeta_0_2", "y_0_2", make_ymms([9, 6], 8, 4), ntt_mod(num_ans=ANS_NUM, prime=P, mont=MONT, root=ROOT, negacyclic=True, stage=1)[0]["modulo"]),
            #     ("zeta_0_2", "y_0_2", make_ymms([8, 11], 8, 4), ntt_mod(num_ans=ANS_NUM, prime=P, mont=MONT, root=ROOT, negacyclic=True, stage=1)[1]["modulo"]),
            #     ("zeta_0_3", "y_0_3", make_ymms([10, 3], 12, 4), 1),
            #     ("zeta_0_3", "y_0_3", make_ymms([7, 4], 12, 4), -1),
            #     ("zeta_0_3", "y_0_3", make_ymms([9, 6], 12, 4), ntt_mod(num_ans=ANS_NUM, prime=P, mont=MONT, root=ROOT, negacyclic=True, stage=1)[0]["modulo"]),
            #     ("zeta_0_3", "y_0_3", make_ymms([8, 11], 12, 4), ntt_mod(num_ans=ANS_NUM, prime=P, mont=MONT, root=ROOT, negacyclic=True, stage=1)[1]["modulo"])
            # ]
            print("] && and [")
            print("true")
            print("];")
            ecut_id = ecut_id + 1
            #rcut_id = rcut_id + 1
        print_comment("===== Start of level 5, off {} =====".format(off))
        level = level + 1
    elif instr.startswith("(* vpsubw %ymm13,%ymm3,%ymm3") and level == 5:
        print(str_assertions([(3, 13)]))   # Verified
    elif instr.startswith("(* vpaddw %ymm4,%ymm7,%ymm10") and level == 5:
        print(str_assertions([(4, 12), (6, 13), (11, 14)]))   # Verified

    # ==================== Level 6 ====================
    elif instr.startswith("(* vpmullw 0x80(%rdx),%ymm5,%ymm12") and level == 5:
        # End of level 5 (Verified: algebra)
        print_comment("===== End of level 5, off {} =====".format(off))
        if CUT_LEVEL[level]:
            print("\n(* ecut {0}, rcut {1} *)\n".format(ecut_id, rcut_id))
            print("cut")
            print("and [")
            print(str_level3to7_algebra(poly_name="inp_poly", args=
                                        [("zeta_0_{}".format(0+4*off), "y_0_{}".format(0+4*off),
                                         make_ymms([5, 3, 10, 4, 7, 6, 9, 11][i:i+1], 0, 4), get_ntt_mod_level3to7(i)) for i in range(8)] +
                                        [("zeta_0_{}".format(1+4*off), "y_0_{}".format(1+4*off),
                                         make_ymms([5, 3, 10, 4, 7, 6, 9, 11][i:i+1], 4, 4), get_ntt_mod_level3to7(i)) for i in range(8)] +
                                        [("zeta_0_{}".format(2+4*off), "y_0_{}".format(2+4*off),
                                         make_ymms([5, 3, 10, 4, 7, 6, 9, 11][i:i+1], 8, 4), get_ntt_mod_level3to7(i)) for i in range(8)] +
                                        [("zeta_0_{}".format(3+4*off), "y_0_{}".format(3+4*off),
                                         make_ymms([5, 3, 10, 4, 7, 6, 9, 11][i:i+1], 12, 4), get_ntt_mod_level3to7(i)) for i in range(8)], expn=4))
            # [
            #     ("zeta_0_0", "y_0_0", make_ymms([5], 0, 4), 1),
            #     ("zeta_0_0", "y_0_0", make_ymms([3], 0, 4), -1),
            #     ("zeta_0_0", "y_0_0", make_ymms([10], 0, 4), ntt_mod(num_ans=ANS_NUM, prime=P, mont=MONT, root=ROOT, negacyclic=True, stage=1)[0]["modulo"]),
            #     ("zeta_0_0", "y_0_0", make_ymms([4], 0, 4), ntt_mod(num_ans=ANS_NUM, prime=P, mont=MONT, root=ROOT, negacyclic=True, stage=1)[1]["modulo"]),
            #     ("zeta_0_0", "y_0_0", make_ymms([7], 0, 4), ntt_mod(num_ans=ANS_NUM, prime=P, mont=MONT, root=ROOT, negacyclic=True, stage=2)[0]["modulo"]),
            #     ("zeta_0_0", "y_0_0", make_ymms([6], 0, 4), ntt_mod(num_ans=ANS_NUM, prime=P, mont=MONT, root=ROOT, negacyclic=True, stage=2)[1]["modulo"]),
            #     ("zeta_0_0", "y_0_0", make_ymms([9], 0, 4), ntt_mod(num_ans=ANS_NUM, prime=P, mont=MONT, root=ROOT, negacyclic=True, stage=2)[2]["modulo"]),
            #     ("zeta_0_0", "y_0_0", make_ymms([11], 0, 4), ntt_mod(num_ans=ANS_NUM, prime=P, mont=MONT, root=ROOT, negacyclic=True, stage=2)[3]["modulo"]),
            #     ...
            # ]
            print("] && and [")
            print("true")
            print("];")
            ecut_id = ecut_id + 1
            #rcut_id = rcut_id + 1
        print_comment("===== Start of level 6, off {} =====".format(off))
        level = level + 1
    elif instr.startswith("(* vpsubw %ymm12,%ymm5,%ymm5") and level == 6:
        print(str_assertions([(5, 12)]))   # Verified
    elif instr.startswith("(* vpsubw %ymm12,%ymm3,%ymm3") and level == 6:
        print(str_assertions([(3, 12)]))   # Verified
    elif instr.startswith("(* vpsubw %ymm12,%ymm10,%ymm10") and level == 6:
        print(str_assertions([(10, 12)]))   # Verified
    elif instr.startswith("(* vpsubw %ymm12,%ymm4,%ymm4") and level == 6:
        print(str_assertions([(4, 12)]))   # Verified
    elif instr.startswith("(* vpsubw %ymm12,%ymm7,%ymm7") and level == 6:
        print(str_assertions([(7, 12)]))   # Verified
    elif instr.startswith("(* vpsubw %ymm12,%ymm6,%ymm6") and level == 6:
        print(str_assertions([(6, 12)]))   # Verified
    elif instr.startswith("(* vpsubw %ymm12,%ymm9,%ymm9") and level == 6:
        print(str_assertions([(9, 12)]))   # Verified
    elif instr.startswith("(* vpsubw %ymm12,%ymm11,%ymm11") and level == 6:
        print(str_assertions([(11, 12)]))   # Verified

    # ==================== Level 7 ====================
    elif instr.startswith("(* vpaddw %ymm8,%ymm4,%ymm6") and level == 6:
        # End of level 6
        print_comment("===== End of level 6, off {} =====".format(off))
        if CUT_LEVEL[level]:
            print("\n(* ecut {0}, rcut {1} *)\n".format(ecut_id, rcut_id))
            ecut_id = ecut_id + 1
            rcut_id = rcut_id + 1
        print_comment("===== Start of level 7, off {} =====".format(off))
        level = level + 1
    elif instr.startswith("(* vpaddw %ymm9,%ymm8,%ymm3") and level == 7:
        print(str_assertions([(9, 12), (11, 13)]))   # Verified
    elif instr.startswith("(* vmovdqa %ymm10,(%rdi)") and level == 7:
        print_comment("===== Store results of levels1t7, off {} =====".format(off))

    # ==================== End of level 7, off = 0 ====================
    elif instr.startswith("(* vmovdqa 0x1c0(%rdx),%ymm15"):
        print_comment("End of level 7, off {}".format(off))
        if CUT_LEVEL[level]:
            print("\n(* ecut {0}, rcut {1} *)\n".format(ecut_id, rcut_id))
            ecut_id = ecut_id + 1
            rcut_id = rcut_id + 1
        # Print the high part of cut 0
        print("\n(* ecut {0}, rcut {1} *)\n".format(ecut_id, rcut_id))
        print("cut")
        print("and [")
        print(str_level0_algebraic_condition_ith (poly='inp_poly', poly_var='x0', base=ANS_BASE, addr_off=2, stage=1, num_ans=ANS_NUM, num_bits=9,
                                                  negacyclic=True, q=P, root=ROOT, ith=1))
        print ("] prove with [ cuts [ 0 ] ] && and [")
        # print(str_level0_range_condition (base=(ANS_BASE + ANS_NUM), addr_off=2, m=1, num_ans=int(ANS_NUM / 2), q=P))   # Verified
        print(str_level0_fined_range_condition(base=(ANS_BASE + ANS_NUM), addr_off=2, ranges=FINED_BOUNDS_7681[0][int(ANS_NUM/2):], num_ans=int(ANS_NUM / 2)))   # Verified
        print("] prove with [ cuts [ 0 ] ];\n")
        ecut_id = ecut_id + 1
        rcut_id = rcut_id + 1
        off = 1
        level = 1
        print_comment("Start of level 1, off {}".format(off))
        # Start of level 1, off = 1
    print(instr)

def main():
    parser = ArgumentParser()
    parser.add_argument("cl_file", help="the nttmul_poly_ntt cl file to be processed")
    args = parser.parse_args()
    with open(args.cl_file) as f:
        # ========== proc main ==========
        print('proc main(\n')
        print(str_main_args())
        print('\n) =\n')
        # ========== pre-condition ==========
        print('{\n')
        print(str_precondition_algebra())
        print("\n&&\n")
        print(str_precondition_range())
        print('\n}\n')
        # ========== inits ==========
        print(str_inits())
        print(str_twiddles())
        print()
        print(str_init_poly_var('x0'))
        print(str_init_poly(poly='inp_poly', poly_var='x0', prefix='f', num=INPUT_NUM))
        # ========== program ==========
        print("\n\n#===== program start =====\n\n")
        for line in f.readlines():
            print_instr(line.strip())
        # ========== post-condition ==========
#      print('\n{ true && true }')


if __name__ == "__main__":
  main()
