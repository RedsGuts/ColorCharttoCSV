from struct import unpack
import csv


def read_aco(file_path):
    colors = []
    with open(file_path, 'rb') as f:
        version = unpack(">H", f.read(2))[0]  # Read the file version
        num_colors = unpack(">H", f.read(2))[0]  # Read the number of colors

        print(f"File version: {version}")  # Check if it's version 2

        # Extract colors from Version 1
        for _ in range(num_colors):
            color_space = unpack(">H", f.read(2))[0]  # Read color space
            values = unpack(">4H", f.read(8))  # Read color values (4 unsigned shorts)

            if color_space == 0:  # 0 = RGB
                r, g, b = [int(v / 256) for v in values[:3]]  # Convert 16-bit to 8-bit
                hex_value = f"#{r:02X}{g:02X}{b:02X}"  # Convert to HEX format
                colors.append([r, g, b, hex_value, ""])  # Add an empty name

        # If Version 2 exists, extract names
        if version == 2:
            f.read(4)  # Skip version 2 header
            for i in range(num_colors):
                name_length = unpack(">H", f.read(2))[0]  # Read length of name
                if name_length > 0:
                    name = f.read(name_length * 2).decode("utf-16-be").strip("\x00")  # Read name
                    colors[i][4] = name  # Update the name in colors list
                f.read(2)  # Skip the null terminator

    return colors

def write_csv(colors, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["R", "G", "B", "Hex", "Name"])  # CSV headers
        writer.writerows(colors)  # Write color data

input_file = "F:\\Project_Perso\\GitLab\\ColorChart\\ExternalRessources\\tollen.aco"  # Change to your file path
output_file = "F:\\Project_Perso\\GitLab\\ColorChart\\ExternalRessources\\colors.csv"

colors = read_aco(input_file)  # Extract colors
write_csv(colors, output_file)  # Save to CSV
print(f"CSV file saved: {output_file}")
