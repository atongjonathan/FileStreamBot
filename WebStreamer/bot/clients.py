# This file is a part of FileStreamBot

import asyncio
import logging
from ..vars import Var
from pyrogram import Client
from WebStreamer.utils import TokenParser
from . import multi_clients, work_loads, StreamBot


async def initialize_clients():
    multi_clients[0] = StreamBot
    work_loads[0] = 0
    all_tokens = TokenParser().parse_from_env()
    if not all_tokens:
        print("No additional clients found, using default client")
        return
    
    async def start_client(client_id, token):
        try:
            if len(token) >= 100:
                session_string=token
                bot_token=None
                print(f'Starting Client - {client_id} Using Session String')
            else:
                session_string=None
                bot_token=token
                print(f'Starting Client - {client_id} Using Bot Token')
            if client_id == len(all_tokens):
                await asyncio.sleep(2)
                print("This will take some time, please wait...")
            client = await Client(
                name=str(client_id),
                api_id=Var.API_ID,
                api_hash=Var.API_HASH,
                bot_token=bot_token,
                sleep_threshold=Var.SLEEP_THRESHOLD,
                no_updates=True,
                session_string=session_string,
                in_memory=True,
            ).start()
            work_loads[client_id] = 0
            return client_id, client
        except Exception:
            logging.error(f"Failed starting Client - {client_id} Error:", exc_info=True)
    
    clients = await asyncio.gather(*[start_client(i, token) for i, token in all_tokens.items()])
    multi_clients.update(dict(clients))
    if len(multi_clients) != 1:
        Var.MULTI_CLIENT = True
        print("Multi-Client Mode Enabled")
    else:
        print("No additional clients were initialized, using default client")
