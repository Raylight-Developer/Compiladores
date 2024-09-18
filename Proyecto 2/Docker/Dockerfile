FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
	curl \
	bash-completion \
	openjdk-17-jdk \
	fontconfig \
	fonts-dejavu-core \
	software-properties-common \
	&& apt-get clean && rm -rf /var/lib/apt/lists/*

RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y \
	python3-pip

COPY antlr-4.13.1-complete.jar /usr/local/lib/antlr-4.13.1-complete.jar

COPY ./commands/antlr /usr/local/bin/antlr
RUN chmod +x /usr/local/bin/antlr
COPY ./commands/antlr /usr/bin/antlr
RUN chmod +x /usr/bin/antlr

COPY ./commands/grun /usr/local/bin/grun
RUN chmod +x /usr/local/bin/grun
COPY ./commands/grun /usr/bin/grun
RUN chmod +x /usr/bin/grun

COPY python-venv.sh .
RUN chmod +x ./python-venv.sh
RUN ./python-venv.sh

COPY requirements.txt .
RUN pip install -r requirements.txt --break-system-packages 

ARG USER=appuser
ARG UID=1001
RUN adduser \
	--disabled-password \
	--gecos "" \
	--home "$(pwd)" \
	--no-create-home \
	--uid "${UID}" \
	"${USER}"
USER ${UID}

WORKDIR /program