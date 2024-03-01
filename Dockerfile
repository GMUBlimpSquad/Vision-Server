FROM python

COPY . .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt


CMD [ "python3", "src/main.py" ]
