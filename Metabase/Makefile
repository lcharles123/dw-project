NAME=metaduck
IMAGE=$(NAME):latest
CONTAINER=$(NAME)-run

main:
	cat Makefile

dbuild:
	docker build . --tag $(IMAGE)

dpush:
	docker push $(IMAGE)

dpull:
	docker pull $(IMAGE)

drun:
	docker run -d -p 3000:3000 -m 1GB -e MB_PLUGINS_DIR=/home/plugins -v /root/dw/operdb.duckdb:/operdb.duckdb --name $(CONTAINER) $(IMAGE) 
	#-v path-to-duckdb/:/operdb.duckdb

denter:
	docker exec -it $(CONTAINER) /bin/bash

dclean:
	docker rm -f $(CONTAINER)

dpurge:
	docker image rm -f $(IMAGE) 

