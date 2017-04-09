def app(environ, start_response):
        data = b"Hello, World!\n"
        data += str.encode(environ['QUERY_STRING'])
        start_response("200 OK", [
            ("Content-Type", "text/plain"),
            ("Content-Length", str(len(data)))
        ])
        return [data]
