FROM python:3.11

WORKDIR /pyassist

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "pyassist/pyassist.py"]