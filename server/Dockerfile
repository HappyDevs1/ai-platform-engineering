# Use an official lightweight Python image
FROM python:3.12-slim

# Set environment variables to optimize Python behavior inside the container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /gateway

# Copy only the requirements file first to leverage Docker caching
COPY ./requirements.txt /gateway/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /gateway/requirements.txt

# Copy the rest of the application code
COPY . /gateway

# Expose the port FastAPI will run on
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
