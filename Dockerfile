FROM python:3.12

WORKDIR /application

ENV PYTHONPATH=/application/b4youeat

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 50051
CMD ["python", "-m", "b4youeat.main"]
