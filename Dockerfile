# python image
FROM python:3.12-slim
# working directory
WORKDIR /app
# copy all files to /app
COPY . /app
# install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt
# run the entrypoint.sh
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]