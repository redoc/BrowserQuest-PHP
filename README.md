# Zero Game
Forked from [walkor/BrowserQuest-PHP](https://github.com/walkor/BrowserQuest-PHP)

![BrowserQuest with workerman](https://github.com/walkor/BrowserQuest-PHP/blob/master/Web/img/screenshot.jpg?raw=true)


# 开发 - Develop
## 环境初始化 - Initialize environment 
+   git clone https://github.com/redoc/zero
+   composer install 

## 启动/停止 - Start/Stop
* 以debug模式启动 `php start.php start`  
* 以daemon模式启动 `php start.php start -d`
* 查看状态 `php start.php status`
* 停止 `php start.php stop`

# 部署 - Deployment

* 安装依赖 - Install dependencies
  ```
  pip3 install fabric
  apt install docker # or blahblah...
  ```

* 构建并发布镜像 - Build/Release container image
  ```
  make build
  make release
  ```

* 部署之- Deploy it
  ```
  make install # install
  make deploy  # upgrade
  ```
 

## 说明 - Description
本游戏是由[BrowserQuest](https://github.com/mozilla/BrowserQuest)修改而来，主要是将后端nodejs部分用php（[workerman框架](https://github.com/walkor/workerman)）重写。

## 在线演示 - Live Demo
[https://zero.givemecolor.cc/](https://zero.givemecolor.cc/)

## 原Repo - Original Repo
[https://github.com/mozilla/BrowserQuest](https://github.com/mozilla/BrowserQuest)
