def plural_word(count: int, one: str, few: str, many: str) -> str:
    if count == 1:
        word = one
    elif 10 <= count < 20:
        word = many
    else:
        last = count % 10

        if 1 < last < 5:
            word = few
        else:
            word = many

    return f'{count} {word}'