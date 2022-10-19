import re
import httpx
import asyncio

max_conn = 5
blacklisted = []
found_address = []

async def juge_spam(match, list):
    count = 0

    for item in list:
        if match == item:
            count += 1

    if count >= max_conn:
        blacklisted.append(match)
        return True
    else:
        return False

async def is_blacklisted(match):
    for item in blacklisted:
        if match == item:
            return True

    return False

async def blacklist(host, text):
    for addr in re.findall(r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', text):
        if addr != host or not await is_blacklisted(addr):
            if await juge_spam(addr, found_address):
                print(f"> Blacklist address --> {addr}")
                return

            found_address.append(addr)

async def resolve_host():
    async with httpx.AsyncClient() as client:
        res = await client.get("https://api.ipify.org")
        return res.text

async def main():
    print("|*> UFW-Firewall (PY) - github.com/pneb (originated by Its-Vichy)")
    host = await resolve_host()

    while True:
        text = input()
        await blacklist(host, text)
        await asyncio.sleep(1)

asyncio.run(main())
