# GetGras Bot With Multiple Proxy

Get Gras bot with multiple proxy which auto filter dead proxy from file, and auto save powerfull proxy.


## installation
install python3
https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe (windows)

for unix ```sudo apt-get install python3``` or ```sudo yum install python3``` or ```sudo dnf install python3```
## module install 
install fakeuseragent
```pip install fake_useragent```

install loguru
```pip install loguru```

install websockets_proxy
```pip install websockets_proxy```

## register: https://app.getgrass.io/register/?referralCode=PnmuSjrqxyxvZsk ( use this link instead! )

## how to use

#### getting your user id

login to https://app.getgrass.io

press f12 go to console, then type ```allow pasting```

![0001](https://github.com/im-hanzou/getgrass_bot/blob/main/pasting.JPG)

then insert this code
```localStorage.getItem('userId')```

![0001](https://github.com/im-hanzou/getgrass_bot/blob/main/userid.JPG)

#### usage command
where to get proxy list ?
open [this](https://github.com/monosans/proxy-list/blob/main/proxies_anonymous/socks5.txt)
copy proxy from that site to proxy_list.txt you can use ```nano```
```nano proxy_list.txt```
that site is update every 30 minutes, so you can add many proxy to your proxylist based on that site scrap
now let start the running process
run ```python main.py```.


#### NOTE
insert your accounts user ids to ```user_id.txt``` and insert your proxies to ```proxy_list.txt```.
remember to only use socks5 proxy, proxy list format is like
```bash
IP:PORT
IP:PORT
IP:PORT
```
without scheme ```socks5://```

