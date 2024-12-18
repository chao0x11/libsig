#!/usr/bin/env python3
# libsig-sign.py
#
# This program is licensed under the GPL-3.0 License.

import sys
import os
import base64
import subprocess
import argparse

import time

def sign_media(args):
    media = args.media_file
    private_key = args.private_key
    identity_id = args.identity_id

    openssl_start_time = time.perf_counter()

    # Generate signature using openssl
    result = subprocess.run(
        ["openssl", 
         "dgst", 
         "-sha256", 
         "-sign", 
         private_key, 
         "-out", 
         "signature.bin", 
         media],
        capture_output=True, 
        text=True
    )

    if result.returncode != 0:
        print(f"Error signing media: {result.stderr}")
        exit()

    openssl_end_time = time.perf_counter()

    openssl_execution_time_ms = (openssl_end_time - openssl_start_time) * 1000
    print(f"OpenSSL Execution time：{openssl_execution_time_ms:.2f} ms")

    # Read signature and media content
    with open("signature.bin", "rb") as sig_file:
        signature_data = sig_file.read()

    with open(media, "rb") as media_file:
        media_data = media_file.read()
    
    # Write media data and signature into a new file
    new_file_path = os.path.join(os.path.dirname(media), f"signed-{os.path.basename(media)}")
    with open(new_file_path, "wb") as new_file:
        new_file.write(media_data)
        new_file.write(int(identity_id).to_bytes(4, byteorder="little"))
        new_file.write(len(signature_data).to_bytes(4, byteorder="little"))
        new_file.write(signature_data)
        total_size = 12 + len(signature_data)
        new_file.write(total_size.to_bytes(4, byteorder="little"))

    print(f"{media} has been signed and saved to: {new_file_path}")

    # remove temp file
    os.remove("signature.bin")

if __name__ == "__main__":
    start_time = time.perf_counter()

    parser = argparse.ArgumentParser();
    parser.add_argument("--media_file", help="Media file to sign")
    parser.add_argument("--private_key", help="Path to private key file")
    parser.add_argument("--identity_id", help="Identity ID")
    args = parser.parse_args()
    sign_media(args)

    end_time = time.perf_counter()

    execution_time_ms = (end_time - start_time) * 1000
    print(f"Total Execution time：{execution_time_ms:.2f} ms")
