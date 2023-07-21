LAVA_IMAGE ?= ""
RUNTIME ?= "podman"

aemva_version ?= "11.21_15"
morello_version ?= "0.11_34"
cs1k_version ?= "11.19_21"

container_aemva_version = $(shell echo $(aemva_version)|sed -e 's|_|.|g')
container_morello_version = $(shell echo $(morello_version)|sed -e 's|_|.|g')
container_cs1k_version = $(shell echo $(cs1k_version)|sed -e 's|_|.|g')

.PHONE: build

build: fvp-aemva fvp-morello

fvp-aemva: aemva/Dockerfile
	cd aemva && $(RUNTIME) build --build-arg version=$(aemva_version) --tag fvp:aemva-$(container_aemva_version) .

fvp-morello: morello/Dockerfile
	cd morello && $(RUNTIME) build --build-arg version=$(morello_version) --tag fvp:morello-$(container_morello_version) .

fvp-cs1k: cs1k/Dockerfile
	cd cs1k && $(RUNTIME) build --build-arg version=$(cs1k_version) --tag fvp:cs1k-$(container_cs1k_version) .

clean:
	$(RUNTIME) image rm fvp:aemva-$(container_aemva_version) fvp:morello-$(container_morello_version)
