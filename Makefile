image_name:=zero:latest


build:
	docker build . -t $(image_name)


release: build
	docker tag $(image_name) $(remote_image_name)
	docker push $(remote_image_name)


start:
	docker run --rm -it -p 8787:8787 -p 8000:8000 $(image_name)


deploy:
	fab -H vps install start


deploy-renew:
	fab -H vps install restart 

check:
	fab -H vps check



