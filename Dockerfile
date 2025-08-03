FROM python:3.9-slim

COPY random_quote.py /
COPY templates/index.html /
COPY templates/quote.html /
COPY templates/form.html /


RUN pip install flask

CMD ["python", "/random_quote"]


