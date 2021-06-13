from urllib.parse import unquote


def unquoteName(string: str):
    result = unquote(string, encoding='utf-8', errors='replace')
    if '%u' in result:
        result = result.replace('%u', '\\u').encode(
            'utf-8').decode('unicode_escape')
    return result
