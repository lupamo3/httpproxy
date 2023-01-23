FROM python:3.9
ENV PYTHONUNBUFFERED 1

# Create a working directory
RUN mkdir /app
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the application will run on
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]