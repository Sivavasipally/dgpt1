# Use a base image with Python and the necessary dependencies
FROM python:3.11.4-slim-bullseye    

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit app code to the container
COPY main.py .

# Expose the port that Streamlit runs on (default is 8501)
EXPOSE 8501

# Set the command to run the Streamlit app
CMD ["streamlit", "run", "main.py"]
