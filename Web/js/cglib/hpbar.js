/**
 * Created by CG on 2016/12/31.
 */
define(['../mobs'], function (Mobs) {
   var hpbar = function () {
       var isMob = function (x, y) {
           return true;
       };
       return {
           isMob:function (x, y) {
               return true;
           }
       }
   };
   return hpbar;
});