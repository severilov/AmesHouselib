FROM python:3.9.2-slim-buster
WORKDIR /app
ENV FLASK_APP "app.py"
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY requirements-test.txt requirements-test.txt
RUN pip3 install -r requirements-test.txt
COPY . .
RUN python3 setup.py install
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
