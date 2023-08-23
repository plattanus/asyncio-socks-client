import asyncio
import re

import socks_client.tcp_async as socks


async def main():
    tcp_socks = socks.socksocket(
        proxy_type=socks.SOCKS5,
        proxy_host="10.233.7.205",
        proxy_port=1080,
        username="my_username",
        password="my_password",
        rdns=False,
    )
    await tcp_socks.settimeout(5)
    sock = await tcp_socks.connect(dest_host="ip.sb", dest_port=80)

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


asyncio.run(main())
