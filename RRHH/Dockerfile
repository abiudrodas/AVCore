FROM my_python/rasa:latest

COPY . /app
EXPOSE 5006
WORKDIR /app
ENV ACTIONS=http://action-service:5055/webhook
RUN rasa train core
CMD ["rasa", "run", "-p", "5006", "--debug"]