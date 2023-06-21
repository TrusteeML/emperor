all: build run	

build:
	docker build . -t emperor-moon-star

run:
	docker run -it --rm --name emperor-moon-star \
		-v $(shell pwd)/res:/emperor/res/ \
		emperor-moon-star python main.py 

