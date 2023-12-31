import asyncio
import socket

import socks_client.udp_async as socks


async def udp_client_through_socks(
    proxy_host, proxy_port, target_host, target_port, message
):
    await socks.setdefaultproxy(
        socks.SOCKS5,
        proxy_host,
        proxy_port,
        rdns=False,
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
    proxy_host = "127.0.0.1"
    proxy_port = 1080
    target_host = "127.0.0.1"
    target_port = 8888
    message = "A"

    await udp_client_through_socks(
        proxy_host, proxy_port, target_host, target_port, message
    )


if __name__ == "__main__":
    asyncio.run(main())
