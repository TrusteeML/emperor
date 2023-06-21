all: build run	

build:
	docker build . -t emperor-nprint-os

run:
	docker run -it --rm --name emperor-nprint-os \
		-v $(shell pwd)/res:/emperor/res/ \
		emperor-nprint-os python main.py 

