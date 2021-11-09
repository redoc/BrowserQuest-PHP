import os, json
from lxml import etree
import cbox

def tmx2json(tmx, dest):
    def process(el, tagname):
        attrs = dict(el.attrib)
        for a in attrs.keys():
            if attrs[a].isdigit():
                attrs[a] = int(attrs[a])
        
        children = el.getchildren()
        if len(children) > 1:
            sibs = {}
            for c in children:
                if c.tag not in sibs:
                    sibs[c.tag] = []
                sibs[c.tag].append(process(c, False))
            for k in sibs.keys():
                attrs.update({k: sibs[k]})
        else:
            for c in children:
                attrs.update(process(c, True))
        return {el.tag: attrs} if tagname else attrs

    tmxfp = open(tmx)
    root = etree.parse(tmx).getroot()
    res = process(root, True)
    with open(dest, "w") as fp:
        json.dump(res, fp)
    tmxfp.close()
    print("Finished converting TMX to JSON.")
    pass


def export2json(src, dest, mode):
    from processmap import processMap, load_map
    mode_defs = ["client", "server"]
    if mode not in mode_defs:
        raise Exception(f"'mode' must be one of {mode_defs}")
    data = load_map(src)
    map = processMap(data, {"mode": mode})
    jsonMap = map.to_json() # Save the processed map object as JSON data
    # map in a .json file for ajax loading
    with open(dest, "w") as fp:
        fp.write(jsonMap)
        print(f"Finished processing map file: {dest} was saved.");
    
    # map in a .js file for web worker loading
    fpath = dest.replace(".json", ".js")
    with open(fpath, "w") as fp:
        fp.write("var mapData = " + jsonMap)
        print(f"Finished processing map file: {fpath} was saved.");
    pass


if __name__ == "__main__":
    cbox.main([tmx2json, export2json])
