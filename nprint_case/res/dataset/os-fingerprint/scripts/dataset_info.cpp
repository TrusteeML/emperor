#include "IPv4Layer.h"
#include "TcpLayer.h"
#include "UdpLayer.h"
#include "Packet.h"
#include "PcapFileDevice.h"

#include <map>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <filesystem>

using namespace std;
namespace fs = std::__fs::filesystem;

string PCAPS_FOLDER = "../pcaps/";
string DATASET_OUTPUT = "../dataset_info.csv"; 

vector<string> TCP_HEADERS = {
    "flags_ack",
    "flags_cwr",
    "flags_ecn",
    "flags_fin",
    "flags_push",
    "flags_reset",
    "flags_syn",
    "flags_urg",
    "data_offset", 
    "window_size",
};

vector<string> TCP_OPTIONS_STRING = {
    "NOP",
    "EOL",
    "MSS",
    "WINDOW_SCALING",
    "SACK_PERM",
    "SACK",
    "ECHO",
    "ECHOREPLY",
    "TIMESTAMP",
    "CC",
    "CCNEW",
    "CCECHO",
    "MD5",
    "MPTCP",
    "SCPS",
    "SNACK",
    "RECBOUND",
    "CORREXP",
    "QS",
    "USER_TO",
    "EXP_FD",
    "EXP_FE",
    "RVBD_PROBE",
    "RVBD_TRPY",
    "Unknown",
};

vector<pcpp::TcpOptionType> TCP_OPTIONS = {
    pcpp::PCPP_TCPOPT_NOP,
    pcpp::PCPP_TCPOPT_EOL,
    pcpp::TCPOPT_MSS,
    pcpp::PCPP_TCPOPT_WINDOW,
    pcpp::TCPOPT_SACK_PERM,
    pcpp::PCPP_TCPOPT_SACK,
    pcpp::TCPOPT_ECHO,
    pcpp::TCPOPT_ECHOREPLY,
    pcpp::PCPP_TCPOPT_TIMESTAMP,
    pcpp::TCPOPT_CC,
    pcpp::TCPOPT_CCNEW,
    pcpp::TCPOPT_CCECHO,
    pcpp::TCPOPT_MD5,
    pcpp::TCPOPT_MPTCP,
    pcpp::TCPOPT_SCPS,
    pcpp::TCPOPT_SNACK,
    pcpp::TCPOPT_RECBOUND,
    pcpp::TCPOPT_CORREXP,
    pcpp::TCPOPT_QS,
    pcpp::TCPOPT_USER_TO,
    pcpp::TCPOPT_EXP_FD,
    pcpp::TCPOPT_EXP_FE,
    pcpp::TCPOPT_RVBD_PROBE,
    pcpp::TCPOPT_RVBD_TRPY,
    pcpp::TCPOPT_Unknown
};


vector<string> IP_HEADERS = {"protocol", "src_ip", "dst_ip", "ttl"};

void write_info(vector<vector<string>> pcap_info) {
    ofstream outfile;
    outfile.open(DATASET_OUTPUT);

    vector<string> header_row;
    header_row.insert(header_row.end(), IP_HEADERS.begin(), IP_HEADERS.end());
    header_row.insert(header_row.end(), TCP_HEADERS.begin(), TCP_HEADERS.end());
    header_row.insert(header_row.end(), TCP_OPTIONS_STRING.begin(), TCP_OPTIONS_STRING.end());

    for (int i = 0; i < header_row.size(); i++) {
        if (i < header_row.size() - 1) {
            // cout << header_row[i] << ",";
            outfile << header_row[i] << ",";
        } else {
            // cout << header_row[i] << "\n";
            outfile << header_row[i] << "\n";
        }
    }

    for (int i = 0; i < pcap_info.size(); i++) {
        for (int j = 0; j < pcap_info[i].size(); j++) {
            if (j < pcap_info[i].size() - 1) {
                // cout << pcap_info[i][j] << ",";
                outfile << pcap_info[i][j] << ",";
            } else {
                // cout << pcap_info[i][j] << "\n";
                outfile << pcap_info[i][j] << "\n";
            }
        }
    }

    outfile.close();
}

int main(int argc, char* argv[])
{
    vector<vector<string>> pcap_info;
    for (const auto & entry : fs::directory_iterator(PCAPS_FOLDER)) {
        string pcap_path = entry.path().string().replace(0, 3, "");
        // cout << pcap_path << endl;
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
            vector<string> packet_info;
            string protocol;

            auto ip_layer = parsed_packet.getLayerOfType<pcpp::IPv4Layer>();
            auto src_ip = ip_layer->getSrcIPv4Address().toString();
            auto dst_ip = ip_layer->getDstIPv4Address().toString();
            auto ttl = ip_layer->getIPv4Header()->timeToLive;

            auto tcp_layer = parsed_packet.getLayerOfType<pcpp::TcpLayer>();
            if (tcp_layer != nullptr) {
                protocol = "TCP";
                packet_info = {
                    protocol, 
                    src_ip, 
                    dst_ip, 
                    to_string(ttl), 
                    // headers
                    to_string(tcp_layer->getTcpHeader()->ackFlag),
                    to_string(tcp_layer->getTcpHeader()->cwrFlag),
                    to_string(tcp_layer->getTcpHeader()->eceFlag),
                    to_string(tcp_layer->getTcpHeader()->finFlag),
                    to_string(tcp_layer->getTcpHeader()->pshFlag),
                    to_string(tcp_layer->getTcpHeader()->rstFlag),
                    to_string(tcp_layer->getTcpHeader()->synFlag),
                    to_string(tcp_layer->getTcpHeader()->urgFlag),
                    to_string(tcp_layer->getTcpHeader()->dataOffset),
                    to_string(tcp_layer->getTcpHeader()->windowSize),
                };
                
                // options
                for (int i = 0; i != TCP_OPTIONS.size(); i++) {
                    auto opt = TCP_OPTIONS[i];
                    auto option_size = tcp_layer->getTcpOption(opt).getDataSize();
                    if (option_size > 0) {
                        auto option_value = tcp_layer->getTcpOption(opt).getValue();
                        std::ostringstream convert;
                        for (int j = 0; j < option_size; j++) {
                            convert << (int)option_value[j];
                        }
                        std::string option_value_str = convert.str();
                        packet_info.push_back(option_value_str);
                    } else {
                        packet_info.push_back("-1");
                    }
                }
            }

            auto udp_layer = parsed_packet.getLayerOfType<pcpp::UdpLayer>();
            if (udp_layer != nullptr) {
                protocol = "UDP";
                packet_info = {
                    protocol, 
                    src_ip, 
                    dst_ip, 
                    to_string(ttl), 
                    // headers
                    "-1",
                    "-1",
                    "-1",
                    "-1",
                    "-1",
                    "-1",
                    "-1",
                    "-1",
                    "-1",
                    "-1"
                };

                for (int i = 0; i != TCP_OPTIONS.size(); i++) {
                    packet_info.push_back("-1");
                }
            }
            
            pcap_info.push_back(packet_info);
        }

        // close the file
        reader.close();
    }

    write_info(pcap_info);

    return 0;
}