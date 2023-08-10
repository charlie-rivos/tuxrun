LAVA_IMAGE ?= ""
RUNTIME ?= "podman"

aemva_version ?= "11.21_15"
morello_version ?= "0.11_34"
stdlib_version ?= "11.22_14"
stdlib_tarball ?= "FVP_ARM_Std_Library_11.22_14_Linux64.tgz"

container_aemva_version = $(shell echo $(aemva_version)|sed -e 's|_|.|g')
container_morello_version = $(shell echo $(morello_version)|sed -e 's|_|.|g')
container_stdlib_version = $(shell echo $(stdlib_version)|sed -e 's|_|.|g')

.PHONE: build

build: fvp-aemva fvp-morello

fvp-aemva: aemva/Dockerfile
	cd aemva && $(RUNTIME) build --build-arg version=$(aemva_version) --tag fvp:aemva-$(container_aemva_version) .

fvp-morello: morello/Dockerfile
	cd morello && $(RUNTIME) build --build-arg version=$(morello_version) --tag fvp:morello-$(container_morello_version) .

fvp-stdlib: morello/Dockerfile
	cd stdlib && $(RUNTIME) build --build-arg FVP_STDLIB_PKG=$(stdlib_tarball) --tag fvp:stdlib-$(container_stdlib_version) .

clean:
	$(RUNTIME) image rm fvp:aemva-$(container_aemva_version) fvp:morello-$(container_morello_version)
