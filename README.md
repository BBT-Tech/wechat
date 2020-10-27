# flask_wechat

基于flask的微信公众平台接口

## 文档

[docs](./docs)

## 部署

### 修改配置文件

1. 注意`jsapi_ticket`和`access_token`在 redis 中的键不要和其他重复

2. 因为使用了nginx反向代理，无法获取请求地址，需要在`BaseConfig`中配置`base_url`，值为后端部署后的地址，最后没有反斜杠

### 定时任务

`auto_refresh.py`会定时刷新`jsapi_ticket`和`access_token`，注意要单独部署运行，`supervisor`中的错误日志要和`flask`项目分开



