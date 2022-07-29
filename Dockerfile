FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "discord_bot/main.py" ]