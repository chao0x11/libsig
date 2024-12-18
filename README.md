# libsig
Digital Signature for images and videos. This project is based on [OpenSSL][1], make sure that you have installed OpenSSL before using this code. 

For example, you can install openssl on your Mac OSX using the following command:

    brew install openssl@3

We verified our code on Mac OS 12.7.6:

    openssl version
    OpenSSL 3.4.0 22 Oct 2024 (Library: OpenSSL 3.4.0 22 Oct 2024)

and Ubuntu 22.04.5:

    openssl version
    OpenSSL 3.0.2 15 Mar 2022 (Library: OpenSSL 3.0.2 15 Mar 2022)

## Python demo

We first use `libsig-keys.py` to generate private key and public key locally. 

    python3 libsig-keys.py

The output will be:

    Private key generated at: ./key/private_key.pem
    Public key generated at: ./key/public_key.pem

Then, we can sign an image or a video using `libsig-sign.py`

    python3 libsig-sign.py --media_file ./image-0.jpeg --private_key ./key/private_key.pem --identity_id 3329

The output will be:

    OpenSSL Execution time：11.32 ms
    ./image-0.jpeg has been signed and saved to: ./signed-image-0.jpeg
    Total Execution time：13.36 ms

The `--media_file` argument indicates the input media file, users can replace this file by others, e.g., `video-1.mp4`

The `--private_key` argument indicates the file path of user's private key generated by `libsig-keys.py`

The `--identity_id` argument indicates 'who the signer are'. For example, 3329 is the index of canon, 5643 is the index of Adobe.

After that, we can verify the signature using `libsig-verify.py`

    python3 libsig-verify.py --media_file ./signed-image-0.jpeg --public_key ./key/public_key.pem

The output will be:

    identity_id: 3329
    Verification successful.
    OpenSSL Execution time：22.04 ms
    Total Execution time：24.64 ms

The `--media_file` argument indicates the input file signed by `libsig-sign.py`.

The `--public_key` argument indicates the file path of user's public key generated by `libsig-keys.py`

After that, we can give a second signature to this signed image. We first generate a new public key and private key:

    python3 libsig-keys.py --path key2

The output will be:

    Private key generated at: key2/private_key.pem
    Public key generated at: key2/public_key.pem

Then, we give a second signature:

    python3 libsig-sign.py --media_file ./signed-image-0.jpeg --private_key ./key2/private_key.pem --identity_id 5346

The output will be:

    OpenSSL Execution time：15.59 ms
    ./signed-image-0.jpeg has been signed and saved to: ./signed-signed-image-0.jpeg
    Total Execution time：17.15 ms

Then, we verify the second signature:

    python3 libsig-verify.py --media_file ./signed-signed-image-0.jpeg --public_key ./key2/public_key.pem

The output will be:

    identity_id: 5346
    Verification successful.
    OpenSSL Execution time：14.45 ms
    Total Execution time：18.81 ms

We can give a third or more signatures using the same way:

    python3 libsig-keys.py --path key3
    
    python3 libsig-sign.py --media_file ./signed-signed-image-0.jpeg --private_key ./key3/private_key.pem --identity_id 5643
    
    python3 libsig-verify.py --media_file ./signed-signed-signed-image-0.jpeg --public_key ./key3/public_key.pem

  [1]: https://github.com/openssl/openssl
