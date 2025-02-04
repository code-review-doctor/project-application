FROM debian:buster-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
COPY requirements.txt entrypoint.sh tools/wait-for-mysql.sh /code/

RUN apt-get update && apt-get install --no-install-recommends --yes \
	python3-pip python3-setuptools \
	libmariadbclient-dev libmariadb-dev-compat libmariadb3 mariadb-client \
	python3-wheel libpython3.7-dev \
	gcc-7 gcc git \
	wkhtmltopdf
RUN pip3 install -r /code/requirements.txt
RUN apt-get purge -y libmariadbclient-dev libmariadb-dev-compat \
	gcc-7 gcc libpython3.7-dev && \
    apt-get autoremove -y && \
    apt-get clean
WORKDIR /code/ProjectApplication
ENTRYPOINT ["/code/entrypoint.sh"]
