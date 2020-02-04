Tools for converting the splash screen partition of Fairphone 3

Based on:
* https://web.archive.org/web/20200203204634/https://source.codeaurora.org/quic/la/kernel/lk/tree/dev/fbcon/fbcon.c?h=LA.UM.8.6.r1-03400-89xx.0#n495
* https://web.archive.org/web/20200203205934/https://source.codeaurora.org/quic/la/kernel/lk/tree/include/dev/fbcon.h?h=LA.UM.8.6.r1-03400-89xx.0

This script needs python3 and PIL.

Usage:
```
./fromsplash.py # splash -> splash.png
./tosplash.py # splash.png -> splash
./fromsplash.py {anyname}.img # {anyname}.img -> {anyname}.png
./tosplash.py {anyname}.png # {anyname}.png -> {anyname}.img
```
