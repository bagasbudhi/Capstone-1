#include <iostream>
#include <csignal>

#include <serial_wrapper/serial_wrapper.hpp>

micron::SerialWrapper<> sw("/dev/ttyUSB0", micron::baud_rate_t(115200));

void sigHandler(int sig){
    (void)sig;
    sw.stop();
}

int main(int argc, char** argv){
    std::string data( "Test from PC" );
    std::string received_data;
    while(sw.isRunning()){
        
        sw.sendData(data);

        received_data = sw.getData();
        std::cout << "Received data : " << received_data << std::endl;

        boost::this_thread::sleep_for(boost::chrono::milliseconds{100});
    }

    return 0;
}
