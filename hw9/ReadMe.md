## 參考自柯志亨老師課程教學

## 筆記
## 安裝 Docker
- [docker](https://docs.docker.com/engine/install/ubuntu/)
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

```
$ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

docker 工具
```
$ sudo curl -L "https://github.com/docker/compose/releases/download/v2.17.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose && sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

git clone - [dialoqbase](https://github.com/n4ze3m/dialoqbase)

```
$ cd dialoqbase/
$ cd docker/
$ vim .env
```
把 openai api 放入

```
docker-compose up -d
```

進入網頁要輸入 ip by ifconfig(192.168...)
帳密 

## telegram bot
```
/newbot
以_bot結尾的名字
/token
```

2024/5/22 順利執行

## 執行結果
我使用 linode 部屬專案
![image](https://github.com/patrick0516/ai_report/assets/109636871/112a33de-8fe2-4911-8753-c31be489d1ca)
![image](https://github.com/patrick0516/ai_report/assets/109636871/41c7a110-8b5f-481f-943c-33a57cac2b22)

