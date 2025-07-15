FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
COPY . .
CMD ["/bin/bash", "docker-entrypoint.sh"]