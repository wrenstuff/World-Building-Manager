import re
import os

def clean_filename(filename):
    # Remove any characters that are not alphanumeric, underscores, or hyphens
    if not filename:
        return 'unnamed'
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', filename)

# def get_notes_content(notes_path):
#     if notes_path and os.path.exists(notes_path):
#         with open(notes_path, 'r', encoding='utf-8') as f:
#             return f.read()
#     return 'No notes available.'