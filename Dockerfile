FROM openjdk:8-jre-alpine


RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

	
	
WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt                                                                            

EXPOSE 80

RUN chmod 644 server.py

CMD ["python3","server.py"]
