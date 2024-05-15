# Define the root of the local git clone for the common rules to be able 
# know where they are running from.
REPOROOT=../../..
# Include a library of common .transform.* targets which most
# transforms should be able to reuse.  However, feel free
# to override/redefine the rules below. 
include ../../.make.transforms

TRANSFORM_NAME=noop
# $(REPOROOT)/.make.versions file contains the versions
DOCKER_IMAGE_VERSION=${NOOP_VERSION}

venv::	.transforms.venv

build::	.transforms.build

test::	.transforms.test

clean:: .transforms.clean

image:: .transforms.image

test-src:: .transforms.test-src

setup:: .transforms.setup

test-image:: .transforms.test-image

publish:: .transforms.publish

run-cli-ray-sample: .transforms.run-cli-ray-sample

run-local-sample: .transforms.run-local-sample

run-local-ray-sample: .transforms.run-local-ray-sample

run-s3-ray-sample: .transforms.run-s3-ray-sample

minio-start:	.minio-start

load-image:: .transforms.load-image

update-toml:: 
	@# Help: Copy the Makefile distribution version into the pyproject.toml
	sed -e 's/^version[ ]*=.*/version = "'${DPK_LIB_VERSION}'"/' pyproject.toml > tt.toml
	mv tt.toml pyproject.toml       
	
setup:: 
	
build-wheel:: update-toml 
	@# Help: Build the distribution for publishing to a pypi
	rm -r dist || true
	rm -rf src/*egg-info || true 
	${PIP} install --upgrade build 
	${PYTHON} -m build
	
publish-wheel:: build test-src 
	@# Help: Publish project to pypi 
	${PYTHON} -m twine check dist/*
	${PYTHON} -m twine upload --verbose --non-interactive dist/*
	#@echo "create a git tag to reference published version"
	#@git tag ${TAG}
	#@git push origin ${TAG}
