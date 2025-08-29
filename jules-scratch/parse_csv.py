import csv
import json
from datetime import datetime

def create_json_from_csv(csv_filepath, output_filepath):
    data = []
    with open(csv_filepath, 'r', encoding='utf-8') as f:
        # Use csv.reader with tab delimiter
        reader = csv.reader(f, delimiter='\t')

        # Read the header and clean it
        header = [h.replace('<', '').replace('>', '') for h in next(reader)]

        for row in reader:
            if not row:
                continue

            # Create a dictionary for the current row
            row_data = {header[i]: value for i, value in enumerate(row)}

            try:
                # Combine date and time and parse into a datetime object
                date_str = row_data['DATE'].replace('.', '-')
                time_str = row_data['TIME']
                dt_obj = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")

                # Convert to Unix timestamp in milliseconds
                timestamp = int(dt_obj.timestamp() * 1000)

                # Construct the final object for JSON serialization
                # Ensure floating point numbers are parsed correctly
                data.append({
                    "time": timestamp,
                    "open": float(row_data['OPEN']),
                    "high": float(row_data['HIGH']),
                    "low": float(row_data['LOW']),
                    "close": float(row_data['CLOSE'])
                })
            except (ValueError, KeyError) as e:
                print(f"Skipping row due to error: {row} - {e}")

    # Write the data to the output file as a JSON array
    with open(output_filepath, 'w', encoding='utf-8') as f:
        # Use a compact format for the JSON output
        json.dump(data, f, separators=(',', ':'))

# Run the conversion
create_json_from_csv('XAUUSD_M15V2.csv', 'jules-scratch/corrected_embedded_data.js')
