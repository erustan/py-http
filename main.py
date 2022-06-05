""" Кастомный HTTP сервер на Python """
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler


class OurHandler(BaseHTTPRequestHandler):
    """ Пример обработчика HTTP запросов """

    def not_found(self):
        """ Страница для ненайденных ресурсов (страниц) """
        self.send_response(HTTPStatus.NOT_FOUND)
        self.send_header("Content-Type", "text/html; charset=UTF-8")
        self.end_headers()

        self.wfile.write("<h1>404 Not Found!</h1>".encode("utf-8"))

    def simple_page(self):
        """ Статическая страница с фиксированным HTML """
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=UTF-8")
        self.end_headers()

        self.wfile.write("<h1>Subscribe to @FlongyDev</h1>".encode("utf-8"))

    def echo_page(self):
        """ Эхо-страница: возвращает строку запроса от клиента """
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/plain; charset=UTF-8")
        self.end_headers()

        ip, _ = self.client_address
        msg = f"{self.requestline}\nIP address: {ip}"
        self.wfile.write(msg.encode("utf-8"))

    def file_page(self, filename: str = "index.html"):
        """ Страница из файла """
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=UTF-8")
        self.end_headers()

        with open(filename, 'rb') as f:
            self.wfile.write(f.read())

    def do_GET(self):
        """ Обработка GET запросов к серверу """
        if self.path == "/":
            self.simple_page()
        elif self.path.startswith("/echo"):
            self.echo_page()
        elif self.path.startswith("/index"):
            self.file_page()
        elif self.path.startswith("/say"):
            self.file_page("post-form.html")
        else:
            self.not_found()


if __name__ == "__main__":
    with HTTPServer(('', 8000), OurHandler) as server:
        server.serve_forever()
