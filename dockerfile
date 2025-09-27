FROM python:3.11-slim

# 1) Katalog roboczy
WORKDIR /app

# 2) Zależności (lepszy cache warstw)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Kod aplikacji
COPY . .

# 4) Port/uruchomienie
ENV PORT=5000
EXPOSE 5000
CMD ["python", "app.py"]
