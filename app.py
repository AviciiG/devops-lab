import os
import MySQLdb
from http.server import BaseHTTPRequestHandler, HTTPServer

DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

def fetch_users():
    try:
        db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME)
        cursor = db.cursor()
        # Создание таблицы и вставка данных
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50), role VARCHAR(50))")
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users (username, role) VALUES ('alice', 'admin'), ('bob', 'user')")
            db.commit()

        cursor.execute("SELECT username, role FROM users")
        data = cursor.fetchall()
        db.close()
        return "<h2>Данные из DB-Server:</h2><ul>" + "".join([f"<li>User: {u[0]}, Role: {u[1]}</li>" for u in data]) + "</ul>"
    except Exception as e:
        return f"<h1>Ошибка подключения к базе данных!</h1><p>{e}</p><p>Адрес БД: {DB_HOST}</p>"

# Простой HTTP-сервер для имитации NGINX 
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html_content = f"""
        <html>
        <head><title>DevOps Lab</title></head>
        <body>
            <h1>Web-Server (NGINX/Python) запущен!</h1>
            {fetch_users()}
        </body>
        </html>
        """
        self.wfile.write(html_content.encode())

if __name__ == '__main__':
    httpd = HTTPServer(('0.0.0.0', 8080), SimpleHTTPRequestHandler)
    print("Starting web server on port 8080...")
    httpd.serve_forever()