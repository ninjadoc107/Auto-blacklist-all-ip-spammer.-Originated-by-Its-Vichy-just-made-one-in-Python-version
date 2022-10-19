import re
import httpx
import asyncio

class UFW:
    def __init__(self):
        self.max_conn = 5
        self.blacklisted = []
        self.found_address = []

    async def juge_spam(self, match, list):
        count = 0

        for item in list:
            if match == item:
                count += 1

        if count >= self.max_conn:
            self.blacklisted.append(match)
            return True
        else:
            return False

    async def is_blacklisted(self, match):
        for item in self.blacklisted:
            if match == item:
                return True

        return False

    async def blacklist(self, host, text):
        for addr in re.findall(r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', text):
            if addr != host or not await self.is_blacklisted(addr):
                if await self.juge_spam(addr, self.found_address):
                    print(f"> Blacklist address --> {addr}")
                    return

                self.found_address.append(addr)

    async def resolve_host(self):
        async with httpx.AsyncClient() as client:
            res = await client.get("https://api.ipify.org")
            return res.text

    async def main(self):
        print("|*> UFW-Firewall (PY) - github.com/pneb (originated by Its-Vichy)")
        host = await self.resolve_host()

        while True:
            text = input()
            await self.blacklist(host, text)
            await asyncio.sleep(1)

asyncio.run(UFW().main())
