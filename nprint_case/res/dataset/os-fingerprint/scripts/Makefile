include /usr/local/etc/PcapPlusPlus.mk

# All Target
all:
	g++ -std=c++11 $(PCAPPP_INCLUDES) -c -o gen_labels.o gen_labels.cpp
	g++ -std=c++11 $(PCAPPP_LIBS_DIR) -o gen_labels gen_labels.o $(PCAPPP_LIBS)
	g++ -std=c++11 $(PCAPPP_INCLUDES) -c -o dataset_info.o dataset_info.cpp
	g++ -std=c++11 $(PCAPPP_LIBS_DIR) -o dataset_info dataset_info.o $(PCAPPP_LIBS)

# Clean Target
clean:
	rm gen_labels.o
	rm gen_labels
	rm dataset_info.o
	rm dataset_info