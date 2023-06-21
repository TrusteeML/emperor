all: build run	

build:
	docker build . -t emperor-heartbleed

run:
	docker run -it --rm --name emperor-heartbleed \
		-v $(shell pwd)/res:/emperor/res/ \
		emperor-heartbleed python main.py 

