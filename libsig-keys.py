#!/usr/bin/env python3
# libsig-keys.py
#
# This program is licensed under the GPL-3.0 License.

import sys
import os
import subprocess
import argparse

def generate_keys(args):
    # private key will be stored in /path/private_key.pem
    # public key will be stored in /path/public_key.pem
    path = args.path
    os.makedirs(path, exist_ok=True)

    private_key_path = os.path.join(path, "private_key.pem")

    # Generate private key using openssl
    result = subprocess.run(
        ["openssl", 
         "ecparam", 
         "-genkey", 
         "-name", 
         "secp256k1", 
         "-out", 
         private_key_path],
        capture_output=True, 
        text=True
    )

    if result.returncode != 0:
        print(f"Error generating private key: {result.stderr}")
        exit()
    else:
        print(f"Private key generated at: {private_key_path}")

    public_key_path = os.path.join(path, "public_key.pem")

    # Generate public key from private key
    result = subprocess.run(
        ["openssl", 
         "ec", 
         "-in", 
         private_key_path, 
         "-pubout", 
         "-out", 
         public_key_path],
        capture_output=True, 
        text=True
    )

    if result.returncode != 0:
        print(f"Error generating public key: {result.stderr}")
        exit()
    else:
        print(f"Public key generated at: {public_key_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser();
    parser.add_argument("--path", 
        default="./key", 
        help="Path to the key file")
    args = parser.parse_args()
    generate_keys(args)
