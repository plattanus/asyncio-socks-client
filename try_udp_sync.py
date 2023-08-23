import socket

import socks_client.udp_sync as socks


def udp_client_through_socks(proxy_host, proxy_port, target_host, target_port, message):
    socks.setdefaultproxy(
        socks.SOCKS5,
        proxy_host,
        proxy_port,
        rdns=False,
        username="my_username",
        password="my_password",
    )
    socket.socket = socks.socksocket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(5)
    udp_socket.sendto(message.encode(), (target_host, target_port))
    response, server_address = udp_socket.recvfrom(1024)
    print("Response from server:", response.decode())
    udp_socket.close()


if __name__ == "__main__":
    proxy_host = ""
    proxy_port = 1080
    target_host = ""
    target_port = 6000
    message = "A"

    udp_client_through_socks(proxy_host, proxy_port, target_host, target_port, message)
