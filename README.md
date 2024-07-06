# Tg-Request-Bot

Tg-Request-Bot 是一个用于配合 webhook 发送请求的 tg 机器人。

配置文件为 `./data/config.yaml`，内容如下：

```yaml
services:
  - name: "百度"
    url: "https://www.baidu.com/"
    method: "GET"
  # 会异常
  - name: "百度带参数"
    url: "https://www.baidu.com/"
    method: "GET"
    param: "wd"
    tips: "请输入查询内容"
```
- `name`：功能名称，用于tgbot菜单显示
- `url`：点击菜单请求的地址
- `method`：请求 url 的方法，可以是 GET 或者 POST。
- `param`：请求携带的参数名称。可选，不填则点击菜单直接发送请求。
- `tips`：点击菜单时，发送给用户的提示语。可选，不填默认提示输入 param 的值。

# docker 部署

```sh
docker run -d --name tg-request-bot -e API_TOKEN=xxx -e ROW_WIDTH=4 -v /home/docker/tg-request-bot/config.yaml:/app/data/config.yaml hausen1012/tg-request-bot
```
