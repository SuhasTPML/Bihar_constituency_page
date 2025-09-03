# Simple HTTP server to serve the Bihar election files
import http.server
import socketserver
import os

# Set the directory to serve files from
directory = r'C:\\Users\\suhas.bhandari\\Downloads\\Bihar elections'
os.chdir(directory)

# Define the port to use
PORT = 8000

# Create the server
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server started at http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")