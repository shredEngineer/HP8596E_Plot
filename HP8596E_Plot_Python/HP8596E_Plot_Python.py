import os
import sys
import time
import serial
import datetime
import matplotlib.pyplot as plt

from printers.EpsonMX80 import parse_printer_data
print("HP8596E: Config -> Set B&W Printer -> EP MX80 LRG\n")

serial_baudrate = 115200
serial_device = "/dev/ttyACM0"
data_folder = "data/"
print(f"Arduino: {serial_baudrate} Baud @ {serial_device}\n")
print(f"Saving to folder: {data_folder}\n")

ser = serial.Serial(serial_device, baudrate=serial_baudrate, timeout=0.1)
ser.reset_input_buffer()

print("Waiting for data...")

while True:
    data_array = []
    start_time = time.time()
    data_transfer_initiated = False
    initial_time = start_time

    while True:
        data = ser.read(ser.in_waiting or 1)

        if data:
            if not data_transfer_initiated:
                print("\nData transfer initiated...")
                data_transfer_initiated = True
                initial_time = time.time()

            data_array.extend(data)
            start_time = time.time()

            elapsed_time = start_time - initial_time
            kib_per_second = (len(data_array) / 1024) / elapsed_time if elapsed_time > 0 else 0

            sys.stdout.write(f"\rBytes received: {len(data_array)} | Speed: {kib_per_second:.2f} KiB/s")
            sys.stdout.flush()

        elif time.time() - start_time > 2:
            break

    if data_array:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        filename_base = os.path.join(data_folder, f"{timestamp}")
        filename_bin = filename_base + ".bin"
        filename_png = filename_base + ".png"

        elapsed_time = time.time() - initial_time
        kib_per_second = (len(data_array) / 1024) / elapsed_time if elapsed_time > 0 else 0

        print(f"Average speed: {kib_per_second:.2f} KiB/s")

        try:
            bitmap_array, width, height = parse_printer_data(data_array, debug=False)

            with open(filename_bin, 'wb') as f:
                f.write(bytearray(data_array))
            print(f"\n{len(data_array)} bytes written to {filename_bin}")

            aspect_ratio = width / height
            fig_width = 5
            fig_height = fig_width / aspect_ratio

            plt.figure(figsize=(fig_width, fig_height), constrained_layout=True)
            plt.imshow(bitmap_array, cmap="gray", interpolation="nearest")
            plt.axis("off")
            plt.savefig(filename_png, format="png", bbox_inches="tight", pad_inches=0)
            plt.show()
        except Exception as e:
            print(f"\nFailed to parse printer data: {e}")

        print("\nWaiting for data...")

    time.sleep(0.1)
