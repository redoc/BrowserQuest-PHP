import os, json
from collections import OrderedDict
from excel2xx import Excel
import cbox


curdir = os.path.dirname(__file__)

def read_excel(fname: str) -> Excel:
    fpath = os.path.join(curdir, fname)
    return Excel(fpath)

def export_entities():
    rs = OrderedDict()
    rs = []
    cache = set()
    for sheet in read_excel("entities.xlsx"):
        for row in sheet.toDict().values():
            if row['id'] in cache:
                raise Exception("duplicated id: {row['id']}  row={row}")
            cache.add(row['id'])
            rs.append(row)
            pass
        pass
    return rs


def export_messages():
    return read_excel("messages.xlsx")[0].toList()


def export_all():
    return {
        "entities": export_entities(),
        "messages": export_messages(),
    }

def main(output):
    if not output:
        raise Exception("invalid output")
    data = export_all()
    with open(output, "w") as fp:
        fp.write(json.dumps(data,indent=4))
    print(f"exported '{output}'")
    return 0

if __name__ == "__main__":
    main("./gamedata.json")