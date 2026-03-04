#!/usr/bin/env python3
"""
Simple HTTP server for Space Guild frontend
Serves static files from SpaceGuildWeb directory
"""

import http.server
import socketserver
import os
import sys

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def log_message(self, format, *args):
        # Print to stdout (not stderr) so it's visible in tmux/terminal
        sys.stdout.write(f"[{self.log_date_time_string()}] {self.address_string()} - {format % args}\n")
        sys.stdout.flush()

    def end_headers(self):
        # Add CORS headers to allow API requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print("=" * 70)
        print("SPACE GUILD - FRONTEND SERVER")
        print("=" * 70)
        print(f"\n[*] Serving frontend at http://localhost:{PORT}")
        print(f"[*] Directory: {DIRECTORY}")
        print("\n[!] Make sure the backend API is running at http://localhost:8000")
        print("\nPress Ctrl+C to stop the server\n")
        print("=" * 70)
        sys.stdout.flush()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n[*] Server stopped")
