FROM my_python/rasa:latest

RUN pip3 install fpdf \
  datefinder
RUN pip3 install --upgrade google-api-python-client \
  google-auth-httplib2 \
  google-auth-oauthlib
COPY . /app
EXPOSE 5055
WORKDIR /app
CMD ["rasa", "run", "actions", "--debug"]
