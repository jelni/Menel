def cut_long_text(text: str, max_length: int = 2000):
    if len(text) > max_length:
        return f'{text[:max_length - 1].rstrip()}…'
    else:
        return text