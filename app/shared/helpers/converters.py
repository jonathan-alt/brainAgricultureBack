def convert_json_with_bytes(data):
    if isinstance(data, bytes):
        return data.decode()
    if isinstance(data, dict):
        return dict(map(convert_json_with_bytes, data.items()))
    if isinstance(data, tuple):
        return tuple(map(convert_json_with_bytes, data))
    if isinstance(data, list):
        return list(map(convert_json_with_bytes, data))
    return data



