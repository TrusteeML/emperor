#include "IPv4Layer.h"
#include "Packet.h"
#include "PcapFileDevice.h"

#include <map>
#include <fstream>
#include <sstream>
#include <iostream>
#include <filesystem>

using namespace std;
namespace fs = std::__fs::filesystem;

string PCAPS_FOLDER = "../pcaps-100/";
string LABELS_INPUT = "../labels-os.txt";
string LABELS_OUTPUT = "../labels-100.txt"; 

map<string, string> read_labels() {
    map<string, string> labels;
    // File pointer
    fstream labels_file;
    // Open an existing file
    labels_file.open(LABELS_INPUT, ios::in);
    // Read the Data from the file
    vector<string> row;
    string line, word;
    
    int row_count = 0;
    while (getline(labels_file, line)) {
        row.clear();
        // used for breaking words
        stringstream s(line);
        // read every column data of a row and
        while (getline(s, word, ',')) {
            // add all the column data of a row to a vector
            row.push_back(word);
        }

        // skipping header
        if (row_count != 0) {
            labels[row[0]] = row[1];
        }
        row_count++;
    }

    return labels;
}

void write_labels(map<string, string> pcap_labels) {
    ofstream outfile;
    outfile.open(LABELS_OUTPUT);
    outfile << "item, label\n";
    for (auto it = pcap_labels.cbegin(); it != pcap_labels.cend(); ++it) {
        cout << it->first << " " << it->second <<  "\n";
        outfile << it->first << "," << it->second <<  "\n";
    }
    outfile.close();
}

int main(int argc, char* argv[])
{
    map<string, string> labels = read_labels();
    for (auto it = labels.cbegin(); it != labels.cend(); ++it) {
        cout << it->first << " " << it->second <<  "\n";
    }

    map<string, string> pcap_labels;
    for (const auto & entry : fs::directory_iterator(PCAPS_FOLDER)) {
        string pcap_path = entry.path().string().replace(0, 3, "");
        cout << pcap_path << endl;
         // open a pcap file for reading
        pcpp::PcapFileReaderDevice reader(entry.path());
        if (!reader.open()) {
            printf("Error opening the pcap file\n");
            return 1;
        }

        // read the first packet from the file (in this case the
        // file contains only one packet)
        pcpp::RawPacket raw_packet;
        if (!reader.getNextPacket(raw_packet)) {
            printf("Couldn't read the first packet in the file\n");
            return 1;
        }

        // parse the raw packet into a parsed packet
        pcpp::Packet parsed_packet(&raw_packet);

        // check if it's an IPv4 packet
        if (parsed_packet.isPacketOfType(pcpp::IPv4)) {
            // extract source and dest IPs
           // extract source and dest IPs
            auto src_ip = parsed_packet.getLayerOfType<pcpp::IPv4Layer>()->getSrcIPv4Address().toString();
            auto dst_ip = parsed_packet.getLayerOfType<pcpp::IPv4Layer>()->getDstIPv4Address().toString();
            
            if (labels.find(src_ip) != labels.end()) {
                pcap_labels[pcap_path] = labels[src_ip];
            } else {
                // print source and dest IPs
                printf("Source IP not found! Src Ip is '%s'; Dest IP is '%s'\n", src_ip.c_str(), dst_ip.c_str());
            }
        }

        // close the file
        reader.close();
    }

    write_labels(pcap_labels);

    return 0;
}