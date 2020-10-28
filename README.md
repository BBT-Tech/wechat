# flask_wechat

基于flask的微信公众平台接口

## 文档

[docs](./docs)

## 部署

### 修改配置文件

1. 注意`jsapi_ticket`和`access_token`在 redis 中的键不要和其他重复

2. 因为在获取用户`access_token`接口中需要后端地址来构造跳转url，在nginx中需要修改`Host`头部

    ```nginx
    location /2020/wechat/ {
        proxy_pass http://127.0.0.1:10000/;
        proxy_set_header Host $host/2020/wechat;  # 修改Host头部
    }
    ```

    


### 定时任务

`auto_refresh.py`会定时刷新`jsapi_ticket`和`access_token`，注意要单独部署运行，`supervisor`中的错误日志要和`flask`项目分开



