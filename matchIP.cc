#include <iostream>
#include <fstream>
#include <string>

void parse(std::string &line, std::string &ip, std::string &mac);

int main(int argc, char *argv[])
{
    // check
    if (argc != 3)
    {
        std::cout << "Argument error" << std::endl;
        return 0;
    }

    // file IO
    std::ifstream infile(argv[1]);
    std::ofstream outfile(argv[2]);
    outfile << "IP Address" << '\t' << "Mac Address" << std::endl;

    // Parse data
    std::string ipWithMac;
    while (std::getline(infile, ipWithMac))
    {
        std::string ipAdrs, macAdrs;
        parse(ipWithMac, ipAdrs, macAdrs);
        outfile << ipAdrs << '\t' << macAdrs << std::endl;
    }
    
    infile.close();
    outfile.close();
    return 0;
}

void parse(std::string &line, std::string &ip, std::string &mac)
{
    size_t startPos = line.find('(') + 1;
    size_t ipPos = line.find(')');
    ip = line.substr(startPos, ipPos - startPos);

    startPos = line.find("at ") + 3;
    size_t macPos = line.find(" on");
    mac = line.substr(startPos, macPos - startPos);
}
