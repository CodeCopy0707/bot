# Step 1: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /bot

# Step 3: Copy the current directory contents into the container
COPY . .

# Step 4: Install any required Python packages
RUN pip install --no-cache-dir telebot google-generativeai asyncio

# Step 5: Expose the port if necessary (not strictly required for Telegram bots)
EXPOSE 8080

# Step 6: Define the command to run the bot
CMD ["python", "bot.py"]

