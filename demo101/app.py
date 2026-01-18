"""
Simple Flask Application for Docker Demo
Displays a welcome message for Docker class
"""

from flask import Flask, render_template_string
from datetime import datetime
import socket
import os

app = Flask(__name__)

# HTML template with styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Docker Class Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            padding: 50px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 600px;
            animation: fadeIn 0.6s ease-in;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .docker-icon {
            font-size: 80px;
            margin-bottom: 20px;
        }
        
        h1 {
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 20px;
            line-height: 1.3;
        }
        
        .welcome-text {
            color: #667eea;
            font-size: 1.8em;
            font-weight: bold;
            margin-bottom: 15px;
        }
        
        .message {
            color: #555;
            font-size: 1.3em;
            margin-bottom: 30px;
        }
        
        .info-box {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin-top: 30px;
            text-align: left;
            border-radius: 8px;
        }
        
        .info-box h3 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        
        .info-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .info-item:last-child {
            border-bottom: none;
        }
        
        .info-label {
            font-weight: bold;
            color: #555;
        }
        
        .info-value {
            color: #667eea;
            font-family: 'Courier New', monospace;
        }
        
        .footer {
            margin-top: 30px;
            color: #999;
            font-size: 0.9em;
        }
        
        .status {
            display: inline-block;
            background: #10b981;
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="docker-icon">🐳</div>
        <h1>Hello Class!</h1>
        <p class="welcome-text">Welcome to Docker Class</p>
        <p class="message">How is it going?</p>
        <div class="status">✓ Running in Container</div>
        
        <div class="info-box">
            <h3>📊 Container Information</h3>
            <div class="info-item">
                <span class="info-label">Hostname:</span>
                <span class="info-value">{{ hostname }}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Container IP:</span>
                <span class="info-value">{{ container_ip }}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Python Version:</span>
                <span class="info-value">{{ python_version }}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Current Time:</span>
                <span class="info-value">{{ current_time }}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Environment:</span>
                <span class="info-value">{{ environment }}</span>
            </div>
        </div>
        
        <div class="footer">
            <p>This application is running inside a Docker container 🚀</p>
            <p>Container ID: {{ container_id }}</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """
    Main route that displays welcome message with container information
    """
    # Get container hostname (container ID)
    hostname = socket.gethostname()
    
    # Get container IP address
    try:
        container_ip = socket.gethostbyname(socket.gethostname())
    except:
        container_ip = "Unable to determine"
    
    # Get Python version
    import sys
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    # Get current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get environment (from ENV variable or default)
    environment = os.getenv('APP_ENV', 'development')
    
    # Get short container ID (first 12 chars of hostname)
    container_id = hostname[:12]
    
    return render_template_string(
        HTML_TEMPLATE,
        hostname=hostname,
        container_ip=container_ip,
        python_version=python_version,
        current_time=current_time,
        environment=environment,
        container_id=container_id
    )

@app.route('/health')
def health():
    """
    Health check endpoint for container monitoring
    Returns JSON with status information
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "flask-docker-demo",
        "version": "1.0.0"
    }

@app.route('/info')
def info():
    """
    Information endpoint that returns container details in JSON format
    """
    import sys
    
    return {
        "message": "Hello Class, welcome to Docker class, how is it going?",
        "container_info": {
            "hostname": socket.gethostname(),
            "ip_address": socket.gethostbyname(socket.gethostname()),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "timestamp": datetime.now().isoformat(),
            "environment": os.getenv('APP_ENV', 'development')
        }
    }

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.getenv('PORT', 5000))
    
    # Run Flask app
    # host='0.0.0.0' makes it accessible from outside the container
    app.run(host='0.0.0.0', port=port, debug=False)