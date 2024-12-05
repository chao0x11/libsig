/*
 * The file is under the GNU General Public License v3.0.
 */

#include <iostream>
#include <string>
#include <cstdlib>  // std::system

int main(int argc, char* argv[]) {
    
    std::cout << "Generating private key..." << std::endl;
    int ret = std::system("openssl ecparam -genkey -name secp256k1 -out private_key.pem");

    if (ret == 0) {
        std::cout << "Private key successfully generated: private_key.pem" << std::endl;
    } else {
        std::cerr << "Error generating private key." << std::endl;
        return 1;
    }

    std::cout << "Generating public key..." << std::endl;
    ret = std::system("openssl ec -in private_key.pem -pubout -out public_key.pem");

    if (ret == 0) {
        std::cout << "Public key successfully generated: public_key.pem" << std::endl;
    } else {
        std::cerr << "Error generating public key." << std::endl;
        return 1;
    }

    return 0;
}
