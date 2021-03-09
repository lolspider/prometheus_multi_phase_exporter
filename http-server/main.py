from simple_http_server import request_map


@request_map("/api/token", method="POST")
def start_api_token_server():
    return {"jwt_token": "1234567890", "other": "other"}


@request_map("/api/v2/orders", method="GET")
def start_api_token_server():
    return 200


if __name__ == "__main__":
    import simple_http_server.server as server

    def main():
        # The following method can import several controller files once.
        server.scan()
        server.start(port=8080)
    main()
