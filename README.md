# RDP-Brute
FreeRDP - as main component

# Installation
### For Linux:
- Install xFreeRDP: ```sudo apt-get update -y && sudo apt-get install freerdp-x11 -y```

### For Wndows:
- Paste to script dir wFreeRDP.exe
  - [Windows x64](https://ci.freerdp.com/job/freerdp-nightly-windows/lastStableBuild/arch=win64,label=vs2013/artifact/build/Release/wfreerdp.exe)
  - [Windows x32](https://ci.freerdp.com/job/freerdp-nightly-windows/lastStableBuild/arch=win32,label=vs2013/artifact/build/Release/wfreerdp.exe)
  
# Usage
- ```data/ip.txt``` - contains IP list
- ```data/passwords.txt``` - contains passwords list
- ```data/users.txt``` - contains users list

- ```rez/good.txt``` - pwned accounts

- ```./start.py``` - main script

# Other
**1**. Default RDP port is ```3389```

**2**. Don\`t set more from 200 threads

**3**. Use only for education. Remember that for all your actions are responsible - you.
