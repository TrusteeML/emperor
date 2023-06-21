all: build run	

build:
	docker build . -t emperor-kitsune

run:
	docker run -it --rm --name emperor-kitsune \
		-v $(shell pwd)/res:/emperor/res/ \
		emperor-kitsune python main.py 

