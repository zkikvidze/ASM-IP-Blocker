# ASM-IP-Blocker

Simple F5 BIG-IP ASM API Client, which blocks ip address for given policy.

Works on Python 2 and Python 3.

Before use, you need to change **asmaddress** and **auth** variables in the file.

Usage:

```
$ python asm-blocker.py -h

usage: asm-blocker.py [-h] -a ADDRESS -p POLICY

F5 ASM IP Address Blocker

 optional arguments:

  -h, --help            show this help message and exit

  -a ADDRESS, --address ADDRESS

                        IP Address

  -p POLICY, --policy POLICY

                        Policy Full path. Example: /Common/website.ge_policy

```



