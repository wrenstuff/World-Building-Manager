import re

def clean_filename(filename):
    # Remove any characters that are not alphanumeric, underscores, or hyphens
    if not filename:
        return 'unnamed'
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', filename)