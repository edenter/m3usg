import re
import requests
import os
import configparser

def load_config(config_file='config.ini'):
    """
    Loads configuration from an INI file.
    """
    config = configparser.ConfigParser()
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config.read_file(f)
    except FileNotFoundError:
        print(f"Error: Config file '{config_file}' not found.")
        import sys
        sys.exit(1)

    epg_url = config.get(
        'epg', 'url',
    )
    
    group_title_map = dict(config['group_titles']) if 'group_titles' in config else {}
    tvg_id_map = dict(config['tvg_ids']) if 'tvg_ids' in config else {}

    return epg_url, tvg_id_map, group_title_map

def update_m3u(input_url, output_file, epg_url, tvg_id_map, group_title_map):
    """
    Reads an M3U file, updates tvg-id based on channel name, and writes to a new file.
    """
    updated_lines = []
    # Add the #EXTM3U header with url-tvg and refresh attributes
    updated_lines.append(f'#EXTM3U url-tvg="{epg_url}" refresh="3600"')
    
    # Skip initial #EXTM3U lines from the input, as we've added our own header.
    # Fetch the M3U content from the URL
    try:
        response = requests.get(input_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        lines = response.text.splitlines()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching M3U from URL: {e}")
        return

    # Find the first line that doesn't start with #EXTM3U
    first_content_line_index = 0
    for i, line in enumerate(lines):
        if not line.strip().startswith('#EXTM3U'):
            first_content_line_index = i
            break
    lines = lines[first_content_line_index:]

    for i, line in enumerate(lines):
        if line.startswith('#EXTINF:-1'):
            updated_line = line
            # First, attempt to update the tvg-id
            for channel_name, new_tvg_id in tvg_id_map.items():
                if re.search(r',' + re.escape(channel_name) + r'(?=\s|$)', updated_line, re.IGNORECASE):
                    # Use a regular expression to find and replace the tvg-id
                    # The pattern looks for tvg-id=" followed by any characters until the next quote
                    updated_line = re.sub(r'tvg-id=".*?"', f'tvg-id="{new_tvg_id}"', updated_line)
                    break
            
            # Second, always attempt to replace the group-title
            group_title_match = re.search(r'group-title="(.*?)"', updated_line)
            if group_title_match:
                old_group = group_title_match.group(1)
                if old_group in group_title_map:
                    new_group = group_title_map[old_group]
                    updated_line = updated_line.replace(f'group-title="{old_group}"', f'group-title="{new_group}"')
            updated_lines.append(updated_line)
        else:
            updated_lines.append(line)
    
    # Write the updated lines to the new file
    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(updated_lines))

def main():
    """Main function to run the script."""
    epg_url, tvg_id_map, group_title_map = load_config('config.ini')

    # Read URL from environment variable 'M3U_URL'.
    input_url = os.environ.get('M3U_URL')
    if not input_url:
        print("Error: M3U_URL environment variable not set. Please set it in your repository's variables.")
        import sys
        sys.exit(1)

    output_file = 'updated_playlist.m3u'

    update_m3u(input_url, output_file, epg_url, tvg_id_map, group_title_map)
    print(f"M3U file updated successfully! Check the new file: {output_file}")

if __name__ == "__main__":
    main()