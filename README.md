# haproxy-shadowsocks-checker
External HAProxy checker for shadowsocks protocol. 

## How works
[使用 HAProxy 为 Shadowsocks 做负载平衡](https://blog.sbw.so/u/haproxy-shadowsocks-load-balance-useibility.html)

## Usage
Edit `/etc/haproxy/haproxy.cfg`, add external-check options.
```
global
    external-check
    insecure-fork-wanted
...
backend backend_services
    mode        tcp
    balance     roundrobin
    option external-check
    external-check command "/your/path/haproxy-shadowsocks-checker.py"

    server your-server-name 127.0.0.1:8001 check fall 5 rise 2 inter 7s
...
```

Note: 
- From HAProxy v1.8.19, need to comment out `chroot /var/lib/haproxy` option. [#2](https://github.com/sbwtw/haproxy-shadowsocks-checker/issues/2)
- From HAProxy v2.2, need to add `insecure-fork-wanted` option in `global` section. 

## Change Test Domain
The checker is trying to connect `www.google.com` in default, but you can modify the global variable to other domain if you want.
```python
TEST_DOMAIN = b'www.facebook.com'
```

## Screenshots
![Screenshots](screenshots/Screenshot_2020-02-01-Statistics-Report-for-HAProxy.png)

## Sponsor
BTC: 3EDpMyGkp2FAQbAe7F3PhzRsxA44Kqek51
