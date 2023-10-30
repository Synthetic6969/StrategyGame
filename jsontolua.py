import json

def dic_to_lua_str(data, layer=0):
    if isinstance(data, str):
        return "\"" + data + "\""
    elif isinstance(data, bool):
        return 'true' if data else 'false'
    elif isinstance(data, (int, float)):
        return str(data)
    elif isinstance(data, list):
        result = "{\n"
        for i, item in enumerate(data):
            result += space_str(layer + 1) + dic_to_lua_str(item, layer + 1)
            if i < len(data) - 1:
                result += ','
            result += '\n'
        result += space_str(layer) + '}'
        return result
    elif isinstance(data, dict):
        result = "{\n"
        data_len = len(data)
        data_count = 0
        for k, v in data.items():
            data_count += 1
            result += space_str(layer + 1)
            if isinstance(k, int):
                result += '[' + str(k) + ']'
            else:
                result += k
            result += ' = ' + dic_to_lua_str(v, layer + 1)
            if data_count < data_len:
                result += ',\n'
            else:
                result += '\n'
        result += space_str(layer) + '}'
        return result
    else:
        raise ValueError(f'{type(data)} is not supported')

def space_str(layer):
    return '\t' * layer

def str_to_lua_table(jsonStr):
    data_dic = json.loads(jsonStr)
    return dic_to_lua_str(data_dic)

def file_to_lua_file(jsonFile, luaFile):
    with open(luaFile, 'w', encoding='utf-8') as luafile:
        with open(jsonFile, encoding='utf-8') as jsonfile:
            luafile.write(str_to_lua_table(jsonfile.read()))

file_to_lua_file("cities_refined.json", "cities_refined.lua")
