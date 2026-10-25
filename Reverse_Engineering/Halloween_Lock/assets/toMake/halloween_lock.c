#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/ptrace.h>

/* ---- the obfuscation key is COMPUTED, never stored as a string ---- */
static void build_key(uint8_t key[16]) {
    for (int j = 0; j < 16; j++) {
        key[j] = (uint8_t)((0x1D * j + 0x37) ^ 0xA5);
    }
}

#define IV 0x6E

static uint8_t rol8(uint8_t x, int r) {
    r &= 7;
    return (uint8_t)((x << r) | (x >> (8 - r)));
}

static uint8_t ror8(uint8_t x, int r) {
    r &= 7;
    return (uint8_t)((x >> r) | (x << (8 - r)));
}

/* four-stage transform: XOR(key) -> ROL(variable) -> ADD(position) -> XOR(chain) */
static void transform_encode(const uint8_t *in, uint8_t *out, int len) {
    uint8_t key[16];
    build_key(key);
    uint8_t prev = IV;
    for (int i = 0; i < len; i++) {
        uint8_t s1 = in[i] ^ key[i % 16];
        int r = (i % 5) + 1;
        uint8_t s2 = rol8(s1, r);
        uint8_t s3 = (uint8_t)(s2 + ((i * 7 + 13) & 0xFF));
        uint8_t c = s3 ^ prev;
        out[i] = c;
        prev = c;
    }
}

static void transform_decode(const uint8_t *in, uint8_t *out, int len) {
    uint8_t key[16];
    build_key(key);
    uint8_t prev = IV;
    for (int i = 0; i < len; i++) {
        uint8_t s3 = in[i] ^ prev;
        uint8_t s2 = (uint8_t)(s3 - ((i * 7 + 13) & 0xFF));
        int r = (i % 5) + 1;
        uint8_t s1 = ror8(s2, r);
        out[i] = s1 ^ key[i % 16];
        prev = in[i];
    }
}

/* the real flag, pre-encoded with transform_encode() offline.
 * Never present in plaintext anywhere in this binary. */
static const uint8_t sealed[] = {
    152,18,218,92,202,150,149,73,100,109,131,159,51,73,102,10,
    114,186,191,106,249,145,187,176,193,114,155,84,161,68
};
static const int sealed_len = 30;

/* an UNREACHABLE target — not the transform of any real word. The
 * prompt below can never succeed; it exists purely as misdirection
 * for anyone who assumes this challenge wants a guessed password. */
static const uint8_t unreachable_target[] = {
    7,19,201,3,88,240,16,254,2,19,201,3,88,240,16,254,
    7,19,201,3,88,240,16,254,2,19,201,3,88,240
};

/* decoy: a plausible, correctly-formatted FAKE flag planted in
 * plaintext, to catch anyone running `strings` instead of actually
 * reverse engineering the transform. */
static const char *decoy = "flame{hehe_its_not_that_simple}";

static void print_banner(void) {
    printf("       _\n");
    printf("      ( )         THE ORACLE'S SEAL\n");
    printf("     _|_|_        ------------------\n");
    printf("    /|(o)(o)      I will not be asked for\n");
    printf("   ( |  __ |      my secrets. They must be\n");
    printf("    \\ |____|      taken.\n\n");
}

int main(int argc, char **argv) {
    /* keep `decoy` referenced (and therefore present in .rodata) without
     * ever actually reaching it in normal execution */
    if (getenv("__NEVER_SET__") && strcmp(getenv("__NEVER_SET__"), decoy) == 0) {
        printf("%s\n", decoy);
        return 1;
    }

    /* harmless anti-debug tripwire: discourages the laziest possible
     * "just breakpoint main and read registers" approach, though it
     * does not and cannot block proper static analysis (which never
     * executes the program at all). */
    volatile int traced = (ptrace(PTRACE_TRACEME, 0, NULL, NULL) == -1);
    (void)traced;

    char input[512];
    print_banner();
    printf("Speak the passphrase, if you believe in that sort of thing: ");
    fflush(stdout);

    if (!fgets(input, sizeof(input), stdin)) {
        printf("\nSilence answers silence. Goodbye.\n");
        return 1;
    }

    size_t len = strlen(input);
    while (len > 0 && (input[len-1] == '\n' || input[len-1] == '\r')) {
        input[--len] = '\0';
    }

    uint8_t encoded[512];
    if (len > 0 && len <= 30) {
        transform_encode((uint8_t *)input, encoded, (int)len);
    }

    int match = (len == 30) && (memcmp(encoded, unreachable_target, 30) == 0);

    if (!match) {
        printf("\nThe seal does not open for the spoken word.\n");
        printf("(Perhaps words were never the way in.)\n");
        return 1;
    }

    /* unreachable in practice — included only so the decode routine
     * is present and inspectable in the compiled binary. */
    uint8_t out[sealed_len];
    transform_decode(sealed, out, sealed_len);
    for (int i = 0; i < sealed_len; i++) putchar((char)out[i]);
    printf("\n");
    return 0;
}
