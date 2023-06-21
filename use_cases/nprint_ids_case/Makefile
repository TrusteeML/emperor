all: build run	

build:
	docker build . -t emperor-nprint-ids

run:
	docker run -it --rm --name emperor-nprint-ids \
		-v $(shell pwd)/res:/emperor/res/ \
		emperor-nprint-ids python main.py 

