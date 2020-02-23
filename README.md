# haproxy-shadowsocks-checker
External HAProxy checker for shadowsocks protocol. 

## How works
[使用 HAProxy 为 Shadowsocks 做负载平衡](https://blog.sbw.so/u/haproxy-shadowsocks-load-balance-useibility.html)

## Usage
Edit `/etc/haproxy/haproxy.cfg`, add external-check options.
```
global
    external-check
...
backend backend_services
    mode        tcp
    balance     roundrobin
    option external-check
    external-check command "/your/path/haproxy-shadowsocks-checker.py"

    server your-server-name 127.0.0.1:8001 check fall 5 rise 2 inter 7s
...
```

## Screenshots
![Screenshots](screenshots/Screenshot_2020-02-01-Statistics-Report-for-HAProxy.png)
