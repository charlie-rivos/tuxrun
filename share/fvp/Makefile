LAVA_IMAGE ?= ""
RUNTIME ?= "podman"

aemva_version ?= "11.27_19"
ifeq ($(shell uname -m),aarch64)
aemva_version_sha256 ?= "66c9939cb2b2104e415dcddb46a2ab52168e8a2b7f30a339e1c05d5d4864ed1d"
aemva_arch = "Linux64_armv8l"
else
aemva_version_sha256 ?= "cd70946a6b632950dca5def33d7656991a29827fa2f6f72f75011d85bdcee248"
aemva_arch = "Linux64"
endif
morello_version ?= "0.11_34"
morello_version_sha256 ?= "ed1e110fb7fa8732d4f1bea9af69491a9e3f7dbf57d2ce6ea916d3cdf910d324"

container_aemva_version = $(shell echo $(aemva_version)|sed -e 's|_|.|g')
container_morello_version = $(shell echo $(morello_version)|sed -e 's|_|.|g')

.PHONE: build

build: fvp-aemva fvp-morello

fvp-aemva: aemva/Dockerfile
	cd aemva && $(RUNTIME) build --build-arg version=$(aemva_version) --build-arg version_sha256=$(aemva_version_sha256) --build-arg arch=$(aemva_arch) --tag fvp:aemva-$(container_aemva_version) .

fvp-morello: morello/Dockerfile
	cd morello && $(RUNTIME) build --build-arg version=$(morello_version) --build-arg version_sha256=$(morello_version_sha256) --tag fvp:morello-$(container_morello_version) .

clean:
	$(RUNTIME) image rm fvp:aemva-$(container_aemva_version) fvp:morello-$(container_morello_version)
