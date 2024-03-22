# script for 1 user_id and a whole bunch of proxies

import asyncio
import random
import ssl
import json
import time
import uuid
from loguru import logger
from websockets_proxy import Proxy, proxy_connect
from fake_useragent import UserAgent

user_agent = UserAgent()
random_user_agent = user_agent.random


async def connect_to_wss(socks5_proxy, user_id):
    device_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, socks5_proxy))
    logger.info(device_id)
    while True:
        try:
            await asyncio.sleep(random.randint(1, 10) / 10)
            custom_headers = {"User-Agent": random_user_agent}
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            uri = "wss://proxy.wynd.network:4650/"
            server_hostname = "proxy.wynd.network"
            proxy = Proxy.from_url(socks5_proxy)
            async with proxy_connect(
                uri,
                proxy=proxy,
                ssl=ssl_context,
                server_hostname=server_hostname,
                extra_headers=custom_headers,
            ) as websocket:

                async def send_ping():
                    while True:
                        send_message = json.dumps(
                            {
                                "id": str(uuid.uuid4()),
                                "version": "1.0.0",
                                "action": "PING",
                                "data": {},
                            }
                        )
                        logger.debug(send_message)
                        await websocket.send(send_message)
                        await asyncio.sleep(20)

                # asyncio.create_task(send_http_request_every_10_seconds(socks5_proxy, device_id))
                await asyncio.sleep(1)
                asyncio.create_task(send_ping())

                while True:
                    response = await websocket.recv()
                    message = json.loads(response)
                    logger.info(message)
                    if message.get("action") == "AUTH":
                        auth_response = {
                            "id": message["id"],
                            "origin_action": "AUTH",
                            "result": {
                                "browser_id": device_id,
                                "user_id": user_id,
                                "user_agent": custom_headers["User-Agent"],
                                "timestamp": int(time.time()),
                                "device_type": "extension",
                                "version": "3.3.2",
                            },
                        }
                        logger.debug(auth_response)
                        await websocket.send(json.dumps(auth_response))

                    elif message.get("action") == "PONG":
                        pong_response = {"id": message["id"], "origin_action": "PONG"}
                        logger.debug(pong_response)
                        await websocket.send(json.dumps(pong_response))
        except Exception as e:
            logger.error(e)
            if "Empty connect reply" in str(e):
                await remove_proxy_from_file("proxy_list.txt", socks5_proxy[len("socks5://"):])
            # logger.error(socks5_proxy)
            # raise


async def remove_proxy_from_file(file_path, proxy):
    logger.info(f"Removing {proxy} from {file_path}")
    if proxy.startswith("socks5://"):
        proxy = proxy[len("socks5://"):]  # Remove "socks5://" prefix

    try:
        with open(file_path, "r") as file:
            proxies = file.readlines()
        
        with open(file_path, "w") as file:
            for p in proxies:
                if p.strip() != proxy:
                    file.write(p)
        
        logger.info(f"{proxy} removed from {file_path}")
    except Exception as e:
        logger.error(f"Error removing {proxy} from {file_path}: {e}")
        
socks5_proxy_list = []
async def main():
    with open("user_id.txt", "r") as file:
        _user_id = file.read().strip()
    # put the proxy in a file in the format socks5://username:password@ip:port or socks5://ip:port
    with open("proxy_list.txt", "r") as file:
        socks5_proxy_list = file.read().splitlines()
    # auto add socks5://
    for i, proxy in enumerate(socks5_proxy_list):
        if not proxy.startswith("socks5://"):
            socks5_proxy_list[i] = 'socks5://' + socks5_proxy_list[i]

    tasks = []
    for i, proxy in enumerate(socks5_proxy_list):
        try:
            task = asyncio.ensure_future(connect_to_wss(proxy, _user_id))
            tasks.append(task)
        except Exception as e:
            del socks5_proxy_list[i]

    await asyncio.gather(*tasks)



if __name__ == "__main__":
    # поехали нафик
    asyncio.run(main())
