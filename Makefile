NSPACE="geovbra"
APP="vmdata"
VER="0.1.0"
RPORT="6405"
FPORT="5005"
UID="876469"
GID="816966"

list-targets:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'


list:
	-docker ps -a | grep ${NSPACE}
	-docker images | grep ${NSPACE}


build-db:
	docker pull redis:6

build-api:
	docker build -t ${NSPACE}/${APP}-api:${VER} \
                     -f docker/Dockerfile.api \
                     ./

build-wrk:
	docker build -t ${NSPACE}/${APP}-wrk:${VER} \
                     -f docker/Dockerfile.wrk \
                     ./


run-db:
	docker run --name ${NSPACE}-db \
                   -p ${RPORT}:6379 \
                   -d \
                   -u ${UID}:${GID} \
                   -v ${PWD}/data/:/data \
                   redis:6 \
                   --save 1 1

run-api:
	RIP=$$(docker inspect ${NSPACE}-db | grep \"IPAddress\" | head -n1 | awk -F\" '{print $$4}') && \
	docker run --name ${NSPACE}-api \
                   --env REDIS_IP=${RIP} \
                   -p ${FPORT}:5000 \
                   -d \
                   ${NSPACE}/${APP}-api:${VER} 

run-wrk:
	RIP=$$(docker inspect ${NSPACE}-db | grep \"IPAddress\" | head -n1 | awk -F\" '{print $$4}') && \
	docker run --name ${NSPACE}-wrk \
                   --env REDIS_IP=${RIP} \
                   -d \
                   ${NSPACE}/${APP}-wrk:${VER} 


clean-db:
	-docker stop ${NSPACE}-db && docker rm -f ${NSPACE}-db

clean-api:
	-docker stop ${NSPACE}-api && docker rm -f ${NSPACE}-api

clean-wrk:
	-docker stop ${NSPACE}-wrk && docker rm -f ${NSPACE}-wrk


push-api:
	docker push ${NSPACE}/${APP}-api:${VER}

push-wrk:
	docker push ${NSPACE}/${APP}-wrk:${VER}


build-all: build-db build-api build-wrk

run-all: run-db run-api run-wrk

clean-all: clean-db clean-api clean-wrk

push-all: push-api push-wrk

all: clean-all build-all run-all 
