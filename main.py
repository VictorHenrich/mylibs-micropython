from examples.tcp_connection.client import BoardControlService


HOST: str = "192.168.15.106"

PORT: int = 5000

WIT_TOKEN: str = "IAL5B7YCCKLCAINBRUV75RUN3DAZCR4J"


if __name__ == "__main__":
    board_control_service: BoardControlService = BoardControlService(
        host=HOST, port=PORT, wit_token=WIT_TOKEN
    )

    board_control_service.execute()
