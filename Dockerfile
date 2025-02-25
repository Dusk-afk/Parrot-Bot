FROM python:3.10-slim

# Install required packages
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libopus0 \
    libopus-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /bot

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt /bot/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /bot

# Run bot.py when the container launches
CMD ["python", "-u", "bot.py"]
