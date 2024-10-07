# HP8596E_Plot

Read screenshot from HP8596E (or similar) spectrum analyzer via Arduino Uno R3 configured as parallel port (Centronics/IEEE1284) printer emulator, with Python program receiving, decoding and saving image as PNG.

(I should have named this repo `HP8596E_Print` since it's actually about *printing* instead of *plotting*, which is an alternative mode.)

## Setup

### Arduino

Load Arduino Uno R3 with sketch in `HP8596E_Print_Arduino`.

The pinout and wiring of Arduino to D-SUB connector is described at the top of the sketch.

Beware: If you decide to change the mapping of the `STROBE_IN_N` pin, make sure to also adapt the Pin Change Interrupt settings to the new pin. All other pins can be wired freely.

### Python

Set your correct serial port in `HP8596E_Print_Python/HP8596E_Print_Python.py` and run.

### HP8596E

**Python program supports Epson MX-80 Printer only.**

Go to `Config`, `Set B&W Printer`, select `EP MX80 LRG`.

## Example Screenshot

Press `COPY` on your HP8596E to initiate the data transfer. This takes about 6 seconds. On success, the image is saved to disk and displayed. (Press `q` to close the related matplotlib window.)

This is what a screenshot looks like:


![Example Print](HP8596E_Plot_Python/data/2024-10-07%2013-03-48.png)

## License

Do what the fuck you want with this. (WTFPL)
