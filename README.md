# libsig
Signature for image, video, and audio. This project is based on OpenSSL, make sure that you have installed OpenSSL before using this code. 

For example, you can install openssl on your mac using the following command:

    brew install openssl@3

Then verify the installation:

    openssl version
    OpenSSL 3.4.0 22 Oct 2024 (Library: OpenSSL 3.4.0 22 Oct 2024)

## Python demo

We first use `libsig-keys.py` to generate private key and public key locally. 

    python3 libsig-keys.py

The output will be:

    Private key generated at: ./key/private_key.pem
    Public key generated at: ./key/public_key.pem

Then, we can sign an image or a video using `libsig-sign.py`

    python3 libsig-sign.py --media_file ./image-0.jpeg --private_key ./key/private_key.pem --identity_id 3329

The output will be:

    ../images/image-0.jpeg has been signed and saved to: 
    ../images/signed-image-0.jpeg
    Execution time：14.94 ms

The `--media_file` argument indicates the input media file, users can replace this file by others, e.g. `video-0.mp4` or `audio-0.mp3`

The `--private_key` argument indicates the file path of private key generated by `libsig-keys.py`

The `--identity_id` argument indicates 'who the signer are'. For example, 3329 is the index of canon, 5643 is the index of Adobe.

After that, we can verify the signature using `libsig-verify.py`

    python3 libsig-verify.py --media_file ./signed-image-0.jpeg --public_key ./key/public_key.pem

The output will be:

    identity_id: 3329
    Verification successful.

The `--media_file` argument indicates the input file signed by `libsig-sign.py`.

The `--public_key` argument indicates the file path of public key generated by `libsig-keys.py`

## C++ demo

We first use `libsig-keys.cc` to generate private key and public key locally. 

    g++ libsig-keys.cc -o libsig-keys
    ./libsig-keys
    
The output will be:

    Generating private key...
    Private key successfully generated: private_key.pem
    Generating public key...
    read EC key
    writing EC key
    Public key successfully generated: public_key.pem

Then, we can sign a image or a video using `libsig-sign.cc`

    g++ libsig-sign.cc -o libsig-sign
    ./libsig-sign ./image-0.jpeg ./private_key.pem 3329
    
The output will be:

    ./image-0.jpeg has been signed and save to: signed.jpeg

`./image-0.jpeg` indicates the input file, users can replace this file by others.

`./private_key.pem` indicates the file path of user's private key generated by `libsig-keys.cc`

`3329` is the identity id indicates who is the signer.

After that, we can verify the signature using `libsig-verify.cc`

    g++ libsig-verify.cc -o libsig-verify
    ./libsig-verify signed.jpeg ./public_key.pem
    
The `signed.jpeg` is the input file signed by `libsig-sign.cc` and the `./public_key.pem` indicates the file path of user's public key generated by `libsig-keys.cc`
    
The output will be:

    indentity id: 3329
    Verified OK
    Verification successful.
