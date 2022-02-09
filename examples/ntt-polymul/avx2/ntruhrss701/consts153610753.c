#include <stdint.h>
#include "params.h"
#include "consts1536.h"

#define P 10753
#define PINV -10751 // p^-1 mod 2^16
#define MONT 1018 // 2^16 mod p
#define MONT_PINV -6
#define V 12482 // floor(2^27/p + 0.5)
#define SHIFT 16
#define F 1268 // mont^2/512
#define F_PINV -780 // pinv*F

__attribute__((aligned(32)))
const int16_t pdata10753[] = {
#define _16XP 0
  P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P,

#define _16XPINV 16
  PINV, PINV, PINV, PINV, PINV, PINV, PINV, PINV,
  PINV, PINV, PINV, PINV, PINV, PINV, PINV, PINV,

#define _16XV 32
  V, V, V, V, V, V, V, V, V, V, V, V, V, V, V, V,

#define _16XSHIFT 48
  SHIFT, SHIFT, SHIFT, SHIFT, SHIFT, SHIFT, SHIFT, SHIFT,
  SHIFT, SHIFT, SHIFT, SHIFT, SHIFT, SHIFT, SHIFT, SHIFT,

#define _16XMONT_PINV 64
  MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV,
  MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV, MONT_PINV,

#define _16XMONT 80
  MONT, MONT, MONT, MONT, MONT, MONT, MONT, MONT,
  MONT, MONT, MONT, MONT, MONT, MONT, MONT, MONT,

#define _16XF_PINV 96
  F_PINV, F_PINV, F_PINV, F_PINV, F_PINV, F_PINV, F_PINV, F_PINV,
  F_PINV, F_PINV, F_PINV, F_PINV, F_PINV, F_PINV, F_PINV, F_PINV,

#define _16XF 112
  F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F,


#define _ZETAS_PINV 128
  -27359, -27359,    408,    408,  -1956,  -1956,  28517,  28517,
   20856,  20856, -10093, -10093, -21094, -21094,  18345,  18345,

#define _ZETAS 144
    -223,   -223,  -3688,  -3688,   4188,   4188,    357,    357,
     376,    376,  -2413,  -2413,  -3686,  -3686,    425,    425,

#define _TWIST96 160
      -6, -20624,   2980,  -7228, -15572,  -4315,  12476,  12896,
   -5814, -14847,  25153, -14499,  21094,  12232, -25646, -17675,
    1018,   3952,  -3164,   3012,  -1236,    293,   2236,  -3488,
    3402,  -4095,   3137,   2397,   3686,    -56,   4050,  -4875,
   23702,  -7899,   9508,  -4163,   3797,   3925, -21715, -18765,
    1956,   1286,  26366,  26518,  17839,   8868,  -7033, -10952,
   -1898,  -3291,   3364,  -3651,    213,    341,   3373,   5299,
   -4188,    262,   4862,    918,  -1105,   2724,   2695,   1336,
   31388, -18363, -13091,   1195, -20856,   5686, -25049, -28103,
   -6223, -20423,  28224,  25494,  26353, -14731,  23800,  -5589,
    4764,   2629,   3805,   4779,   -376,  -3530,   1063,  -5063,
   -3663,   2617,  -4544,   -106,  -3855,  -1931,   3320,  -2005,
   27359, -19582,  -9197,   7429, -24720, -28499,  29449, -23312,
   17138,  -3639,   8021,   9764,  10093,   9697, -20167, -23056,
     223,   1922,  -1517,  -4347,   -144,  -3411,  -4855,   1264,
   -2318,  -5175,   4437,   3620,   2413,   4065,   2873,   1520,
   31394,   2261, -16072,   8423,  -5284,  10001,  28011,  24537,
    -408,  -5577,   3072, -25543,   5260, -26963, -16090,  12086,
    3746,  -1323,  -3784,   1767,    860,  -3823,  -1173,  -1575,
    3688,  -4041,   3072,  -2503,   3212,  -1875,   -730,   2870,
    3657, -11683, -18705,  11592, -28517, -32424, -14371,  -4547,
   15182,  -4924, -18345, -16754,  -7746,    829, -13134, -12104,
    2121,   5213,  -4881,   -696,   -357,  -3752,   2525,  -4035,
    1870,   5316,   -425,   2702,   3518,   1341,    178,    184,
      -6,  12104,  13134,   -829,   7746,  16754,  18345,   4924,
  -15182,   4547,  14371,  32424,  28517, -11592,  18705,  11683,
    1018,   -184,   -178,  -1341,  -3518,  -2702,    425,  -5316,
   -1870,   4035,  -2525,   3752,    357,    696,   4881,  -5213,
   -3657, -12086,  16090,  26963,  -5260,  25543,  -3072,   5577,
     408, -24537, -28011, -10001,   5284,  -8423,  16072,  -2261,
   -2121,  -2870,    730,   1875,  -3212,   2503,  -3072,   4041,
   -3688,   1575,   1173,   3823,   -860,  -1767,   3784,   1323,
  -31394,  23056,  20167,  -9697, -10093,  -9764,  -8021,   3639,
  -17138,  23312, -29449,  28499,  24720,  -7429,   9197,  19582,
   -3746,  -1520,  -2873,  -4065,  -2413,  -3620,  -4437,   5175,
    2318,  -1264,   4855,   3411,    144,   4347,   1517,  -1922,
  -27359,   5589, -23800,  14731, -26353, -25494, -28224,  20423,
    6223,  28103,  25049,  -5686,  20856,  -1195,  13091,  18363,
    -223,   2005,  -3320,   1931,   3855,    106,   4544,  -2617,
    3663,   5063,  -1063,   3530,    376,  -4779,  -3805,  -2629,
  -31388,  10952,   7033,  -8868, -17839, -26518, -26366,  -1286,
   -1956,  18765,  21715,  -3925,  -3797,   4163,  -9508,   7899,
   -4764,  -1336,  -2695,  -2724,   1105,   -918,  -4862,   -262,
    4188,  -5299,  -3373,   -341,   -213,   3651,  -3364,   3291,
  -23702,  17675,  25646, -12232, -21094,  14499, -25153,  14847,
    5814, -12896, -12476,   4315,  15572,   7228,  -2980,  20624,
    1898,   4875,  -4050,     56,  -3686,  -2397,  -3137,   4095,
   -3402,   3488,  -2236,   -293,   1236,  -3012,   3164,  -3952,
      -6, -32606,  12104,   6924,  13134,  12397,   -829,  21965,
    7746,  24098,  16754, -18004,  18345, -27389,   4924,    573,
    1018,   5282,   -184,   4876,   -178,   4717,  -1341,  -2099,
   -3518,  -3550,  -2702,  -3668,    425,   4867,  -5316,   1085,
  -15182, -23666,   4547,  10586,  14371,  12378,  32424,  -7259,
   28517,  -2036, -11592, -20490,  18705,  -4150,  11683, -14700,
   -1870,  -4210,   4035,  -4774,  -2525,  -2982,   3752,  -2651,
     357,  -4084,    696,   3062,   4881,   5066,  -5213,   3732,
   -3657,  31369, -12086,  25360,  16090,  32369,  26963,   6381,
   -5260, -24458,  25543,  11245,  -3072,  15864,   5577,  16059,
   -2121,  -2935,  -2870,    784,    730,   2161,   1875,  -1299,
   -3212,   -906,   2503,   3565,  -3072,  -4616,   4041,  -4933,
     408,  21947, -24537,  -5126, -28011,  21398, -10001, -29876,
    5284,  23812,  -8423,  26597,  16072,     85,  -2261,  27152,
   -3688,    955,   1575,  -4102,   1173,  -4202,   3823,    844,
    -860,   1284,  -1767,  -1563,   3784,  -3499,   1323,   2576,
  -31394,  12732,  23056,  11604,  20167,  22623,  -9697,  27584,
  -10093,   5315,  -9764,  -3407,  -8021,  15938,   3639,   1883,
   -3746,   2492,  -1520,  -2732,  -2873,  -4513,  -4065,  -5184,
   -2413,   4803,  -3620,   -847,  -4437,   4674,   5175,  -2725,
  -17138,  -4589,  23312,   4821, -29449,  -6022,  28499,  31217,
   24720,    280,  -7429, -32497,   9197, -14341,  19582, -27408,
    2318,   3091,  -1264,   1237,   4855,  -4998,   3411,   1009,
     144,  -3816,   4347,  -2289,   1517,  -2565,  -1922,  -2832,
      -6,  22258, -20624,  19326,   2980,  -5059,  -7228, -13329,
  -15572, -16724,  -4315,  29840,  12476, -14073,  12896,  23007,
    1018,   2802,   3952,  -2178,  -3164,  -4547,   3012,    495,
   -1236,  -2388,    293,   5264,   2236,  -4345,  -3488,  -4129,
   -5814,    219, -14847,  21581,  25153,  23781, -14499,  -1926,
   21094, -29236,  12232,  24269, -25646,   9623, -17675,  -5516,
    3402,  -4389,  -4095,  -2483,   3137,  -4379,   2397,   -902,
    3686,   1484,    -56,    205,   4050,  -5225,  -4875,  -3468,
   23702,  12707,  -7899,  10190,   9508,  12007,  -4163,  -2316,
    3797,  27060,   3925,  18400, -21715,   5766, -18765, -19076,
   -1898,  -4189,  -3291,  -3122,   3364,   5351,  -3651,   -268,
     213,  -3660,    341,   2016,   3373,   4742,   5299,   3452,
    1956,  -1310,   1286,  22209,  26366, -14597,  26518,  18784,
   17839,  -5619,   8868, -10227,  -7033,  -4681, -10952,  20198,
   -4188,   3810,    262,    193,   4862,  -2821,    918,   2400,
   -1105,   3085,   2724,  -1523,   2695,  -3145,   1336,   2790,
   31388,  -4894, -18363,  19241, -13091, -31656,   1195,  28395,
  -20856,  13152,   5686,   8441, -25049,  -8947, -28103,   1060,
    4764,    226,   2629,   1321,   3805,  -2984,   4779,   -789,
    -376,  -3232,  -3530,  -1287,   1063,   -243,  -5063,  -5084,
   -6223, -15840, -20423,   5717,  28224,  12537,  25494,  22532,
   26353,  29919, -14731,  -8100,  23800, -15736,  -5589,  28651,
   -3663,    544,   2617,   2133,  -4544,   2809,   -106,      4,
   -3855,   2783,  -1931,  -1956,   3320,   4744,  -2005,   -533,
      -6,  -4120, -32606, -21892,  12104,  -9684,   6924,  27261,
   13134,  31235,  12397,  -8533,   -829,  29504,  21965, -28200,
    1018,    -24,   5282,    636,   -184,   4652,   4876,  -4995,
    -178,  -2045,   4717,  -4949,  -1341,  -3264,  -2099,    472,
    7746,  -6363,  24098, -27993,  16754, -11854, -18004,  19223,
   18345,  14889, -27389,  31418,   4924, -13378,    573,  -5936,
   -3518,  -1755,  -3550,  -1881,  -2702,   1458,  -3668,   4375,
     425,  -3031,   4867,   -326,  -5316,  -2114,   1085,   2256,
  -15182,  26238, -23666,  -7167,   4547,  -6674,  10586,  13012,
   14371,  15627,  12378, -20893,  32424,  29364,  -7259,   8283,
   -1870,   4734,  -4210,   3585,   4035,  -3602,  -4774,  -1324,
   -2525,   2827,  -2982,  -5021,   3752,  -1356,  -2651,   3675,
   28517,   9886,  -2036,    177, -11592,  28084, -20490, -23336,
   18705,  -4175,  -4150,  12330,  11683, -31820, -14700,  24037,
     357,   4766,  -4084,   2737,    696,  -2636,   3062,   5336,
    4881,  -1615,   5066,   5162,  -5213,   2996,   3732,  -4123,
   -3657,  18369,  31369, -28035, -12086,  22044,  25360, -27121,
   16090,  -2182,  32369,  -7716,  26963,   7862,   6381, -11738,
   -2121,  -3647,  -2935,   5245,  -2870,  -4580,    784,   3087,
     730,  -1158,   2161,  -1572,   1875,  -1354,  -1299,   3622,
   -5260, -16614, -24458, -18479,  25543,  30943,  11245,   -780,
   -3072,  20673,  15864, -23550,   5577, -31290,  16059, -22782,
   -3212,    794,   -906,    465,   2503,   3807,   3565,   1268,
   -3072,  -1343,  -4616,  -2046,   4041,    454,  -4933,  -1278,
      -6,  17096,  19326, -11726,  -7228,  24702, -16724, -13579,
   12476,   1627,  23007,  17248, -14847,  29407,  23781,   8801,
    1018,   4808,  -2178,   1586,   3012,   3198,  -2388,   -779,
    2236,  -2981,  -4129,    864,  -4095,   2271,  -4379,   3169,
   21094,  11300,  24269,  17412, -17675,  31887,  12707,   7356,
    9508,   4090,  -2316,   8246,   3925,    512,   5766,  14999,
    3686,   5156,    205,  -5116,  -4875,  -3441,  -4189,  -2884,
    3364,   5114,   -268,   -970,    341,    512,   4742,    151,
    1956,  17352,  22209,  28541,  26518,    609,  -5619, -32076,
   -7033,   1932,  20198, -31558, -18363,  -2395, -31656,  -6978,
   -4188,   5064,    193,  -3715,    918,  -5023,   3085,   2740,
    2695,   -116,   2790,   2234,   2629,   2213,  -2984,   4286,
  -20856, -22666,   8441, -18845, -28103, -12214, -15840,  -2066,
   28224,  -2017,  22532, -25555, -14731,  32271, -15736, -30546,
    -376,    886,  -1287,  -2973,  -5063,  -2998,    544,   1006,
   -4544,   3615,      4,   -467,  -1931,  -3057,   4744,   5294,
   27359,    719,  14341,  13268,   7429,    969, -31217,   7326,
   29449, -30351,   4589, -27895,  -3639, -17571,   3407,  11842,
     223,  -1841,   2565,  -1068,  -4347,   -567,  -1009,   2206,
   -4855,   4977,  -3091,   3337,  -5175,   -675,    847,    578,
   10093,   1316, -22623,  19844, -23056, -11555, -27152,   7856,
  -16072,  -7795, -23812,  11141,  10001,  -4394,   5126, -24976,
    2413,  -4828,   4513,  -2684,   1520,   5341,  -2576,   -336,
   -3784,    909,  -1284,   -635,  -3823,   2774,   4102,   -400,
      -6, -21892,   6924,  31235,   -829, -28200,  24098, -11854,
   18345,  31418,    573,  26238,   4547,  13012,  12378,  29364,
    1018,    636,   4876,  -2045,  -1341,    472,  -3550,   1458,
     425,   -326,   1085,   4734,   4035,  -1324,  -2982,  -1356,
   28517,    177, -20490,  -4175,  11683,  24037,  31369,  22044,
   16090,  -7716,   6381, -16614,  25543,   -780,  15864, -31290,
     357,   2737,   3062,  -1615,  -5213,  -4123,  -2935,  -4580,
     730,  -1572,  -1299,    794,   2503,   1268,  -4616,    454,
     408,  24976,  -5126,   4394, -10001, -11141,  23812,   7795,
   16072,  -7856,  27152,  11555,  23056, -19844,  22623,  -1316,
   -3688,    400,  -4102,  -2774,   3823,    635,   1284,   -909,
    3784,    336,   2576,  -5341,  -1520,   2684,  -4513,   4828,
  -10093, -11842,  -3407,  17571,   3639,  27895,  -4589,  30351,
  -29449,  -7326,  31217,   -969,  -7429, -13268, -14341,   -719,
   -2413,   -578,   -847,    675,   5175,  -3337,   3091,  -4977,
    4855,  -2206,   1009,    567,   4347,   1068,  -2565,   1841,
  -27359,  30546,  15736, -32271,  14731,  25555, -22532,   2017,
  -28224,   2066,  15840,  12214,  28103,  18845,  -8441,  22666,
    -223,  -5294,  -4744,   3057,   1931,    467,     -4,  -3615,
    4544,  -1006,   -544,   2998,   5063,   2973,   1287,   -886,
   20856,   6978,  31656,   2395,  18363,  31558, -20198,  -1932,
    7033,  32076,   5619,   -609, -26518, -28541, -22209, -17352,
     376,  -4286,   2984,  -2213,  -2629,  -2234,  -2790,    116,
   -2695,  -2740,  -3085,   5023,   -918,   3715,   -193,  -5064,
      -6, -27048,  22258,  17096, -20624,  22849,  19326, -16937,
    2980, -11726,  -5059,  28883,  -7228, -32003, -13329,  24702,
    1018,   1624,   2802,   4808,   3952,    833,  -2178,    983,
   -3164,   1586,  -4547,   3795,   3012,   1277,    495,   3198,
  -15572,  32454, -16724,  32162,  -4315, -13579,  29840, -20509,
   12476, -10355, -14073,   1627,  12896,  20960,  23007,   1682,
   -1236,  -1338,  -2388,   4514,    293,   -779,   5264,  -4637,
    2236,  -1651,  -4345,  -2981,  -3488,   4576,  -4129,  -1390,
   -5814,  17248,    219,  -9307, -14847, -25616,  21581,  29407,
   25153,  19911,  23781,  28925, -14499,   8801,  -1926, -27536,
    3402,    864,  -4389,  -4699,  -4095,  -1040,  -2483,   2271,
    3137,  -3129,  -4379,  -3331,   2397,   3169,   -902,  -2960,
   21094,  28243, -29236,  11300,  12232,  21831,  24269,  30089,
  -25646,  17412,   9623, -20442, -17675,   6954,  -5516,  31887,
    3686,   3155,   1484,   5156,    -56,  -1209,    205,  -4215,
    4050,  -5116,  -5225,  -5082,  -4875,   -214,  -3468,  -3441,
   23702,   4979,  12707, -31101,  -7899,   7356,  10190,   4669,
    9508, -10068,  12007,   4090,  -4163,   7265,  -2316,  10855,
   -1898,  -3725,  -4189,   1155,  -3291,  -2884,  -3122,   5181,
    3364,   4268,   5351,   5114,  -3651,   1633,   -268,   4199,
    3797,   8246,  27060,  31839,   3925, -13567,  18400,    512,
  -21715,  30894,   5766,  28511, -18765,  14999, -19076,  11799,
     213,   -970,  -3660,   4703,    341,  -2815,   2016,    512,
    3373,   1198,   4742,   1375,   5299,    151,   3452,  -3049,
      -6,   -158,  -4120,  23952, -32606,   4199, -21892,  20630,
   12104, -12976,  -9684,  10349,   6924, -16596,  27261, -12098,
    1018,   4962,    -24,   -624,   5282,  -2457,    636,  -4970,
    -184,  -4784,   4652,   2669,   4876,  -2260,  -4995,   -834,
   13134,  13804,  31235,  25683,  12397,  -5369,  -8533, -25238,
    -829, -21551,  29504, -19320,  21965, -18729, -28200, -12305,
    -178,  -4628,  -2045,    595,   4717,   4359,  -4949,    362,
   -1341,  -2607,  -3264,   1160,  -2099,   -809,    472,   1519,
    7746,   4797,  -6363,  31174,  24098, -28803, -27993,  -6917,
   16754, -23141, -11854,  19472, -18004,  -9343,  19223, -24501,
   -3518,   5309,  -1755,  -2618,  -3550,   4477,  -1881,   4859,
   -2702,   5019,   1458,  -5104,  -3668,   1409,   4375,  -4533,
   18345,  18217,  14889,  -6095, -27389,   8770,  31418,  30437,
    4924,  -3035, -13378, -20143,    573,  14895,  -5936, -23269,
     425,    297,  -3031,  -3535,   4867,  -2494,   -326,   2277,
   -5316,   1573,  -2114,  -1199,   1085,  -4049,   2256,   4891,
  -15182,  -1511,  26238,  26817, -23666, -25482,  -7167,  10257,
    4547, -12860,  -6674,  23093,  10586,  13104,  13012,  10635,
   -1870,   5145,   4734,   4801,  -4210,  -1930,   3585,  -3567,
    4035,  -2620,  -3602,   3125,  -4774,   4912,  -1324,  -2165,
   14371, -19564,  15627,  13079,  12378,  -5845, -20893, -18918,
   32424,  -8953,  29364, -22965,  -7259,   7880,   8283,  18741,
   -2525,  -1132,   2827,  -1769,  -2982,  -2261,  -5021,  -1510,
    3752,    775,  -1356,  -2997,  -2651,  -4408,   3675,  -1227,
      -6, -11946, -16937,  30053, -13329,  23934, -13579,  -7082,
   12896, -20100,  -9307, -21855,  23781,  15462,  28243, -22215,
    1018,  -4778,    983,   1893,    495,   2430,   -779,     86,
   -3488,   2428,  -4699,   5281,  -4379,  -1946,   3155,    825,
  -25646,   -786,  31887, -22197,  10190, -15511,   7265,  17790,
    3925,  25226,  28511, -20899,  -1310, -12390,  28541, -26707,
    4050,   2286,  -3441,  -2229,  -3122,   -663,   1633,  -3714,
     341,   1674,   1375,  -4003,   3810,   5018,  -3715,  -1619,
   17839, -31583,  29651, -15304,  20198,   3827,  30705,  19661,
    1195, -17967, -22666,   7887,  -8947,  27572, -25506,  11818,
   -1105,  -4447,   4563,  -3016,   2790,  -4877,    497,  -4403,
    4779,    977,    886,   5327,   -243,  -3148,   2142,   4650,
   28224,   7484, -10922,  23836,  -8100, -15931, -30546,  28779,
  -19582,  23026, -23995,  25195, -31217,  25488,  17882, -13500,
   -4544,  -2756,  -3754,  -2788,  -1956,   5061,   5294,   -405,
    1922,   3570,  -3003,  -3989,  -1009,    912,   2522,  -3260,
   17138, -29065, -17571, -32637,  -5315,   3699, -23544,  -8338,
  -23056,  29803,  21191, -15127, -26597, -29285,  11141,  12988,
   -2318,   5239,   -675,   -381,  -4803,  -5005,  -3064,  -5266,
    1520,    619,  -1849,   -279,   1563,  -1125,   -635,   2748,
   28011, -17394, -13896,  27109, -15864, -30217,  18479, -22483,
  -26963, -25122, -22044, -18851,  14700, -23160,  23336,  -4595,
   -1173,   2062,  -1608,  -1051,   4616,   4087,   -465,   2605,
   -1875,   2526,   4580,  -1955,  -3732,  -2680,  -5336,   4109,
      -6,   4199,  -9684, -12098,  12397, -21551, -28200,  31174,
   16754,  -9343,  14889,  30437,    573,  -1511,  -7167,  23093,
    1018,  -2457,   4652,   -834,   4717,  -2607,    472,  -2618,
   -2702,   1409,  -3031,   2277,   1085,   5145,   3585,   3125,
   14371,  -5845,  29364,  18741,  -2036,  26286, -23336,  22526,
   11683,  11007,  18369,  -8027,  25360,  25122,  -7716,   7807,
   -2525,  -2261,  -1356,  -1227,  -4084,  -3410,   5336,   1022,
   -5213,    255,  -3647,  -3419,    784,  -2526,  -1572,  -2945,
   -5260,  19454,  30943, -20283,  15864,  13920, -22782, -31924,
  -24537,  -2194,   4394, -12988, -29876,   6314, -25025,   6064,
   -3212,  -2050,   3807,    709,  -4616,  -2464,  -1278,  -1204,
    1575,    878,  -2774,  -2748,    844,   -854,  -3009,  -2128,
   16072,   2218, -21191, -13811,  12732,   9636, -19844, -24336,
   -9697,  -3699,  -6972,  19789,  -3407, -11927,  25890, -12531,
    3784,  -4950,   1849,  -5107,   2492,   3492,   2684,    240,
   -4065,   5005,   3268,  -4275,   -847,   2921,  -1758,  -3827,
  -17138,  11751,  30351,  -6174,  -6022,  20070,     37, -25195,
   -7429,   7052,  -8843,  -1767, -27408,   9563,  30546,  -9477,
    2318,   5095,  -4977,  -1054,  -4998,   2662,   4645,   3989,
    4347,   5004,   3957,   4889,  -2832,   4955,  -5294,   2299,
  -23800,  13987,  -3437,   9069, -22532,  -7484, -20691, -30467,
   20423,  18625,  12214, -26646,   8947,  -4083,  -4565,   -506,
   -3320,  -2909,   4243,   1389,     -4,   2756,   4397,   2813,
   -2617,  -3391,   2998,  -1046,    243,   4621,   -981,  -1530,
      -6, -11123,  17096,   4248,  19326,  11952, -11726,  30053,
   -7228, -18875,  24702,  -8161, -16724,  18881, -13579,  -8935,
    1018,  -2419,   4808,    152,  -2178,   3760,   1586,   1893,
    3012,   2117,   3198,  -2529,  -2388,  -3135,   -779,  -2279,
   12476,  27329,   1627,  20661,  23007, -20100,  17248,  20173,
  -14847, -28712,  29407,  -6594,  23781,  16236,   8801,   4967,
    2236,   5313,  -2981,    693,  -4129,   2428,    864,  -3891,
   -4095,    -40,   2271,   4670,  -4379,  -2196,   3169,  -1689,
   21094,  26292,  11300, -22215,  24269, -11446,  17412,  -7192,
  -17675, -12336,  31887,  -1609,  12707,  -8758,   7356,  -9691,
    3686,  -4428,   5156,    825,    205,  -2230,  -5116,  -3096,
   -4875,  -4144,  -3441,    -73,  -4189,    458,  -2884,  -5083,
    9508, -15511,   4090,  -7722,  -2316, -32351,   8246, -24165,
    3925,  19643,    512,  16809,   5766, -29151,  14999, -20899,
    3364,   -663,   5114,   -554,   -268,  -5215,   -970,   3995,
     341,  -1349,    512,  -1111,   4742,  -2015,    151,  -4003,
    1956,  31467,  17352,  12653,  22209,  30144,  28541, -13164,
   26518,  29626,    609,  -1834,  -5619, -31583, -32076, -15517,
   -4188,   2283,   5064,   4973,    193,  -2624,  -3715,   5268,
     918,  -2118,  -5023,   5334,   3085,  -4447,   2740,    355,
   -7033,   9374,   1932, -13024,  20198,  29644, -31558,  12415,
  -18363, -24025,  -2395,  19661, -31656,  31058,  -6978, -21593,
    2695,   4254,   -116,   3360,   2790,  -5172,   2234,   1663,
    2629,   2087,   2213,  -4403,  -2984,  -4782,   4286,   4519,
      -6,  23952, -21892, -12976,   6924, -12098,  31235,  -5369,
    -829, -19320, -28200,   4797,  24098,  -6917, -11854,  -9343,
    1018,   -624,    636,  -4784,   4876,   -834,  -2045,   4359,
   -1341,   1160,    472,   5309,  -3550,   4859,   1458,   1409,
   18345,  -6095,  31418,  -3035,    573, -23269,  26238, -25482,
    4547,  23093,  13012, -19564,  12378, -18918,  29364,   7880,
     425,  -3535,   -326,   1573,   1085,   4891,   4734,  -1930,
    4035,   3125,  -1324,  -1132,  -2982,  -1510,  -1356,  -4408,
   28517,  -5120,    177,  26286, -20490, -16925,  -4175,  23160,
   11683,  24641,  24037, -29541,  31369,  -8027,  22044,   3998,
     357,  -5120,   2737,  -3410,   3062,  -1053,  -1615,   2680,
   -5213,   2625,  -4123,  -1381,  -2935,  -3419,  -4580,  -1122,
   16090,   8807,  -7716, -19863,   6381,  22483, -16614,  19454,
   25543,  18077,   -780, -14329,  15864, -22471, -31290,  24330,
     730,   2151,  -1572,  -5015,  -1299,  -2605,    794,  -2050,
    2503,   2205,   1268,  -4601,  -4616,    569,    454,    778,
     408, -31924,  24976,  17394,  -5126,  24129,   4394,  32070,
  -10001, -16273, -11141,   6314,  23812,   4717,   7795, -29370,
   -3688,  -1204,    400,  -2062,  -4102,   2113,  -2774,  -1722,
    3823,  -2449,    635,   -854,   1284,  -2963,   -909,   2374,
   16072,  15127,  -7856,   6747,  27152, -13811,  11555,   3346,
   23056,  25652, -19844,     61,  22623,  22313,  -1316,  -3699,
    3784,    279,    336,   2139,   2576,  -5107,  -5341,    274,
   -1520,  -5068,   2684,    573,  -4513,   4393,   4828,   5005,
      -6, -14268,  22849,  11952,  -5059,  19887,  24702,  23934,
   -4315,  -8935, -10355,   7624,  23007, -10306,  -9307, -28712,
    1018,  -4028,    833,   3760,  -4547,    943,   3198,   2430,
     293,  -2279,  -1651,  -4664,  -4129,    958,  -4699,    -40,
   25153,  31162,   8801,  24147, -29236, -22215,  30089, -11933,
  -17675, -22898,   4979,  -8758,  10190,    366,   4090,   5321,
    3137,   -582,   3169,   -941,   1484,    825,  -4215,   3939,
   -4875,  -3442,  -3725,    458,  -3122,   3438,   5114,   3785,
    3797, -24165, -13567,  25226,   5766,  -3242,  11799,  31467,
    1286,  -4187,  28541, -31430,  18784,  -1834,  30821,  -3754,
     213,   3995,  -2815,   1674,   4742,   3926,  -3049,   2283,
     262,    421,  -3715,   2362,   2400,   5334,   2661,   3414,
   -7033, -15304,  22185,  29644,  -4894,  11897,  -2395,  28919,
    1195, -21593, -21941,  16773,   8441, -31211,   8130,  27572,
    2695,  -3016,   4265,  -5172,    226,   2169,   2213,  -2313,
    4779,   4519,  -1973,   4997,  -1287,  -2027,  -3134,  -3148,
   -6223, -18254,  -2066,  12939,  12537, -11623, -10922,  -8545,
  -14731, -12915, -21002, -14237,  28651,  28779,    719, -20356,
   -3663,  -4942,   1006,    139,   2809,  -4967,  -3754,  -2913,
   -1931,  -4211,   2550,   1635,   -533,   -405,  -1841,   2172,
   -9197,  31497,   7088,  12640, -31217,  -6137, -15115,   5729,
  -23312,  17821, -27895, -29065, -15938, -19856, -18900,  -7106,
   -1517,  -2807,  -1104,  -3744,  -1009,   3591,  -2315,     97,
    1264,   1949,   3337,   5239,  -4674,   4720,  -4564,   4158,
      -6,  20630,  27261,  -5369,  21965,  31174, -11854,  18217,
    4924, -23269,  -7167,  13104,  12378, -22965,   9886,  26286,
    1018,  -4970,  -4995,   4359,  -2099,  -2618,   1458,    297,
   -5316,   4891,   3585,   4912,  -2982,  -2997,   4766,  -3410,
   18705,  -7112,  24037,  29169,  25360,   8807,   7862,  -5680,
   25543, -20283, -23550,  24330,  21947,  27530,   4394,   2109,
    4881,   5176,  -4123,  -1039,    784,   2151,  -1354,   2512,
    2503,    709,  -2046,    778,    955,   3978,  -2774,   2621,
    5284,   4717,  22806,   2218,  27152, -27237, -11616,     61,
   -9697, -10471, -11842, -23044,  15938, -12531,  14438,  16291,
    -860,  -2963,  -2794,  -4950,   2576,    923,   4768,    573,
   -4065,  -3815,   -578,   -516,   4674,  -3827,  -2970,   -605,
  -29449,   6137,     37,   7289, -32497,  32216,   -719,   9563,
    5589,  21770, -29547,   8545, -22532, -13085,  -8734,   6716,
    4855,  -3591,   4645,  -2439,  -2289,  -4648,   1841,   4955,
    2005,  -1782,   -363,   2913,     -4,   2787,  -3614,  -3524,
    6223, -26646,  18845, -22861, -13152,  21593, -21088,  12695,
   18363, -31455, -22185,  -9374,  10227, -14908,   -609,  31430,
    3663,  -1046,   2973,   1203,   3232,  -4519,  -4704,  -2153,
   -2629,  -4319,  -4265,  -4254,   1523,  -4668,   5023,  -2362,
  -26366, -12653, -31704, -28304,  -5766, -13311, -31839,  32351,
    4163,   -366,  -7356,  -2712,   5516,   7192, -30089,   9648,
   -4862,  -4973,   5160,  -3728,  -4742,  -2559,  -4703,   5215,
    3651,  -3438,   2884,   1384,   3468,   3096,   4215,   1456,
      -6,  17644, -27048, -11123,  22258, -14268,  17096, -11946,
  -20624,   4248,  22849, -21807,  19326,  18388, -16937,  11952,
    1018,   -788,   1624,  -2419,   2802,  -4028,   4808,  -4778,
    3952,    152,    833,  -2863,  -2178,   4052,    983,   3760,
    2980,  22800, -11726,   -451,  -5059,  30053,  28883,   8673,
   -7228,  19887, -32003, -18875, -13329, -13116,  24702, -11653,
   -3164,  -1776,   1586,     61,  -4547,   1893,   3795,   3041,
    3012,    943,   1277,   2117,    495,  -2876,   3198,    123,
  -15572,  -8161,  32454,  23934, -16724, -15767,  32162,  18881,
   -4315, -25372, -13579, -10605,  29840,  -8935, -20509,  -3309,
   -1236,  -2529,  -1338,   2430,  -2388,   -919,   4514,  -3135,
     293,   1252,   -779,  -2925,   5264,  -2279,  -4637,   4371,
   12476,  -7082, -10355,  27329, -14073, -23227,   1627,   7624,
   12896,  20661,  20960,   8368,  23007, -21801,   1682, -20100,
    2236,     86,  -1651,   5313,  -4345,  -2235,  -2981,  -4664,
   -3488,    693,   4576,    176,  -4129,  -3881,  -1390,   2428,
   -5814, -10306,  17248,   5705,    219,  20173,  -9307,   7204,
  -14847, -10653, -25616, -28712,  21581, -21855,  29407,  -1390,
    3402,    958,    864,   4169,  -4389,  -3891,  -4699,   1060,
   -4095,   5219,  -1040,    -40,  -2483,   5281,   2271,  -4462,
   25153,  -6594,  19911,  28493,  23781,  31162,  28925,  16236,
  -14499,  32210,   8801,  15462,  -1926,   4967, -27536,  24147,
    3137,   4670,  -3129,   4429,  -4379,   -582,  -3331,  -2196,
    2397,  -3630,   3169,  -1946,   -902,  -1689,  -2960,   -941,

#define _TWIST12 3232
      -6,  -5814,  23702,   1956,     -6,   7746, -15182,  28517,
    1018,   3402,  -1898,  -4188,   1018,  -3518,  -1870,    357,
   31388,  -6223,  27359,  17138,  -3657,  -5260,    408,   5284,
    4764,  -3663,    223,  -2318,  -2121,  -3212,  -3688,   -860,
   31394,   -408,   3657,  15182, -31394, -10093, -17138,  24720,
    3746,   3688,   2121,   1870,  -3746,  -2413,   2318,    144,
      -6, -15182,  -3657,    408,     -6, -15572,  -5814,  21094,
    1018,  -1870,  -2121,  -3688,   1018,  -1236,   3402,   3686,
  -31394, -17138, -27359,   6223,  23702,   3797,   1956,  17839,
   -3746,   2318,   -223,   3663,  -1898,    213,  -4188,  -1105,
  -31388,  -1956, -23702,   5814,  31388, -20856,  -6223,  26353,
   -4764,   4188,   1898,  -3402,   4764,   -376,  -3663,  -3855,
      -6,  13134,   7746,  18345,     -6,  18345,  28517,  16090,
    1018,   -178,  -3518,    425,   1018,    425,    357,    730,
  -15182,  14371,  28517,  18705,    408,  16072, -10093, -29449,
   -1870,  -2525,    357,   4881,  -3688,   3784,  -2413,   4855,
   -3657,  16090,  -5260,  -3072, -27359, -28224,  20856,   7033,
   -2121,    730,  -3212,  -3072,   -223,   4544,    376,  -2695,
      -6,  12476,  21094,   9508,     -6,   2980, -15572,  12476,
    1018,   2236,   3686,   3364,   1018,  -3164,  -1236,   2236,
    1956,  -7033, -20856,  28224,  -5814,  25153,  21094, -25646,
   -4188,   2695,   -376,  -4544,   3402,   3137,   3686,   4050,
   27359,  29449,  10093, -16072,  23702,   9508,   3797, -21715,
     223,  -4855,   2413,  -3784,  -1898,   3364,    213,   3373,
};
