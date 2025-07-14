FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
COPY . .
CMD ["gunicorn", "app:create_app()", "--bind", "0.0.0.0:80"]