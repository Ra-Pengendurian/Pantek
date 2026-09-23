import os
import sys
import time
import math

# Ukuran terminal
W, H = 80, 30
A, B = 30.0, 15.0  # Skala

# Warna ANSI
PINK = "\033[95m"
RED = "\033[91m"
MAGENTA = "\033[35m"
RESET = "\033[0m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"

# Karakter buat density (dari tipis ke tebal)
CHARS = ".,-~:;=!*#$@"


def render(t):
    """Render frame love berputar di sudut t."""
    zbuf = [[0.0] * W for _ in range(H)]
    buf = [[" "] * W for _ in range(H)]

    cos_t = math.cos(t)
    sin_t = math.sin(t)

    # Parametric love 2D
    for i in range(0, 628, 3):
        u = i / 100.0
        # Rumus heart
        x = 16 * math.sin(u) ** 3
        y = 13 * math.cos(u) - 5 * math.cos(2 * u) - 2 * math.cos(3 * u) - math.cos(4 * u)

        # Rotasi 3D sekitar Y axis
        x3 = x * cos_t
        z3 = x * sin_t
        y3 = y

        # Project ke 2D
        ooz = 1.0 / (z3 + 40)  # depth
        xp = int(W / 2 + A * x3 * ooz * 2)
        yp = int(H / 2 - B * y3 * ooz * 2)

        if 0 <= xp < W and 0 <= yp < H:
            if ooz > zbuf[yp][xp]:
                zbuf[yp][xp] = ooz
                # Density karakter
                idx = int(abs(y3) / 2) % len(CHARS)
                buf[yp][xp] = CHARS[-idx - 1] if idx else "@"

    # Output
    out = []
    for row in buf:
        out.append("".join(row))
    return "\n".join(out)


def main():
    print(HIDE_CURSOR, end="")
    t = 0.0
    try:
        while True:
            frame = render(t)
            # Warna selang-seling
            color = [PINK, RED, MAGENTA][int(t * 2) % 3]
            sys.stdout.write("\033[H\033[2J")  # clear + home
            sys.stdout.write(color + frame + RESET)
            sys.stdout.flush()
            time.sleep(0.05)
            t += 0.15
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write(SHOW_CURSOR + RESET + "\n")
        print("Bye! 💖")


if __name__ == "__main__":
    main()
EOF