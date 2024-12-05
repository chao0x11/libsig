/*
 * The file is under the GNU General Public License v3.0.
 */

#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <cstdlib>  // std::system

int main(int argc, char* argv[]) {
    std::string media = argv[1];
    std::string public_key = argv[2];

    std::ifstream inFile(media, std::ios::binary);
    if (!inFile) {
        std::cerr << "Open file error: " << media << std::endl;
        return 1;
    }

    // Read signature size
    inFile.seekg(0, std::ios::end);
    std::streampos fileSize = inFile.tellg();
    inFile.seekg((int)fileSize - sizeof(int), std::ios::beg);
    int total_size;
    inFile.read(reinterpret_cast<char*>(&total_size), sizeof(total_size));
    int media_size = (int)fileSize - total_size;

    inFile.seekg(0, std::ios::beg);
    std::vector<unsigned char> media_data(media_size);
    inFile.read(reinterpret_cast<char*>(media_data.data()), media_data.size());
    int identity_id;
    inFile.read(reinterpret_cast<char*>(&identity_id), sizeof(identity_id));
    int signature_size;
    inFile.read(reinterpret_cast<char*>(&signature_size), sizeof(signature_size));
    std::vector<unsigned char> signature(signature_size);
    inFile.read(reinterpret_cast<char*>(signature.data()), signature.size());

    std::cout << "indentity id: " << identity_id << std::endl;

    // Write signature and media data into tmp files
    std::ofstream sig_file("tmp-signature.bin", std::ios::binary);
    sig_file.write(reinterpret_cast<char*>(signature.data()), signature.size());
    std::ofstream media_file("tmp-media.bin", std::ios::binary);
    media_file.write(reinterpret_cast<char*>(media_data.data()), media_data.size());

    sig_file.close();
    media_file.close();

    // Verify signature using openssl
    std::string command = "openssl dgst -sha256 -verify ";
    command = command + public_key;
    command = command + " -signature tmp-signature.bin tmp-media.bin";

    int ret = std::system(command.c_str());
    if (ret != 0) {
        std::cerr << "Verification failed." << std::endl;
        return 1;
    } else {
        std::cout << "Verification successful." << std::endl;
    }

    ret = std::system("rm tmp-signature.bin");
    if (ret != 0) {
        std::cerr << "Error remove tmp-signature.bin" << std::endl;
        return 1;
    }

    ret = std::system("rm tmp-media.bin");
    if (ret != 0) {
        std::cerr << "Error remove tmp-media.bin" << std::endl;
        return 1;
    }

    return 0;
}