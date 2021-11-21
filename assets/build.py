import cbox


@cbox.cmd
def gamedata(output):
    """
    导出数值
    """
    from gamedata import build
    build.main(output)
    pass


@cbox.cmd
def map():
    """
    导出地图
    """
    pass



if __name__ == "__main__":
    cbox.main([
        gamedata,
        map,
    ])

