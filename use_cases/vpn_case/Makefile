all: build run	

build:
	docker build . -t emperor-vpn

run:
	docker run -it --rm --name emperor-vpn \
		-v $(shell pwd)/res:/emperor/res/ \
		emperor-vpn python main.py 

