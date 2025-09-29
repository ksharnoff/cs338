# Eve

## Diffie Hellman

In order to figure out the shared secret number between Bob and Alice, I had to find Alice's (or Bob's) individual secret number. I decided to solve for both Alice's and Bob's individual secret numbers in order to double check my work. I did this by iterating through all the options until I got one that matched, using the following function:

```
def brute_DH(g, p, A, maximum):
    for i in range(maximum):
        if (g**i % p == A):
            return i

    return -1
```

I set my maximum to 100 initially, which was enough to give me both secrets. This function uses the equation `g**i % p == A` as that is how both Alice and Bob calculate their public shared numbers (where `i` is the individual secret number and `A` is the public number). From this function, I found that Alice's secret number was 45 and Bob's was 67. 

To find the shared secret number using Alice's information, I used the equation `B**x % p`, where `B` is Bob's public number and `x` is Alice's private number. I also calculated this shared secret number using Bob's information: `A**y % p` where `A` is Alice's public number and `y` is Bob's private number. Both equations gave **31** as the shared secret number.

If the individual secret numbers chosen at the beginning were larger, I would have had to chose a larger maximum number. This for loop runs in `O(n)`, but the math computation `g**i % p` does take significantly longer as the `i` integer gets bigger. Therefore, if the individual secret numbers were larger, this would take too long to brute force. 


## RSA

Bob's public key, `(e, n)` is `(17, 266473)`. I need to find his private key `(d, n)` in order to decrypt the ciphertext. In order to get `d`, I need `lambda_n` which is the least common multiple of the product of the original primes subtracted by 1 multiplied together, therefore I need the original primes. I realized that the primes that multiple to produce 266,473 cannot both be over one thousand and therefore could be brute forced. I found a [list](https://di-mgt.com.au/primes1000.html) of the first 170 primes where the 170th is 1,013. I wrote the following function to check all product combinations of primes until the two that multiplied to 266,473.

```
def find_original_primes(n):
    for i in primes:
        for j in primes:
            if (i * j == n):
                return (i, j)

    return(-1)
```

This `find_original_primes` calculated the primes to be `q: 439, p: 607`. This function ran quickly, taking less than 0.001 seconds. If the original `n` was larger, then more primes would have to be checked, which would take longer. This function runs in `O(n^2)` time, where `n` is the number of primes in the prime list. If both primes were greater than the 10,000th primes, then this function would need to do over 100,000,000 computations to brute force the original primes, which would take a while. 

Next, I solved for `lambda_n` by `math.lcm(q-1,p-1)` which gave 44,238. I then had enough information to solve for `d`. The equation for calculating `d` is `e*d % lambda_n = 1` so I created the following function to try all the options: 

```
def find_d(e, lambda_n):
    for i in range(10000000):
        if (e * i % lambda_n) == 1:
            return i

    return -1
```

This function returned that `d` is 10,409. This is another function where if the original primes were larger it would take a long time to brute force, as the `d` would have also been bigger. Next, I decrypted the cipher text using the equation `y**d %n` where `y` is one number in the cipher text. I used the following equation:

```
def decrypt(cipher, d, n):
    plaintext = []
    for num in cipher:
        decrypted = num**d % n
        plaintext.append(decrypted)

    return plaintext
```

This function returned the decrypted bytes: 

> [18533, 31008, 17007, 25132, 8296, 25970, 25895, 29472, 29551, 28005, 8291, 29305, 28788, 28519, 29281, 28776, 31008, 26729, 29556, 28530, 31008, 26223, 29216, 31087, 29984, 10344, 29812, 28787, 14895, 12133, 28206, 30569, 27497, 28773, 25705, 24878, 28530, 26415, 30569, 27497, 12116, 26725, 24397, 24935, 26979, 24407, 28530, 25715, 24417, 29285, 24403, 29045, 25953, 28009, 29544, 24399, 29555, 26982, 29281, 26469, 10542, 8264, 24944, 28793, 8294, 24931, 29807, 29289, 28263, 11296, 16748, 26979, 25902]

I used `chr(decrypted)` for each decrypted encoded byte in the plaintext, which works on ASCII bytes. I got the following: 

> 䡥礠䉯戬⁨敲攧猠獯浥⁣特灴潧牡灨礠桩獴潲礠景爠祯甠⡨瑴灳㨯⽥渮睩歩灥摩愮潲术睩歩⽔桥彍慧楣彗潲摳彡牥当煵敡浩獨彏獳楦牡来⤮⁈慰灹⁦慣瑯物湧Ⱐ䅬楣攮% 

I realized that this was not the decoded plaintext because it is unlikely that the decoded plaintext is a mix of Chinese and other random (like `⤮⁈`) characters. Looking at the decrypted byte numbers, I realized that they are greater than the Latin alphabet ASCII characters. They are also not concatenated in pairs or threes as those are also not valid Latin alphabet ASCII characters.

I then tried to decode it using utf-16 as I was trying whatever I could think of, and when searching about the syntax to change ints to bytes, I found the idea of a number storing more than a single byte. I wrote in more details about this searching and discovery process in `LLM.md`.

I then used the function `decrypted.to_bytes(2)` and ASCII conversion to decode the bytes, seen in the following function:

```
def decode(input):
    plaintext = ""
    for i in input:
        x = i.to_bytes(2)
        x = x.decode("ascii")
        plaintext += (x)

    return plaintext
```

This function outputted the text:

> Hey Bob, here's some cryptography history for you (https://en.wikipedia.org/wiki/The_Magic_Words_are_Squeamish_Ossifrage). Happy factoring, Alice.

The encoding ended up being two bytes, each representing a character, in each number. This is not a secure encoding because it is recognizable and easily reversible. On Python's information on the [int.to_bytes function](https://docs.python.org/3/library/stdtypes.html#int.to_bytes), ints can be made with any chosen number of bytes. How many bytes were used can be seen by looking at how many digits are in the numbers.

