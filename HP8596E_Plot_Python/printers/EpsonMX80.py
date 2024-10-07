import numpy as np

def parse_printer_data(data, debug):
	bitmap_data = []
	index = 0
	data_length = len(data)
	width = 0
	height = 0

	if debug:
		print("\nParsing printer data...")

	while index < data_length:
		byte = data[index]

		# Check for escape sequence (ESC, 0x1B)
		if byte == 0x1B:
			# Identify the command following ESC
			index += 1
			if index >= data_length:
				break  # Avoid index out of range if there's no command byte

			command = data[index]

			# Handle specific commands
			if command == 0x3C:  # '<' - Switch to unidirectional printing
				if debug:
					print("ESC < (Switch to unidirectional printing mode)")

			elif command == 0x4F:  # 'O' - Cancel unidirectional printing
				if debug:
					print("ESC O (Cancel unidirectional printing mode)")

			elif command == 0x33:  # '3' - Set line spacing
				index += 1
				if index < data_length:
					line_spacing = data[index]
					if debug:
						print(f"ESC 3 {line_spacing} (Set line spacing to {line_spacing}/216 inches)")

			elif command == 0x4B:  # 'K' - Graphics command
				# Graphics command ESC K n1 n2
				if index + 2 < data_length:
					n1 = data[index + 1]
					n2 = data[index + 2]
					data_length_bytes = n1 + 256 * n2
					if debug:
						print(f"ESC K {n1} {n2} (Graphics command, expecting {data_length_bytes} bytes)")

					# Check if the expected number of bytes is available
					index += 3  # Move to the start of the graphics data
					if index + data_length_bytes > data_length:
						raise ValueError(f"Not enough data for expected graphics data length: {data_length_bytes} bytes.")

					# Extract the graphics data
					graphics_data = data[index:index + data_length_bytes]
					bitmap_data.extend(graphics_data)

					# Update image dimensions
					width = max(width, data_length_bytes)  # Width extends for each graphics command's data length
					height += 8  # Each ESC K command is treated as 8 rows of graphics since each byte represents 8 vertical pixels

					index += data_length_bytes - 1  # Move past the graphics data

			else:
				if debug:
					print(f"ESC {chr(command)} (Unknown or unhandled escape sequence)")

		else:
			# Handle other control characters if needed (e.g., LF, CR)
			if debug:
				if byte == 0x0A:
					print("LF (Line Feed)")
				elif byte == 0x0D:
					print("CR (Carriage Return)")

		index += 1

	# Calculate the final resolution
	if width > 0 and height > 0:
		print(f"Final image resolution: Width = {width} pixels, Height = {height} pixels")

	bitmap_array = np.zeros((height, width), dtype=np.uint8)
	col_index = 0
	for byte_index in range(len(bitmap_data)):
		if col_index >= width:
			col_index = 0
		byte = bitmap_data[byte_index]
		for row_bit in range(8):
			row_index = (byte_index // width) * 8 + row_bit
			if row_index < height:
				if byte & (1 << (7 - row_bit)):
					bitmap_array[row_index, col_index] = 1
		col_index += 1

	return bitmap_array, width, height
