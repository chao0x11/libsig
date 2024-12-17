#!/usr/bin/env python3
# libsig-verify.py
#
# This program is licensed under the GPL-3.0 License.

import sys
import os
import base64
import subprocess
import argparse

import time

def verify_signature(args):
    media = args.media_file
    public_key = args.public_key

    try:
        # read last 4 bytes
        with open(media, "rb") as file:
            file.seek(-4, 2)
            total_size = int.from_bytes(file.read(4), byteorder="little")
    
        # Read original media content and signature data
        media_size = os.path.getsize(media) - total_size
        with open(media, "rb") as file:
            media_data = file.read(media_size)
            identity_id = int.from_bytes(file.read(4), byteorder="little")
            signature_size = int.from_bytes(file.read(4), byteorder="little")
            signature = file.read(signature_size)
    except Exception as e:
        print("Read file error. Make sure that the file has been signed.")
        exit()
    
    print(f"identity_id: {identity_id}")

    # Write signature and media data into tmp files
    with open("tmp-signature.bin", "wb") as sig_file:
        sig_file.write(signature)
    with open("tmp-media.bin", "wb") as media_file:
        media_file.write(media_data)

    openssl_start_time = time.perf_counter()

    # Verify signature using openssl
    result = subprocess.run(
        ["openssl", 
         "dgst", 
         "-sha512", 
         "-verify", 
         public_key, 
         "-signature", 
         "tmp-signature.bin", 
         "tmp-media.bin"],
        capture_output=True, 
        text=True
    )

    if result.returncode != 0:
        print(f"Verification failed: {result.stderr}")
        exit()
    else:
        print("Verification successful.")

    openssl_end_time = time.perf_counter()

    openssl_execution_time_ms = (openssl_end_time - openssl_start_time) * 1000
    print(f"OpenSSL Execution time：{openssl_execution_time_ms:.2f} ms")

    # delete tmp files
    os.remove("tmp-signature.bin")
    os.remove("tmp-media.bin")

if __name__ == "__main__":
    start_time = time.perf_counter()

    parser = argparse.ArgumentParser();
    parser.add_argument("--media_file", help="Signed media file")
    parser.add_argument("--public_key", help="Path to public key file")
    args = parser.parse_args()
    verify_signature(args)

    end_time = time.perf_counter()

    execution_time_ms = (end_time - start_time) * 1000
    print(f"Total Execution time：{execution_time_ms:.2f} ms")
