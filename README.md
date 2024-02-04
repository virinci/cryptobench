# cryptobench

## Instructions
```shell
# Setup cyclops on RPI.
$ ./run.sh

# Run any of the benchmark_*.py on the receiver device.
$ python3 benchmark_speck.py

# After running the script on receiver device, run the same script on the sender device.
# RECEIVER is the IP of receiver device.
# PLAINTEXT is the size of the random plaintext to generate.
$ RECEIVER='192.168.1.12' PLAINTEXT=1000 python3 benchmark_speck.py
```

## To-Do
- [ ] Camellia code is not in Python.
- [ ] Klein only has encryption function, no decryption.
- [x] Print only has encryption function, no decryption.
- [ ] Rectangle code is not in Python.
- [x] Abstract out benchmarking functionality from each algorithm

## Dependencies
- `pip install hwcounter`

## Notes
- Compares 41 existing symmetric key lightweight cryptography (plain encryption) algorithms over 7 performance metrics (Block/Key size, Memory, Gate Area, Latency, Throughput, Power & Energy requirements along with hardware and soft- ware efficiency) as recommended by the NIST report for resource-constrained IoT devices.

## References
- <https://singleboardbytes.com/289/connect-wi-fi-enable-ssh-without-monitor-raspberry-pi.htm>
- <https://github.com/Daksh-Axel/Midori128-64/tree/main/App>
- [Midori: A Block Cipher for Low Energy](https://eprint.iacr.org/2015/1142.pdf)

### SIMON and SPECK
- <https://github.com/inmcm/Simon_Speck_Ciphers/tree/master/Python/simonspeckciphers>
- [The SIMON and SPECK Families of Lightweight Block Ciphers](https://eprint.iacr.org/2013/404)
- <https://github.com/bozhu/NSA-ciphers/>
