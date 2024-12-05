#!/usr/bin/env python3
# libsig-verify.py
#
# This program is licensed under the GPL-3.0 License.

import sys
import os
import base64
import subprocess
import argparse

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

    # Verify signature using openssl
    result = subprocess.run(
        ["openssl", 
         "dgst", 
         "-sha256", 
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

    # delete tmp files
    os.remove("tmp-signature.bin")
    os.remove("tmp-media.bin")

if __name__ == "__main__":
    parser = argparse.ArgumentParser();
    parser.add_argument("--media_file", help="Signed media file")
    parser.add_argument("--public_key", help="Path to public key file")
    args = parser.parse_args()
    verify_signature(args)