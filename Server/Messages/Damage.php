<?php 
/**
 * This file is part of workerman.
 *
 * Licensed under The MIT License
 * For full copyright and license information, please see the MIT-LICENSE.txt
 * Redistributions of files must retain the above copyright notice.
 *
 * @author walkor<walkor@workerman.net>
 * @copyright walkor<walkor@workerman.net>
 * @link http://www.workerman.net/
 * @license http://www.opensource.org/licenses/mit-license.php MIT License
 */
namespace Server\Messages;
use Server\Properties;

class Damage
{
    public $entity = 0;
    public $points = 0;
    public function __construct($entity, $points)
    {
        $this->entity = $entity;
        $this->points = $points;
    }
    
    public function serialize()
    {
        return array(TYPES_MESSAGES_DAMAGE, 
                $this->entity->id,
                $this->points,
                Properties::getHitPoints($this->entity->kind),  // 怪物总血量
                $this->entity->hitPoints,                       // 怪物当前血量
        );
    }
}

