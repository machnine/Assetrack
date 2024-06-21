# python image
FROM python:3.12-slim

# working directory
WORKDIR /app

# copy the requirements file
COPY requirements.txt /app/requirements.txt

# install dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# copy all files to /app
COPY . /app/

# copy the shell scripts
COPY entrypoint.sh /app/

# make the shell scripts executable
RUN chmod +x /app/entrypoint.sh

# set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]