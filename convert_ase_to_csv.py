import struct
import csv
import os

def read_ase(file_path):
    colors = []
    
    with open(file_path, "rb") as f:
        # Read the ASE header
        header = f.read(4).decode("ascii")  # "ASEF"
        if header != "ASEF":
            raise ValueError("Not a valid ASE file!")

        # Read version info
        version_major, version_minor = struct.unpack(">HH", f.read(4))
        print(f"ASE Version: {version_major}.{version_minor}")

        # Read number of blocks
        num_blocks = struct.unpack(">I", f.read(4))[0]
        print(f"Number of blocks: {num_blocks}")

        for _ in range(num_blocks):
            block_type = struct.unpack(">H", f.read(2))[0]  # Should be 0x0001 for colors
            block_size = struct.unpack(">I", f.read(4))[0]  # Block length

            if block_type != 0x0001:
                f.read(block_size)  # Skip non-color blocks
                continue
            
            # Read color name (UTF-16 Big Endian)
            name_length = struct.unpack(">H", f.read(2))[0]  # Name length (in 16-bit chars)
            name = f.read(name_length * 2).decode("utf-16be").strip("\x00")

            # Read color mode (e.g., "RGB ", "CMYK", "LAB ")
            color_mode = f.read(4).decode("ascii").strip()

            # Read color values (floats) based on mode
            if color_mode == "RGB":
                r, g, b = struct.unpack(">fff", f.read(12))
                r, g, b = int(r * 255), int(g * 255), int(b * 255)  # Convert to 0-255 range
                hex_value = f"#{r:02X}{g:02X}{b:02X}"
                rvb_format = f"{r:03d}-{g:03d}-{b:03d}"  # Format as 000-000-000
                colors.append([name, color_mode, r, g, b, hex_value, rvb_format])

            elif color_mode == "CMYK":
                c, m, y, k = struct.unpack(">ffff", f.read(16))
                c, m, y, k = round(c * 100, 1), round(m * 100, 1), round(y * 100, 1), round(k * 100, 1)  # Convert to %
                colors.append([name, color_mode, c, m, y, k, "N/A", "N/A"])  # No hex or RVB for CMYK

            elif color_mode == "LAB":
                l, a, b = struct.unpack(">fff", f.read(12))
                l, a, b = round(l * 100, 1), round(a, 1), round(b, 1)  # L is 0-100, A/B are roughly -128 to 127
                colors.append([name, color_mode, l, a, b, "N/A", "N/A"])  # No hex or RVB for LAB

            else:
                f.read(block_size - (name_length * 2 + 4))  # Skip unsupported color modes

            f.read(2)  # Skip color type (usually 0)

    return colors

def write_csv(colors, input_file):
    # Get input file directory and filename without extension
    input_dir = os.path.dirname(os.path.abspath(input_file))  # Get input file directory
    base_name = os.path.splitext(os.path.basename(input_file))[0]  # Extract filename without extension
    output_file = os.path.join(input_dir, f"{base_name}.csv")  # Save CSV in the same folder

    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name", "Hex", "RVB"])  # CSV headers
        writer.writerows(colors)  # Write color data

    print(f"✅ CSV file saved: {output_file}")

# Change this to your .ASE file path
input_file = "F:\\Project_Perso\\GitLab\\ColorChart\\ExternalRessources\\Tollens_nuancie_TOTEM_façade.ase"

colors = read_ase(input_file)  # Extract colors from ASE file
write_csv(colors, input_file)  # Save to CSV in the same folder as input file
