all: build run	

build:
	docker build . -t emperor-iot

run:
	docker run -it --rm --name emperor-iot \
		-v $(shell pwd)/res:/emperor/res/ \
		emperor-iot python main.py 

