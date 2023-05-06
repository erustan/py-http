""" Кастомный HTTP сервер на Python """
import urllib.parse
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler


def dict_as_html_table(data: dict[str, str]) -> str:
    """ Форматирование словаря в виде HTML таблицы """
    lines = []
    for key, val in data.items():
        lines.append(f"<tr><td>{key}</td><td>{val}</td></tr>")

    return f"<table border=\"1\"><tr><th>key</th><th>value</th></tr>{''.join(lines)}</table>"


class OurHandler(BaseHTTPRequestHandler):
    """ Пример обработчика HTTP запросов """

    def _headers(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=UTF-8")

    def not_found(self):
        """ Страница для ненайденных ресурсов (страниц) """
        self.send_response(HTTPStatus.NOT_FOUND)
        self.send_header("Content-Type", "text/html; charset=UTF-8")
        self.end_headers()

        self.wfile.write("<h1>404 Not Found!</h1>".encode("utf-8"))

    def simple_page(self, body: str = "<h1>Subscribe to @FlongyDev</h1>"):
        """ Статическая страница с фиксированным HTML """
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=UTF-8")
        self.end_headers()

        self.wfile.write(body.encode("utf-8"))

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


    def dummy_page(self):
        self._headers()
        self.wfile.write(b"Dummy page for debug")

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

    def _process_post_urlencoded(self) -> dict[str, str]:
        """ Парсинг POST запросов типа `application/x-www-form-urlencoded` """
        length = int(self.headers["Content-Length"])
        data = self.rfile.read(length).decode("ascii")
        result = {}
        for pair in data.split('&'):
            key, value = pair.split('=', 1)
            result[urllib.parse.unquote(key)] = urllib.parse.unquote(value)

        return result

    def do_POST(self):
        """ Обработка POST запросов к серверу """
        content_type = self.headers["Content-Type"]
        if content_type == "application/x-www-form-urlencoded":
            result = self._process_post_urlencoded()
            self.simple_page(dict_as_html_table(result))
        else:
            self.log_error("Unknown content_type: %s", content_type)


if __name__ == "__main__":
    with HTTPServer(('', 8000), OurHandler) as server:
        server.serve_forever()
