FROM python


RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /home/

COPY . .
EXPOSE 8000
CMD [ "python3", "src/main.py" ]
