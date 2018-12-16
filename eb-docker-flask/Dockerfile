FROM python:3.6

COPY . /app
WORKDIR /app

RUN pip install Flask==1.0.2
RUN pip install --upgrade "watson-developer-cloud>=2.5.1"

ENV IAM_APIKEY <your-api-key>
ENV TRANSLATOR_URL <your-translator-url>

EXPOSE 5000
CMD ["python", "application.py"]