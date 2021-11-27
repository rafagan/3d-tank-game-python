from util.decorator.singleton import singleton


@singleton
class KeyListener:
    ESCAPE = b'\x1b'

    def __init__(self):
        self.key_pressed = {}
        self.key_first_pressed = {}

    def on_keyboard_pressed(self, key: bytes, *args) -> None:
        self.key_pressed[key] = True
        self.key_first_pressed[key] = True

    def on_keyboard_released(self, key: bytes, *args) -> None:
        self.key_pressed[key] = False

    def is_key_first_pressed(self, key_code: bytes):
        return self.key_first_pressed.get(key_code, False)

    def is_key_pressed(self, key_code: bytes) -> None:
        return self.key_pressed.get(key_code, False)

    def update(self) -> None:
        for k in self.key_first_pressed:
            self.key_first_pressed[k] = False
