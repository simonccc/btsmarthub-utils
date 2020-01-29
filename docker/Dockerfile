FROM alpine:latest
RUN apk add --no-cache python3
RUN pip3 install graphyte
RUN pip3 install requests
COPY smarthub.py /
ENTRYPOINT [ "python3", "-u", "./smarthub.py" ]
