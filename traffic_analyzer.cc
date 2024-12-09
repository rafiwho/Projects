#include <pcap.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <netinet/udp.h>
#include <arpa/inet.h>
#include <bits/stdc++.h>
#include <thread>
#include <mutex>

// Global variables to track statistics
std::map<int, int> protocolCount; // Stores protocol usage count
int packetCount = 0;
int totalPacketSize = 0;
std::mutex mtx; // Mutex to protect shared variables

// Function to analyze and update traffic statistics
void analyzeTraffic(const struct pcap_pkthdr *pkthdr, int protocol) {
    std::lock_guard<std::mutex> lock(mtx); // Lock to ensure thread safety
    packetCount++;
    totalPacketSize += pkthdr->len;
    protocolCount[protocol]++;
}
// Filtering variables (currently set to capture all traffic)

int filterProtocol = -1; // -1 means no protocol filtering
// For TCP: filterProtocol = IPPROTO_TCP
// For UDP: filterProtocol = IPPROTO_UDP
std::string filterIP = "10.0.0.1"; // Empty string means no IP filtering

// Packet handler function
void packetHandler(u_char *userData, const struct pcap_pkthdr *pkthdr, const u_char *packet) {
    struct ip *ipHeader = (struct ip *)(packet + 14); // Skip Ethernet header
    std::string srcIP = inet_ntoa(ipHeader->ip_src);
    std::string destIP = inet_ntoa(ipHeader->ip_dst);

    // Check if packet matches the filtering criteria
    if ((filterProtocol != -1 && filterProtocol != ipHeader->ip_p) ||
            (!filterIP.empty() && filterIP != srcIP && filterIP != destIP)) {
        return; // Skip packets that don't match the filter
    }

    // Print packet details
    std::cout << "Source IP: " << srcIP << '\n';
    std::cout << "Destination IP: " << destIP << '\n';
    std::cout << "Protocol: " << (int)ipHeader->ip_p << '\n';
    std::cout << "Packet Length: " << pkthdr->len << '\n';

    // Check for TCP and UDP packets to print port numbers
    if (ipHeader->ip_p == IPPROTO_TCP) {
        struct tcphdr *tcpHeader = (struct tcphdr *)(packet + 14 + (ipHeader->ip_hl * 4));
        std::cout << "Source Port: " << ntohs(tcpHeader->th_sport) << '\n';
        std::cout << "Destination Port: " << ntohs(tcpHeader->th_dport) << '\n';
    } else if (ipHeader->ip_p == IPPROTO_UDP) {
        struct udphdr *udpHeader = (struct udphdr *)(packet + 14 + (ipHeader->ip_hl * 4));
        std::cout << "Source Port: " << ntohs(udpHeader->uh_sport) << '\n';
        std::cout << "Destination Port: " << ntohs(udpHeader->uh_dport) << '\n';
    }

    // Update traffic statistics
    analyzeTraffic(pkthdr, ipHeader->ip_p);
    std::cout << '\n';
}

// Function to display traffic statistics
void displayTrafficStats() {
    std::cout << "Total Packets: " << packetCount << '\n';
    std::cout << "Average Packet Size: " << (packetCount ? totalPacketSize / packetCount : 0) << '\n';
    std::cout << "Protocol Distribution:\n";
    for (const auto &entry : protocolCount) {
        std::cout << "Protocol " << entry.first << ": " << entry.second << " packets\n";
    }
}

// Function to save statistics to a file
void saveStatsToFile() {
    std::ofstream outFile("traffic_stats.txt");
    outFile << "Total Packets: " << packetCount << '\n';
    outFile << "Average Packet Size: " << (packetCount ? totalPacketSize / packetCount : 0) << '\n';
    outFile << "Protocol Distribution:\n";
    for (const auto &entry : protocolCount) {
        outFile << "Protocol " << entry.first << ": " << entry.second << '\n';
    }
    outFile.close();
}

// Capture function for packet capturing in a separate thread
void capturePackets(pcap_t *handle) {
    pcap_loop(handle, 10, packetHandler, nullptr); // Capture 10 packets
}

int main() {
    char errbuf[PCAP_ERRBUF_SIZE];

    // Open the network interface for packet capture
    pcap_t *handle1 = pcap_open_live("h1-eth0", BUFSIZ, 1, 1000, errbuf);

    if (handle1 == nullptr) {
        std::cerr << "Error opening device: " << errbuf << '\n';
        return 1;
    }

    // Capture packets in a separate thread
    std::thread thread1(capturePackets, handle1);

    // Wait for the thread to finish capturing
    thread1.join();

    // Close the pcap handle
    pcap_close(handle1);

    // Display and save statistics after capture
    displayTrafficStats();
    saveStatsToFile();

    return 0;
}
