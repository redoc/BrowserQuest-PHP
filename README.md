# Zero Game
Forked from [walkor/BrowserQuest-PHP](https://github.com/walkor/BrowserQuest-PHP)

![BrowserQuest with workerman](https://github.com/walkor/BrowserQuest-PHP/blob/master/Web/img/screenshot.jpg?raw=true)


## 安装 － Install
+   git clone https://github.com/redoc/zero
+   composer install 

## 启动停止 - Start and Stop
* 以debug模式启动 `php start.php start`  
* 以daemon模式启动 `php start.php start -d`
* 查看状态 `php start.php status`
* 停止 `php start.php stop`

## 使用 docker
* 构建本地镜像
  ```
  make build
  ```

* 发布镜像到 docker hub
  ```
  make release
  ```

* 部署/重部署服务
  ```
  make deploy
  make deploy-renew
  ```
 
 

## 说明 - Description
本游戏是由[BrowserQuest](https://github.com/mozilla/BrowserQuest)修改而来，主要是将后端nodejs部分用php（[workerman框架](https://github.com/walkor/workerman)）重写。

## 在线演示 - Live Demo
[http://zero.adzuki.studio/](http://zero.adzuki.studio/)

## 原Repo - Original Repo
[https://github.com/mozilla/BrowserQuest](https://github.com/mozilla/BrowserQuest)
