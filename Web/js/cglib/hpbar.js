/**
 * Created by CG on 2016/12/31.
 */
define(['../../shared/js/gametypes'], function (GameTypes) {
    var HPBar = {
        isMob: function (kind) {
            return GameTypes.isMob(kind);
        },
        getMobName: function (kind) {
            var en = GameTypes.getKindAsString(kind);
            var en2cn = {
                'rat': '小老鼠',
                'skeleton': '骷髅战士',
                'goblin': '哥布林',
                'ogre': '食人魔',
                'spectre': '幽灵',
                'deathknight': '亡灵骑士',
                'crab': '大螃蟹',
                'snake': '小青蛇',
                'bat': '灰蝙蝠',
                'wizard': '邪恶巫师',
                'eye': '地狱之眼',
                'skeleton2': '强化骷髅战士',
                'boss': '骷髅王'
            };
            return en2cn[en] || '无名小怪';
        },
        drawMobName: function (render, kind, x, y, color) {
            var name = HPBar.getMobName(kind);
            color = color || "white";
            render.context.save();
            render.drawText(name, x, y, true, color, 'rgba(0,0,0,0)');
            render.context.restore();
        },
        drawMobHp: function (render, hpmax, hpnow, x, y, color) {
            color = color || "white";
            render.context.save();
            render.drawText(hpnow + ' / ' + hpmax, x, y, true, color, 'rgba(0,0,0,0)');
            render.context.restore();
        }
    };

    return HPBar;
});