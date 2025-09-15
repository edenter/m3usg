import re
import requests
import os

# Define the mapping of channel names to new tvg-ids
tvg_id_map = {
    "Preview Channel": "101",
    "Channel 5 HD": "102",
    "Channel 8 HD": "103",
    "Suria HD": "104",
    "Vasantham HD": "105",
    "Channel News Asia HD": "106",
    "Channel U HD": "107",
    "Hub E City HD": "111",
    "Citra Entertainment": "115",
    "Karisma": "116",
    "Astro Warna HD": "118", # 119, 120, 121, 122 are missing
    "Astro Sensasi HD": "123",
    "ONE (Malay)": "124",
    "Zee TV": "125", # 126 is missing
    "Sony Entertainment Television": "127",
    "COLORS": "128", # 129 is missing
    "Zee Cinema": "130",
    "SONY MAX": "131",
    "COLORS Tamil HD": "132",
    "Sun TV": "133",
    "Sun Music": "134",
    "Vijay TV HD": "135",
    "Vannathirai": "136",
    "Zee Thirai": "137",
    "Zee Tamil": "138",
    "Asianet": "139",
    "Asianet Movies": "140",
    "Kalaignar TV": "141", # 142 is missing
    "ANC": "143",
    "The Filipino Channel HD": "144",
    "Cinema One Global": "145", # 146, 147, 148, 149, 150, 151 are missing
    "TV5MONDE HD": "152",
    "DW English HD": "153", # 154, 155, 156, 157 are missing
    "ADITHYA TV": "158",
    "KTV HD": "159", # 160-200 are missing
    "Hub Sports 1 HD": "201",
    "Hub Sports 2 HD": "202",
    "Hub Sports 3 HD": "203",
    "Hub Sports 4 HD": "204",
    "Hub Sports 5 HD": "205",
    "Hub Sports 6": "206",
    "Hub Sports 7": "207", # 208 is missing
    "SPOTV": "209",
    "SPOTV2": "210",
    "beIN Sports 2 HD": "211", # 212 is missing
    "beIN Sports HD": "213",
    "beIN Sports 3": "214",
    "beIN Sports 4": "215",
    "beIN Sports 5": "216", # 217-220 are missing
    "Hub Premier 1": "221",
    "Hub Premier 2 HD": "222",
    "Hub Premier 3": "223",
    "Hub Premier 4": "224",
    "Hub Premier 5": "225",
    "Hub Premier 6": "226",
    "Hub Premier 7": "227",
    "Hub Premier 8": "228", # 229, 230, 231 are missing
    "Hub Premier 2 4K": "232", # 233, 234 are missing
    "MOLA Sport": "235",
    "MOLA Golf": "236", # 237, 238, 239, 240 are missing
    "FIGHT SPORTS HD": "241", # 242, 243, 244, 245, 246 are missing
    "Premier Sports": "247", # 248-302 are missing
    "Cbeebies HD": "303",
    "Nick Jr.": "304", # 305, 306 are missing
    "DreamWorks Channel HD": "307", # 308-313 are missing
    "Nickelodeon HD": "314", # 315 is missing
    "Cartoon Network": "316",
    "Cartoonito HD": "317", # 318-400 are missing
    "HISTORY HD": "401", # 402 is missing
    "Crime + Investigation HD": "403", # 404, 405, 406 are missing
    "BBC Earth HD": "407", # 408-421 are missing
    "Discovery HD": "422", # 423, 424, 425, 426 are missing
    "Travelxp HD": "427", # 428, 429, 430, 431 are missing
    "BBC Lifestyle": "432", # 433, 434, 435, 436 are missing
    "HGTV": "437", # 438, 439, 440, 441, 442 are missing
    "FashionTV HD": "443", # 444, 445, 446 are missing
    "ABC Australia HD": "447", # 448-508 are missing
    "ROCK Entertainment": "509", # 510 is missing
    "AXN HD": "511",
    "HITS MOVIES HD": "512", # 513 is missing
    "Lifetime HD": "514", # 515, 516, 517, 518 are missing
    "Hits HD": "519", # 520-531 are missing
    "Animax HD": "532", # 533-600 are missing
    "HBO HD": "601", # 602 is missing
    "HBO Signature HD": "603",
    "HBO Family HD": "604",
    "HBO Hits HD": "605", # 606-610 are missing
    "Cinemax HD": "611", # 612-700 are missing
    "BBC World News HD": "701",
    "Fox News Channel": "702",
    "Sky News HD": "703",
    "Euronews HD": "704", # 705, 706 are missing
    "CNBC HD": "707",
    "Bloomberg Television HD": "708",
    "Bloomberg Originals": "709", # 710 is missing
    "CNN HD": "711", # 712-719 are missing
    "SEA Today": "720", # 721 is missing
    "CGTN": "722", # 723 is missing
    "France24": "724", # 725-800 are missing
    "CCTV-4": "801", # 802, 803, 804 are missing
    "Phoenix Chinese Channel HD": "805",
    "Phoenix InfoNews HD": "806", # 807 is missing
    "TVBS NEWS HD": "808", # 809, 810 are missing
    "NHK World Premium HD": "811",
    "NHK WORLD - JAPAN HD": "812", # 813, 814 are missing
    "KBS World HD": "815", # 816 is missing
    "Arirang TV HD": "817", # 818, 819 are missing
    "ETTV ASIA HD": "820", # 821, 822 are missing
    "ONE HD": "823",
    "tvN HD": "824",
    "Hub E City HD": "825", # 826 is missing
    "CTI TV HD": "827",
    "TVBS Asia": "828", # 829, 830, 831 are missing
    "Dragon TV": "832", # 833-837 are missing
    "TVB Jade HD": "838", # 839-854 are missing
    "Hub VV Drama HD": "855", # 856, 857, 858 are missing
    "TVB Xing He": "859", # 860-867 are missing
    "Celestial Movies HD": "868",
    "CCM": "869", # 870-992 are missing
    "TestChannel 993": "993",
    "TestChannel1": "994",
    "TestChannel 995": "995",
    "TestChannel 996": "996",
    "TestChannel2": "997",
    "Test 998": "998",
}

group_title_map = {
    "教育": "Education & Lifestyle",
    "国际民族": "International/Ethnic",
    "娱乐": "Entertainment",
    "中文亚洲": "Chinese/Asian",
    "新闻": "News",
    "电影": "Movies",
    "儿童": "Kids",
    "体育": "Sports",
}

def update_m3u(input_url, output_file, tvg_id_map, group_title_map):
    """
    Reads an M3U file, updates tvg-id based on channel name, and writes to a new file.
    """
    updated_lines = []
    # Add the #EXTM3U header with url-tvg and refresh attributes
    updated_lines.append('#EXTM3U url-tvg="https://raw.githubusercontent.com/dbghelp/StarHub-TV-EPG/refs/heads/main/starhub.xml" refresh="3600"')
    
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
    # Read URL from environment variable 'M3U_URL'.
    input_url = os.environ.get('M3U_URL')
    if not input_url:
        print("Error: M3U_URL environment variable not set. Please set it in your repository's variables.")
        import sys
        sys.exit(1)

    output_file = 'updated_playlist.m3u'

    update_m3u(input_url, output_file, tvg_id_map, group_title_map)
    print(f"M3U file updated successfully! Check the new file: {output_file}")

if __name__ == "__main__":
    main()