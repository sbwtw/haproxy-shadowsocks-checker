#!/usr/bin/python3

import socket
import ipaddress
import ssl
import sys

# do socks5 handshake to shadowsocks-client.
def handshake_socks5(host, port):
    sock = socket.create_connection((host, port));
    sock.settimeout(3.0);
    sock.send(b'\x05'); # version
    sock.send(b'\x01'); # length of auth list
    sock.send(b'\x00'); # no auth
    # check auth method response
    buf = sock.recv(2);
    if buf != b'\x05\x00':
        print('err: auth error.', buf)
        sock.close();
        return None;

    sock.send(b'\x05\x01\x00\x03\x0e'); # connect to domain
    sock.sendall(b'www.google.com');
    sock.send(b'\x01\xbb'); # port 443 in big endian
    # check proxy response
    buf = sock.recv(3);
    if buf != b'\x05\x00\x00':
        print('err: connect error.', buf);
        sock.close();
        return None;

    atyp = sock.recv(1);
    ip = None;
    # 0x04 means 16bytes IPv6 address
    if atyp == b'\x04':
        buf = sock.recv(16);
        ip = ipaddress.IPv6Address(buf);
    # 0x01 means 4bytes IPv4 address
    elif atyp == b'\x01':
        buf = sock.recv(4);
        ip = ipaddress.IPv4Address(buf);
    # 0x03 means domain, not valid here!
    else:
        print('err: atyp error', atyp);
        sock.close();
        return None;

    port = int.from_bytes(sock.recv(2), 'big');

    #print('done', ip, port);
    return sock;

def test_shadowsocks(host, port):
    socks5 = handshake_socks5(host, port);
    if socks5 == None:
        print('socks5 handshake error', host, port);
        return False;

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT);
    ctx.options |= ssl.HAS_TLSv1_3 | ssl.HAS_TLSv1_2;
    ctx.verify_mode = ssl.CERT_REQUIRED;
    ctx.check_hostname = True;
    ctx.load_default_certs();

    ssock = ctx.wrap_socket(socks5, server_hostname='www.google.com', do_handshake_on_connect=True);

    # if handshake success, return ok.
    ssock.close();
    return True;

    #ssock.sendall(b'GET / HTTP/1.0\r\nHost: www.google.com\r\nConnection: close\r\n\r\n');

    #buf = ssock.recv(20);
    #ssock.close();

    #if "200 OK" in str(buf):
    #    #print('available!');
    #    return True;
    #return False;

if __name__ == "__main__":
    host = sys.argv[3];
    port = sys.argv[4];

    try:
        if test_shadowsocks(host, port):
            exit(0);
    except Exception as e:
        pass

    exit(-1);

