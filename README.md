# cryptobench
A project for benchmarking LWC algorithms.

NOTE: All the sub-directories contain the implementation files of crypto algorithms. The implementations are taken from the internet.

## Instructions
```shell
# Setup cyclops on RPI.
$ ./run.sh

# Import the correct modules in benchmark.py on both the sender and the receiver side.
# On the receiver device execute:
$ python3 benchmark.py

# After running the script on receiver device, run the same script on the sender device.
# RECEIVER is the IP of receiver device.
# PLAINTEXT is the size of the random plaintext to generate.
$ RECEIVER='192.168.1.12' PLAINTEXT=1000 python3 benchmark.py
```

## To-Do
- [x] Print only has encryption function, no decryption.
- [x] Abstract out benchmarking functionality from each algorithm
- [ ] Camellia code is not in Python.
- [ ] Klein only has encryption function, no decryption.
- [ ] Rectangle code is not in Python.

## Dependencies
- `pip install hwcounter`

## Notes
- Compares 41 existing symmetric key lightweight cryptography (plain encryption) algorithms over 7 performance metrics (Block/Key size, Memory, Gate Area, Latency, Throughput, Power & Energy requirements along with hardware and soft- ware efficiency) as recommended by the NIST report for resource-constrained IoT devices.

## References
- <https://singleboardbytes.com/289/connect-wi-fi-enable-ssh-without-monitor-raspberry-pi.htm>
- [Midori: A Block Cipher for Low Energy](https://eprint.iacr.org/2015/1142.pdf)

### SIMON and SPECK
- [The SIMON and SPECK Families of Lightweight Block Ciphers](https://eprint.iacr.org/2013/404)
- <https://github.com/bozhu/NSA-ciphers/>

### Algorithm Implementation Source
- ascon: <https://github.com/meichlseder/pyascon/>
- midori: <https://github.com/Daksh-Axel/Midori128-64/tree/main/App>
- simon: <https://github.com/inmcm/Simon_Speck_Ciphers/tree/master/Python/simonspeckciphers>
- speck: <https://github.com/inmcm/Simon_Speck_Ciphers/tree/master/Python/simonspeckciphers>
