FROM my_python/rasa:latest

RUN pip3 install fpdf
COPY . /app
EXPOSE 5055
WORKDIR /app
CMD ["rasa", "run", "actions", "--debug"]