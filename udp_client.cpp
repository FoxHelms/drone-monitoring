#include <iostream>
#include <cstring>      // For memset()
#include <unistd.h>     // For close()
#include <arpa/inet.h>  // For inet_pton(), sockaddr_in
#include <sys/socket.h> // For socket functions

#define SERVER_PORT 8889
#define BUFFER_SIZE 1518

int main() {
    int sockfd;
    struct sockaddr_in serverAddr;
    char buffer[BUFFER_SIZE];

    // Create UDP socket
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("Socket creation failed");
        return 1;
    }

    // Configure server address
    memset(&serverAddr, 0, sizeof(serverAddr));
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(SERVER_PORT);
    inet_pton(AF_INET, "192.168.10.1", &serverAddr.sin_addr);  // Change IP if needed

    socklen_t addrLen = sizeof(serverAddr);

    std::cout << "Type messages to send (type 'exit' to quit):\n";

    while (true) {
        std::cout << "> ";
        std::string message;
        std::getline(std::cin, message);

        // Send message
        sendto(sockfd, message.c_str(), message.length(), 0,
               (struct sockaddr*)&serverAddr, addrLen);

        if (message == "exit") {
            break;
        }

        // Receive response
        ssize_t recvLen = recvfrom(sockfd, buffer, BUFFER_SIZE - 1, 0,
                                   (struct sockaddr*)&serverAddr, 
&addrLen);
        if (recvLen < 0) {
            perror("recvfrom failed");
            break;
        }

        buffer[recvLen] = '\0';
        std::cout << "Server: " << buffer << "\n";
    }

    close(sockfd);
    return 0;
}

