image_name:=zero:latest
remote_image_name:=cupen/zero:latest


build:
	docker build . -t $(image_name)


release: release
	docker tag $(image_name) $(remote_image_name)
	docker push $(remote_image_name)


start:
	docker run --rm -it -p 8787:8787 -p 8000:8000 $(image_name)


deploy:
	fab -H vps6 start


deploy-renew: release
	fab -H vps6 full-restart


