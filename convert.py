import pandas as pd
from datetime import datetime
import os


def convert_to_gpx(input_file, output_file):
    df = pd.read_csv(input_file)

    # Check available columns
    print(f"Processing {input_file}")
    print("Available columns:", df.columns)

    # Ensure required columns exist
    if not {'Date', 'Latitude', 'Longitude', 'Steps'}.issubset(df.columns):
        print(f"Skipping {input_file} — missing required columns: Date, Latitude, Longitude, Steps")
        return

    # Prepare GPX content
    gpx_header = """<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="Samsung Health to GPX Converter">
<trk>
  <name>Converted Activity</name>
  <trkseg>"""

    gpx_footer = """
  </trkseg>
</trk>
</gpx>"""

    gpx_points = []

    for index, row in df.iterrows():
        timestamp = datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S').isoformat() + 'Z'
        lat, lon = row['Latitude'], row['Longitude']
        steps = row['Steps']

        gpx_point = f"""
    <trkpt lat="{lat}" lon="{lon}">
      <time>{timestamp}</time>
      <extensions>
        <steps>{steps}</steps>
      </extensions>
    </trkpt>"""
        gpx_points.append(gpx_point)

    # Write GPX file
    with open(output_file, 'w') as f:
        f.write(gpx_header)
        f.write("".join(gpx_points))
        f.write(gpx_footer)

    print(f"GPX file saved to {output_file}")


def process_all_csv_files(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith('.csv'):
                input_path = os.path.join(dirpath, file)
                output_path = os.path.splitext(input_path)[0] + '.gpx'
                convert_to_gpx(input_path, output_path)


if __name__ == "__main__":
    root_dir = "."  # Set this to your base directory
    process_all_csv_files(root_dir)

    print("Batch conversion complete! 🚀")

# The script now converts every CSV in subfolders to GPX! Let me know if you want me to add anything else! 🌟
