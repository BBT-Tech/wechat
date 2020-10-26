# flask_wechat

基于flask的微信公众平台接口

## 配置文件

修改配置文件`app/config/config.sample.py`并重命名为`config.py`

## Installation

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple
pip install gunicorn gevent -i https://mirrors.cloud.tencent.com/pypi/simple
```

## Deploy

### Run

```bash
chmod +x run.sh
./run.sh
```

### Running with docker

```bash
# build the image
docker build -t flask_wechat .
# run the container on the host network
docker run -d --name flask_wechat --network="host" flask_wechat
```

