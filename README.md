# haproxy-shadowsocks-checker
External HAProxy checker for shadowsocks protocol. 

## Usage
```
...
backend backend_services
    mode        tcp
    balance     roundrobin
    option external-check
    external-check command "/your/path/haproxy-shadowsocks-checker.py"

    server your-server-name 127.0.0.1:8001 check fall 5 rise 2 inter 7s
...
```
