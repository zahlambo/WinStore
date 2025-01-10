import subprocess
import json

# Define the output JSON file
output_file = "winget_apps.json"

# Fetch all apps using Winget search with a wildcard query
print("Fetching all apps from Winget...")
try:
    result = subprocess.run(
        ["winget", "search", "--accept-source-agreements", "-q", "*"],
        capture_output=True,
        text=True,
        encoding='utf-8'  # Handle UnicodeDecodeError by specifying utf-8 encoding
    )

    print("Raw Winget Output:")
    print(result.stdout)  # Debugging: Show raw Winget output

    # Ensure result is captured properly
    if result.stdout:
        # Split the output into lines
        lines = result.stdout.splitlines()

        # Try to locate a separator line first
        separator_index = next(
            (i for i, line in enumerate(lines) if line.startswith("-")), None
        )

        if separator_index is not None:
            # Process lines after the separator
            data_lines = lines[separator_index + 1:]  # Lines after the separator
        else:
            # Fallback if no separator is found (assume header is the first row)
            data_lines = lines[1:]  # Skip the first line (header)

        apps = []

        for line in data_lines:
            # Split the line into its columns: Name, Id, Version, Source
            parts = line.split()
            if len(parts) >= 4:  # Ensure line has all columns
                name = " ".join(parts[:-3])  # Join all parts except last 3 as Name
                app_id = parts[-3]
                version = parts[-2]
                source = parts[-1]

                # Append the app data as a dictionary
                apps.append({
                    "Name": name,
                    "Id": app_id,
                    "Version": version,
                    "Source": source
                })

        if apps:
            # Save the apps to a JSON file
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(apps, f, indent=4, ensure_ascii=False)
            print(f"App list saved to {output_file} in JSON format")
        else:
            print("No valid app data found in Winget output.")
    else:
        print("No output captured from Winget.")
except Exception as e:
    print(f"An error occurred: {e}")
