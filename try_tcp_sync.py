import re

import asyncio_socks_client.tcp_sync as socks


def tcp_client_through_socks(proxy_host, proxy_port, target_host, target_port):
    tcp_socks = socks.socksocket()  # Same API as socket.socket in the standard lib

    tcp_socks.setproxy(
        socks.SOCKS5,
        proxy_host,
        proxy_port,
        rdns=False,
        username="my_username",
        password="my_password",
    )  # SOCKS4 and SOCKS5 use port 1080 by default
    # tcp_socks.set_proxy(socks.SOCKS5, proxy_host, proxy_port, rdns=True, username='my_username', password='my_password') # SOCKS4 and SOCKS5 use port 1080 by default

    # tcp_socks.set_proxy(socks.SOCKS4, proxy_host, proxy_port, rdns=False)
    # tcp_socks.set_proxy(socks.SOCKS4, proxy_host, proxy_port, rdns=True)
    tcp_socks.settimeout(5)

    tcp_socks.connect_ex((target_host, target_port))
    request = b"GET / HTTP/1.1\r\nHost: ip.sb\r\nUser-Agent: curl/7.64.0\r\n\r\n"

    tcp_socks.send(request)
    response_headers = tcp_socks.recv(4096).decode()
    ip_address = re.search(
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", response_headers
    ).group()
    tcp_socks.close()
    print(ip_address)


if __name__ == "__main__":
    proxy_host = "10.233.7.205"
    proxy_port = 1080
    target_host = "ip.sb"
    target_port = 80

    tcp_client_through_socks(proxy_host, proxy_port, target_host, target_port)
