import urandom


class CharUtils:
    @staticmethod
    def generate_uuid():
        random_bytes = bytearray(urandom.getrandbits(8) for _ in range(16))

        random_bytes[8] = (random_bytes[8] & 0x3F) | 0x80

        uuid_string = "{:02x}{:02x}{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(
            *random_bytes
        )

        return uuid_string
