run:
	uvicorn main:app --host 0.0.0.0 --port 443 \
		--ssl-keyfile /etc/letsencrypt/live/api.expensiveonlineschools.com/privkey.pem \
		--ssl-certfile /etc/letsencrypt/live/api.expensiveonlineschools.com/fullchain.pem
add:
	git add Makefile domain.sh ext/algo.py ext/stralgo.py main.py misc/append.py requirements.txt 

