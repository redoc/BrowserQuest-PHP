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
use \Workerman\WebServer;
use \Workerman\Worker;

require_once __DIR__ . '/vendor/autoload.php';

function setup_web($web_env) {
    $envs = array("dev", "alpha", "prod");
    if (!is_string($web_env)) {
        $web_env = "dev";
    }
    if(!in_array($web_env, $envs)) {
        throw Exception("setup web failed. invalid \$web_env=$web_env");
    }
    $src = __DIR__."/Web/config/config_$web_env.json";
    $dest = __DIR__.'/Web/config/config.json';
    file_put_contents($dest, file_get_contents($src));
}

// 根据环境变量创建 Web/config.json
setup_web($_ENV["webenv"]);

// 这里使用workerman的WebServer运行Web目录。Web目录也可以用nginx/Apache等容器运行
$web = new WebServer("http://0.0.0.0:8787");
$web->count = 2;
$web->name = 'BrowserQuestWeb';
$web->addRoot('www.your_domain.com', __DIR__.'/Web');

// 如果不是在根目录启动，则运行runAll方法
if(!defined('GLOBAL_START'))
{
    Worker::runAll();
}
