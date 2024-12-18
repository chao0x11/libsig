/*
 * The file is under the GNU General Public License v3.0.
 */

#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <cstdlib>  // std::system

#include <chrono>

std::string getSuffix(const std::string& fileName) {
    std::string suffix;
    int mark = 0;
    for (int i = fileName.size()-1; i >= 0; --i) {
        if (fileName[i] == '.') {
            mark = i;
            break;
        }
    }
    for (int i = mark; i < fileName.size(); ++i) {
        suffix.push_back(fileName[i]);
    }
    return suffix;
}

void readFile(const char* fileName, std::vector<unsigned char>& data) {
    std::ifstream file(fileName, std::ios::binary | std::ios::ate);
    std::streamsize size = file.tellg();
    file.seekg(0, std::ios::beg);
    data.resize(size);
    file.read(reinterpret_cast<char*>(data.data()), size);
    file.close();
}

int main(int argc, char* argv[]) {
    auto start = std::chrono::high_resolution_clock::now();

    std::string media = argv[1];
    std::string private_key = argv[2];
    int identity_id = atoi(argv[3]);

    auto openssl_start = std::chrono::high_resolution_clock::now();

    std::string command = "openssl dgst -sha256 -sign ";
    command = command + private_key;
    command = command + " -out signature.bin ";
    command = command + media;
 
    int ret = std::system(command.c_str());

    if (ret !=0) {
        std::cerr << "Error sign file." << std::endl;
        return 1;
    }

    auto openssl_end = std::chrono::high_resolution_clock::now();

    auto openssl_dur = openssl_end - openssl_start;
    auto openssl_milliseconds = 
        std::chrono::duration_cast<std::chrono::milliseconds>(openssl_dur).count();
    
    std::cout << "OpenSSL execution time: " << openssl_milliseconds << " ms\n";

    // Read signature and media content
    std::vector<unsigned char> signature_data;
    std::vector<unsigned char> media_data;
    readFile("signature.bin", signature_data);
    readFile(media.c_str(), media_data);

    // Write media data and signature into a new file
    std::string suffix = getSuffix(media);
    std::string new_file_path = "signed" + suffix;
    std::ofstream outFile(new_file_path, std::ios::binary);
    if (!outFile) {
        std::cerr << "Cannot creat a output file: " << new_file_path << std::endl;
        return 1;
    }

    int sig_size = signature_data.size();
    int total_size = 12 + sig_size;
    int identity = identity_id;
    outFile.write(reinterpret_cast<char*>(media_data.data()), media_data.size());
    outFile.write(reinterpret_cast<char*>(&identity), sizeof(identity_id));
    outFile.write(reinterpret_cast<char*>(&sig_size), sizeof(sig_size));
    outFile.write(reinterpret_cast<char*>(signature_data.data()), signature_data.size());
    outFile.write(reinterpret_cast<char*>(&total_size), sizeof(total_size));

    std::cout << media << " has been signed and save to: " << new_file_path << std::endl;

    ret = std::system("rm signature.bin");

    if (ret != 0) {
        std::cerr << "Error remove tmp file." << std::endl;
        return 1;
    }

    auto end = std::chrono::high_resolution_clock::now();
    auto dur = end - start;
    auto milliseconds = std::chrono::duration_cast<std::chrono::milliseconds>(dur).count();
    
    std::cout << "Total execution time: " << milliseconds << " ms\n";

    return 0;
}
