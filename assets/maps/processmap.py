import logging
import json

log = logging.root

class Types:
    @staticmethod
    def getKindFromString(name):
        return 1

class FakeJSObject:
    def __init__(self, d=None):
        if d: self.__dict__.update(d)
        pass

    def __getattr__(self, name: str):
        if name not in self.__dict__:
            return None
        return self.__dict__[name]

    def set_attrs(self, **kwargs):
        self.__dict__.update(kwargs)
        pass

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, separators=(',', ':'))


class FakeJSArray(list):
    def __init__(self, v=None):
        pass

    def __getitem__(self, index):
        length = super().__len__(self)
        if index < 0 or index >= length:
            return None
        return super().__getitem__(index)

    def __setitem__(self, index, v):
        length = super().__len__(self)
        if v < 0:
            raise IndexError(f"invalid index: {index}, current length:{length}")
        if v < length:
            return super().__setitem__(index, v)
        elif v == length:
            return super().append(v)
        else:
            fill = index - (len(self) - 1)
            super().extend([None]*fill)
            super().__setitem__(index, v)
        pass

    def __len__(self) -> int:
        return super().__len__()


map = FakeJSObject()
mode = None
collidingTiles = {}
staticEntities = {}
mobsFirstgid = ""

def load_map(fpath) -> FakeJSObject:
    def _decoder(d):
        return FakeJSObject(d) if isinstance(d, dict) else d
    with open(fpath) as fp:
        return json.load(fp, object_hook=_decoder)
    pass

def processMap(data: FakeJSObject, options):
    global map
    global mobsFirstgid
    global staticEntities
    global collidingTiles
    global mode
    mode = options["mode"]
    Tiled = data.map
    layerIndex = 0
    tileIndex = 0
    tilesetFilepath = ""
    map.set_attrs(
        width= 0,
        height= 0,
        collisions= [],
        doors= [],
        checkpoints= []
    )
    if mode == "client":
        map.data = []
        map.high = []
        map.animated = {}
        map.blocking = []
        map.plateau = []
        map.musicAreas = []

    if mode == "server":
        map.roamingAreas = []
        map.chestAreas = []
        map.staticChests = []
        map.staticEntities = {}
    
    log.info("Processing map info...")
    map.width = Tiled.width
    map.height = Tiled.height
    map.tilesize = Tiled.tilewidth

    # Tile properties (collision, z-index, animation length...)
    tileProperties = FakeJSObject()
    def handleProp(property, id):
        if property.name == "c":
            collidingTiles[id] = True
        
        if mode == "client":
            if property.name == "v":
                map.high.append(id)
            if property.name == "length":
                if id not in map.animated:
                    map.animated[id] = {}
                map.animated[id]["l"] = property.value

            if property.name == "delay":
                if id not in map.animated:
                    map.animated[id] = {}
                map.animated[id]["d"] = property.value
    
    if isinstance(Tiled.tileset, list):
        for tileset in Tiled.tileset:
            if tileset.name == "tilesheet":
                log.info("Processing terrain properties...")
                tileProperties = tileset.tile
                for i in range(len(tileProperties)):
                    property = tileProperties[i].properties.property
                    tilePropertyId = tileProperties[i].id + 1
                    if isinstance(property, list):
                        for pi in range(len(property)):
                            handleProp(property[pi], tilePropertyId)
                    else:
                        handleProp(property, tilePropertyId)
                    pass
            elif tileset.name == "Mobs" and mode == "server":
                log.info("Processing static entity properties...")
                mobsFirstgid = tileset.firstgid
                for p in tileset.tile:
                    property = p.properties.property
                    id = p.id + 1
                    if property.name == "type":
                        staticEntities[id] = property.value
                    pass
    else:
        log.error("A tileset is missing")
    
    for i in range(len(Tiled.objectgroup)):
        group = Tiled.objectgroup[i]
        if group.name == 'doors':
            doors = group.object
            log.info("Processing doors...")
            map.doors = []
            for j in range(len(doors)):
                map.doors.append({
                    "x": int(doors[j].x / map.tilesize),
                    "y": int(doors[j].y / map.tilesize),
                    "p": 1 if doors[j].type == 'portal' else 0
                })
                doorprops = doors[j].properties.property
                for k in range(len(doorprops)):
                    map.doors[j]['t'+doorprops[k].name] = doorprops[k].value
                pass
            pass
        pass

    # Object layers
    for objectlayer in Tiled.objectgroup:
        if objectlayer.name == "roaming" and mode == "server":
            log.info("Processing roaming areas...")
            areas = objectlayer.object
            for i in range(len(areas)):
                if areas[i].properties:
                    nb = areas[i].properties.property.value
                map.roamingAreas[i] = {
                    "id": i,
                    "x": int(areas[i].x / 16),
                    "y": int(areas[i].y / 16),
                    "width": int(areas[i].width / 16),
                    "height": int(areas[i].height / 16),
                    "type": areas[i].type,
                    "nb": nb
                }
        elif objectlayer.name == "chestareas" and mode == "server":
            log.info("Processing chest areas...")
            for area in objectlayer.object:
                chestArea = {
                    "x": int(area.x / map.tilesize),
                    "y": int(area.y / map.tilesize),
                    "w": int(area.width / map.tilesize),
                    "h": int(area.height / map.tilesize),
                }
                for prop in area.properties.property:
                    if prop.name == 'items':
                        chestArea['i'] = list(map(lambda name: Types.getKindFromString(name)), prop.value.split(','))
                    else:
                        chestArea['t'+prop.name] = prop.value
                    pass
                map.chestAreas.append(chestArea)
        elif objectlayer.name == "chests" and mode == "server":
            log.info("Processing static chests...")
            for chest in objectlayer.object:
                items = chest.properties.property.value
                newChest = {
                    "x": int(chest.x / map.tilesize),
                    "y": int(chest.y / map.tilesize),
                    "i": list(map(lambda name: Types.getKindFromString(name), items.split(',')))
                }
                map.staticChests.append(newChest)
        elif objectlayer.name == "music" and mode == "client":
            log.info("Processing music areas...")
            for music in objectlayer.object:
                musicArea = {
                    "x": int(music.x / map.tilesize),
                    "y": int(music.y / map.tilesize),
                    "w": int(music.width / map.tilesize),
                    "h": int(music.height / map.tilesize),
                    "id": music.properties.property.value
                }
                map.musicAreas.append(musicArea)
        elif objectlayer.name == "checkpoints":
            log.info("Processing check points...")
            count = 0
            for checkpoint in objectlayer.object:
                count += 1
                cp = {
                    "id": count,
                    "x": int(checkpoint.x / map.tilesize),
                    "y": int(checkpoint.y / map.tilesize),
                    "w": int(checkpoint.width / map.tilesize),
                    "h": int(checkpoint.height / map.tilesize),
                }
                if mode == "server":
                    cp.s = 1 if checkpoint.type else 0
                map.checkpoints.append(cp)
                pass

    # Layers
    if isinstance(Tiled.layer,  list):
        # for(var i=Tiled.layer.length - 1; i > 0; i -= 1) {
        for i in reversed(range(len(Tiled.layer))):
            processLayer(Tiled.layer[i])
    else:
        processLayer(Tiled.layer)
    
    if mode == "client":
        # Set all undefined tiles to 0
        for i in range(len(map.data)):
            if not isinstance(map.data[i], int):
                map.data[i] = 0
    return map

def processLayer(layer):
    if mode == "server":
        # Mobs
        if layer.name == "entities":
            log.info("Processing positions of static entities ...")
            tiles = layer.data.tile
            for j in range(len(tiles)):
                gid = tiles[j].gid - mobsFirstgid + 1
                if gid and gid > 0:
                    map.staticEntities[j] = staticEntities[gid]
                pass
            pass
        pass
    pass
    
    tiles = layer.data.tile
    if mode == "client" and layer.name == "blocking":
        log.info("Processing blocking tiles...")
        for i in range(len(tiles)):
            gid = tiles[i].gid
            if gid and gid > 0:
                map.blocking.append(i)
                pass
            pass
        pass
    elif mode == "client" and layer.name == "plateau":
        log.info("Processing plateau tiles...")
        for i in range(len(tiles)):
            gid = tiles[i].gid
            if gid and gid > 0:
                map.plateau.append(i)
                pass
            pass
        pass
    elif layer.visible != 0 and layer.name != "entities":
        log.info("Processing layer: "+ layer.name)
        for j in range(len(tiles)):
            gid = tiles[j].gid
            # print(f"j={j}")
            if not gid or gid <= 0:
                continue
            if mode == "client":
                # Set tile gid in the tilesheet
                if not jsarray_get(map.data, j):
                    # map.data[j] = gid
                    jsarray_set(map.data, j, gid)
                elif isinstance(map.data[j], list): 
                    # map.data[j].unshift(gid)
                    map.data[j].insert(0, gid)
                else:
                    map.data[j] = [gid, map.data[j]]
                pass
            # Colliding tiles
            if gid in collidingTiles:
                map.collisions.append(j)
            pass
        pass
    pass
pass

def jsarray_has_index(arr, i) -> bool:
    return i >= 0 and i < len(arr)

def jsarray_get(arr, i):
    return arr[i] if jsarray_has_index(arr, i) else None

def jsarray_set(arr, i, v):
    if jsarray_has_index(arr, i):
        arr[i] = v
    else:
        fill = i - (len(arr) - 1)
        # print(f"i={i} fill={fill} length={len(arr)}")
        arr.extend([None]*fill)
        arr[i] = v
    # from IPython import embed; embed()
    pass
 