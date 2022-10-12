FROM openjdk:slim
WORKDIR /usr/src/app
COPY    . /usr/src/app
RUN apt update -y \
    && apt install maven -y \
    && mvn clean install -DskipTests
CMD ["mvn", "clean", "test"]