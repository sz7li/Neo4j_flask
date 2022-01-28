FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# serving flask backend through WSGI server
CMD [ "python", "run.py" ]