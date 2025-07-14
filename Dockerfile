FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]