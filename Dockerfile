FROM python:3.9 
COPY ./src /app
COPY ./data /app/data
COPY ./requirements.txt /app/.
COPY ./output.sh /app/.
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["bash", "output.sh"]