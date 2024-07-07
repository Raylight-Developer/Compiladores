FROM ubuntu:latest

RUN apt-get update -y \
  && apt-get install -y --no-install-recommends build-essential bison flex g++ mono-mcs \
  && rm -rf /var/lib/apt/lists/*

COPY files /home/files

VOLUME /home
WORKDIR /home/files

RUN flex simple_language.lex
RUN bison -d simple_language.y
RUN g++ -o parser simple_language.tab.c lex.yy.c
RUN ./script.bash