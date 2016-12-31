/**
 * Created by CG on 2016/12/31.
 */
define(['../../shared/js/gametypes'], function (GameTypes) {
   var hpbar = (function (t) {
       var isMob = function (k) {
           return t.isMob(k);
       };
       var getMobName = function (k) {
           var en = t.getKindAsString(k);
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
               'boss': 'boss'
           };
            return en2cn[en];
       };
       var drawMobName = function(n, r, x, y, color){
           r.context.save();
           var color = color | "white";
           r.drawText(n,
               x,
               y,
               true,
               color);
           r.context.restore();
       };

       var drawHp = function (m, h, r, x, y, color) {
           r.context.save();
           
           var color = color | "white";
           r.drawText('('+h+'/'+m+')',
               x,
               y,
               true,
               color);
           r.context.restore();
       };

       return {
           isMob:function (kind) {
               return isMob(kind);
           },
           getMobName:function (kind) {
               return getMobName(kind);
           },
           drawMobName:function (name, renderer, x, y, color) {
               drawMobName(name, renderer, x, y, color);
           },
           drawHp: function (maxhp, hp, renderer, x, y, color) {
                drawHp(maxhp, hp, renderer, x, y, color);
           }
   }
   })(GameTypes);
   return hpbar;
});