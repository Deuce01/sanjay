import pandas as pd

# This script generates a sample Excel file for "Format 1" (URLs only)
# Run this script, and it will create 'format_1_urls.xlsx' in your folder.

data = {
    'Profile url': [
        'https://www.freeindianmatrimony.com/10500/',
        'https://www.freeindianmatrimony.com/10441/',
        'https://www.freeindianmatrimony.com/10440/'
    ],
    'Background music URL': [
        'https://www.free-stock-music.com/music/jay-someday-inspiring-corporate.mp3',
        'https://www.free-stock-music.com/music/scott-buckley-moonlight.mp3',
        'https://www.free-stock-music.com/music/inspiring-background-music.mp3'
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Save to Excel
output_filename = 'format_1_urls.xlsx'
df.to_excel(output_filename, index=False)

print(f"Success! Created '{output_filename}' in your folder.")