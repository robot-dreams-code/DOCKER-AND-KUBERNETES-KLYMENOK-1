for ((i=0;i<10;i++)); do
	docker run -d -p 808${i}:80 nginx
done
