import asyncio
import re

import socks_client.tcp_async as socks


async def tcp_client_through_socks(proxy_host, proxy_port, target_host, target_port):
    tcp_socks = socks.socksocket(
        proxy_type=socks.SOCKS5,
        proxy_host=proxy_host,
        proxy_port=proxy_port,
        username="my_username",
        password="my_password",
        rdns=False,
    )
    await tcp_socks.settimeout(5)
    sock = await tcp_socks.connect(dest_host=target_host, dest_port=target_port)

    reader, writer = await asyncio.open_connection(
        host=None,
        port=None,
        sock=sock,
    )
    request = (
        b"GET / HTTP/1.1\r\n" b"Host: ip.sb\r\n" b"User-Agent: curl/7.64.0\r\n\r\n"
    )
    writer.write(request)

    response = await asyncio.wait_for(reader.read(1024), timeout=1)

    response_headers = response.decode("utf-8")
    ip_address = re.search(
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", response_headers
    ).group()
    print(ip_address)


async def main():
    proxy_host = ""
    proxy_port = 1080
    target_host = "ip.sb"
    target_port = 80

    await tcp_client_through_socks(proxy_host, proxy_port, target_host, target_port)


if __name__ == "__main__":
    asyncio.run(main())
