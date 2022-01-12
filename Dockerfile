FROM python:3.6-slim

WORKDIR /home/nalog

RUN python -m venv venv
RUN . venv/bin/activate

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt; exit 0
RUN pip install gunicorn

COPY app app
COPY utility_methods utility_methods
COPY app.py boot.sh config.py ./

RUN chmod a+x boot.sh
ENV FLASK_APP app.py

EXPOSE 8282
ENTRYPOINT ["./boot.sh"]
