VERSION_FILE=version.txt
ifdef VERSION
  $(shell echo "version=$(VERSION)" > $(VERSION_FILE))
  $(info using version $(VERSION) from parameter input or environment)
else ifneq ("$(wildcard $(VERSION_FILE))","")
  VERSION=$(shell awk -F'=' '/version/{print $$2}' $(VERSION_FILE))
  $(info using version $(VERSION) from file $(VERSION_FILE))
else
  VERSION=$(shell date -u +"%Y-%m-%dT%H-%M-%SZ")
  $(shell echo "version=$(VERSION)" > $(VERSION_FILE))
  $(info using version $(VERSION) which is self-calculated)
endif

CURRENT_BRANCH=${bamboo_planRepository_branchName}
RELEASE_BRANCH=master

IMAGE_NAME=meteogroup/sqs-count-custom-metric

clean:
	rm -f $(VERSION_FILE)

docker-build:
	docker build --no-cache --file=Dockerfile --tag=$(IMAGE_NAME):$(VERSION) .

docker-push:
ifeq ($(CURRENT_BRANCH),$(RELEASE_BRANCH))
		docker tag $(IMAGE_NAME):$(VERSION) $(IMAGE_NAME):latest
		docker push $(IMAGE_NAME):$(VERSION)
		docker push $(IMAGE_NAME):latest
else
		docker tag $(IMAGE_NAME):$(VERSION) $(IMAGE_NAME):${CURRENT_BRANCH}
		docker push $(IMAGE_NAME):${CURRENT_BRANCH}
		docker push $(IMAGE_NAME):$(VERSION)
endif
