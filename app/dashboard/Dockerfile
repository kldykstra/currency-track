FROM python:3.13-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Plotly Dash app code
COPY . .

# Expose the port Plotly Dash will run on
EXPOSE 8050

# Set environment variables (optional)
ENV DASH_DEBUG_MODE=false

# Run the Plotly Dash app
CMD ["python", "app.py"]