def format_filename(name: str) -> str:
    illegal_characters = ['*', '!', '"', "|", "?", ":", "/", "\\", "<", ">"]
    return ''.join(char for char in name if char not in illegal_characters)


def remove_extension(path: str) -> str:
    return ".".join(path.split(".")[:-1])
