# Use a full-featured base image with Python
FROM python:3.10-slim

# Set environment vars
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Create virtual environment
RUN python -m venv $VIRTUAL_ENV

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the bot files
COPY . .

# Run the bot
CMD ["python", "main.py"]
