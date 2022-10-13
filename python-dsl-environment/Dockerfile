FROM openjdk:slim
WORKDIR /usr/src/app
COPY    requirements.txt /usr/src/app
COPY    main.py /usr/src/app
RUN apt update -y \
    && apt install python3 -y \
    && apt install python3-pip -y \
    && pip install --no-cache-dir -r requirements.txt
CMD ["python3", "main.py"]