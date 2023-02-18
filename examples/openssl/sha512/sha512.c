#include <openssl/sha.h>

SHA512_CTX c;
char data[16] = { 0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7,
                  0x8, 0x9, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf };
char out[64];

int main (void) {
  SHA512_Init (&c);
  SHA512_Update (&c, data, 16);
  SHA512_Final (out, &c);
  return (0);
}
