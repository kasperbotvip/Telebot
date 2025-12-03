FROM python:3.11-slim

# تثبيت ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# نسخ الملفات
WORKDIR /app
COPY . .

# تثبيت المكتبات
RUN pip install -r requirements.txt

# أمر التشغيل
CMD ["python", "app.py"]
