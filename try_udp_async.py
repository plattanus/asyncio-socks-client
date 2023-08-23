import asyncio
import socket

import asyncio_socks_client.udp_async as socks


async def udp_client_through_socks(
    proxy_host, proxy_port, target_host, target_port, message
):
    # 创建一个 SOCKS5 代理连接
    # await socks.setdefaultproxy(socks.SOCKS5, proxy_host, proxy_port, rdns=False, username='my_username', password='my_password')
    await socks.setdefaultproxy(
        socks.SOCKS5,
        proxy_host,
        proxy_port,
        rdns=True,
        username="my_username",
        password="my_password",
    )

    socket.socket = socks.socksocket

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    await udp_socket.settimeout(5)
    await udp_socket.sendto(message.encode(), (target_host, target_port))

    response, server_address = await udp_socket.recvfrom(1024)

    print("Response from server:", response.decode())

    await udp_socket.close()


async def main():
    proxy_host = "10.233.7.205"
    proxy_port = 1080
    target_host = "10.233.7.205"
    target_port = 6000
    message = "Hello, server!"

    await udp_client_through_socks(
        proxy_host, proxy_port, target_host, target_port, message
    )


if __name__ == "__main__":
    asyncio.run(main())
