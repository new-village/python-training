""" sanitizer.py
"""
import re
import json
import jaconv


def execute(_record):
    meta = json.load(open('./config/data-definition.json', 'r'))
    res = dict()
    for k, v in meta.items():
        # get record value to value variable
        value = _record.get(k)
        
        # if meta has function key, execute additional process
        if v.get('function') is not None and value is not None:
            process = v.get('function') + '("' + value + '")'
            value = eval(process)

        res[k] = formatter(value, v.get('regex'), v.get('type'))

    return res


def formatter(target, reg, type="str"):
    if reg is not None:
        # Extract target variables
        fmt = re.compile(reg)
        val = fmt.findall(target)[0] if target is not None and fmt.search(target) else None
    else:
        val = target

    # Redact comma from numerical values
    if isinstance(val, str) and (type == "int" or type == "float") and val is not None:
        val = re.sub(",", "", val)

    # Convert type
    if type == "int":
        value = int(val) if val is not None else 0
    elif type == "float":
        value = float(val) if val is not None else 0
    else:
        value = str(val) if val is not None else ""

    return value


def JpnYear_to_ad(value):
    fmt = re.compile(r'(明治|大正|昭和|平成|令和)(元|\d{1,2})年')
    value = ["".join(x) for x in fmt.findall(value)[0]]
    year = int(value[1]) if value[1] != '元' else 0

    if value[0] == "明治":
        year += 1868
    elif value[0] == "大正":
        year += 1912
    elif value[0] == "昭和":
        year += 1926
    elif value[0] == "平成":
        year += 1989
    elif value[0] == "令和":
        year += 2019

    return year

def jp_normalize(value):
    normalized = jaconv.z2h(value, kana=False, ascii=True, digit=True)
    return normalized