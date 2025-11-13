#!/usr/bin/env python3
"""
LangBot - Dify与飞书集成服务
简单的HTTP服务器，用于处理飞书Webhook和Dify集成
"""

import os
import sys
import json
import logging
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

# 配置日志
log_level = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/langbot/langbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LangBotHandler(BaseHTTPRequestHandler):
    """HTTP请求处理器"""
    
    def do_GET(self):
        """处理GET请求"""
        path = urlparse(self.path).path
        
        if path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'service': 'langbot'
            }
            self.wfile.write(json.dumps(response).encode())
            logger.info("Health check passed")
            
        elif path == '/api/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'service': 'langbot',
                'version': '1.0.0',
                'status': 'running',
                'dify_url': os.getenv('DIFY_API_URL'),
                'feishu_app_id': os.getenv('FEISHU_APP_ID', 'not_set')
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'message': 'LangBot Service',
                'version': '1.0.0',
                'endpoints': {
                    'health': '/health',
                    'status': '/api/status',
                    'feishu_webhook': '/webhook/feishu'
                }
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'error': 'Not found'}
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """处理POST请求"""
        path = urlparse(self.path).path
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        if path == '/webhook/feishu':
            try:
                data = json.loads(body.decode())
                logger.info(f"Received Feishu message: {data}")
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {
                    'code': 0,
                    'msg': 'success'
                }
                self.wfile.write(json.dumps(response).encode())
                logger.info("Feishu message processed successfully")
                
            except Exception as e:
                logger.error(f"Error processing Feishu message: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {
                    'code': -1,
                    'msg': str(e)
                }
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {'error': 'Not found'}
            self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        """重写日志输出"""
        logger.info("%s - - [%s] %s" % (
            self.client_address[0],
            self.log_date_time_string(),
            format % args
        ))

def run_server():
    """运行HTTP服务器"""
    host = os.getenv('LANGBOT_HOST', '0.0.0.0')
    port = int(os.getenv('LANGBOT_PORT', 8080))
    
    server_address = (host, port)
    httpd = HTTPServer(server_address, LangBotHandler)
    
    logger.info(f"Starting LangBot server on {host}:{port}")
    logger.info(f"Dify URL: {os.getenv('DIFY_API_URL')}")
    logger.info(f"Feishu App ID: {os.getenv('FEISHU_APP_ID', 'not_set')}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        httpd.shutdown()
        sys.exit(0)

if __name__ == '__main__':
    run_server()

