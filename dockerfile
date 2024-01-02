# For more information, please refer to https://aka.ms/vscode-docker-python
FROM nikolaik/python-nodejs:python3.10-nodejs16-alpine

EXPOSE 5002

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1


WORKDIR /app

# 前端打包
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build


# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt --verbose

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python","server/app.py"]
