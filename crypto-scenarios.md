- Kezia Sharnoff
- October 5, 2025

CS338 Computer Security

crypto-scenarios.md


## Problem 1:
Alice wants to send Bob a long message, `M`, and she doesn't want Eve to be able to read it. Assume for this scenario that AITM is impossible.


#### Solution:
Alice and Bob use Diffie-Hellman to get a shared secret number to make an AES key `K`. Alice sends Bob the ciphertext `C = AES(K, M)`. Bob decrypts this ciphertext using `M = AES_D(K, C)`. 


#### Explanation:
In order to avoid eavesdroppers, messages must be encrypted. Long messages should be encrypted using symmetric encryption as it is faster. Since an adversary in the middle attack is impossible, Alice and Bob can use just a Diffie-Hellman key exchange, without the question of if their messages are being read and modified because they are talking through Mal. After the Diffie-Hellman key exchange, they can use the same key with symmetric encryption and an eavesdropper cannot guess it as they have neither secret number. 



## Problem 2:
Alice wants to send Bob a long message, `M`. She doesn't want Mal to be able to modify the message without Bob detecting the change.


#### Solution:
Alice and Bob use Diffie-Hellman to get a shared secret number to make an AES key `K`. Alice computes the hash of message and concatenates with the key: `D = H(M) || K`. She encrypts `D` using Bob's public key: `Sig = E(P_A, D)`. She concatenates `T = M || Sig`. She encrypts this total message using the shared key, `C = AES(K, T)`. Bob decrypts, `T = AES_D(K, C)`. He then splits it into the `M` and the `Sig`. He decrypts the `Sig` using his private key to get `H(M)` and `K`. He checks if the `K` he received is the same one he has been using in previous communication and that the `H(M)` value still corresponds to the message. 


#### Explanation:
If there was an adversary in the middle, where Mal has been in communications with both Alice and Bob, pretending to be the other person, then there would exist two different keys, `K_A` and `K_B`. `K_A` is the key shared between Alice and Mal while `K_B` is shared between Mal and Bob. These two keys would be discovered by Bob decrypting `Sig` as the `K` part of the signature would not equal the `K` that Bob has seen. The `Sig` part of the message could not be replaced by Mal because they cannot decrypt the `Sig` without Bob's private key. If the `Sig` did not include the key `K`, then they could duplicate it also using Bob's public key. If it was encrypted using Alice's private key, Mal could also decrypt it using Alice's public key. 


## Problem 3:
Alice wants to send Bob a long message, `M` (in this case, it's a signed contract between AliceCom and BobCom), she doesn't want Eve to be able to read it, and she wants Bob to have confidence that it was Alice who sent the message. Assume for this scenario that AITM is impossible.


#### Solution:
Alice and Bob use Diffie-Hellman to get a shared secret number to make an AES key `K`. Alice creates a hash of the message, `D = H(M)`. She encrypts this with her private key, `Sig = E(S_A, D)`. She concats to get the text `T = M || Sig`. She sends an encrypted version of `T`, `C = AES(K, T)`. Bob decrypts `C` by `AES_D(K, C)`. He splits `C` into the message `M` and `Sig`. Using Alice's public key, he decrypts `Sig`: `E(P_A, Sig)` which gives him `D`. Bob computes the hash of the message, `H(M)` and if `H(M)` equals `D`, then he knows the message came from Alice. 


#### Explanation:
Since an adversary in the middle attack is impossible, Alice and Bob can use just a Diffie-Hellman key exchange, without the question of if their messages are being read and modified because they are talking through Mal. One way to prove that the message came from Alice would be to encrypt it using Alice's private key (`S_A`), however, this would be slow as it is a long message. Instead, Alice computes the hash of the message and encrypts it with her private key. Only Alice could have her private key, so she must have created the hash. Alice could have only created the hash if she had the message, so Bob can conclude that the message came from Alice. 

## Problem 4: 
1. CLAIM: The contract `C` and signature `Sig` were created by Alice but were sent to Bob (or an accomplice of Bob) for an earlier contract. 


Depending on the contents of `C`, this could be plausible to the judge. If `C` is literally only Alice's signature, this could be true. If `C` also includes date or contract information, this would be less likely. 

2. CLAIM: The signature `Sig` was created by Alice for a different message, `M`. The false contract `C` has the same hash as `M`, so `H(M)` equals `H(C)`. 

This is possible but not very plausible. Cryptographic hash functions are designed to avoid collisions and to be hard (mathematically impossible) to get a message starting from a hash. That the message `C` is a valid pdf (strict requirements on what bits are used) makes this even less plausible. 

3. CLAIM: Bob has a (secret) prime factoring algorithm and by using Alice's public key, he was able to find her private key. He then created both `C` and the signature `Sig` using Alice's private key.

This is not plausible, no prime factoring algorithm has been found in the almost 50 years of using RSA to make public-private keys. Also, if Bob had a secret prime factoring algorithm and a desire for evil actions, there are likely more impactful keys he could forge: governments, banks, certificate authorities, etc..


## Problem 5: 
Where `Cert_B = "bob.com" || P_B || Sig_CA`. 

`Sig_CA` is created similarly to the `Sig` in problem 3. Where `data` is `"bob.com" || P_B`. 

`Sig_CA = E(S_CA, H(data))`


## Problem 6: 
It is not enough for Alice to believe that she is talking to the real Bob because anyone (Alice included) can get a copy of `Cert_B`. Alice could send Bob a challenge, a random number encrypted using `P_B` and if Bob can send the random number back, then Bob must have access to `S_B`, the secret key corresponding to the `P_B` of the certificate. 


## Problem 7: 
1. If Mal steals the certificate authority's secret key (`S_CA`), then they could create another certificate using their key that is `Cert_M = "bob.com" || P_M || Sig_CA`. Alice would receive `Cert_M` and think that `P_M` belongs to `"bob.com"`. If Alice sent a challenge encrypted with `P_M` and Mal decrypted it using their private key, Alice would think Mal is Bob of `"bob.com" `. 

2. Imagine that Mal owns the domain `"bob.corn"` and has a valid certificate, `Cert_M` for it. If Mal attacks `"bob.com"` to redirect to `"bob.corn"` (the `"rn"` looks similar to `"m"`), then Alice's computer will check if the certificate matches the domain (it does) and continue. Alice will be confident that she is speaking to Bob given that the certificate matched. 


