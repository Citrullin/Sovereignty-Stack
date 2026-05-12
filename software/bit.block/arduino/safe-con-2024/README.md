# Safe{CON} 2024 Astronaut on Moon Demo

Keep in mind, it's the Arduino IDE and just a PoC and learning tool.
In order to make it work, you need to flash the right songs onto the micro sd card.
As well as training the speech recognition model for the right commands.

This should(tm) be the API for it.

| Endpoint | Method | Payload |
| :--- | :--- | :--- |
| `192.168.178.57/.well-known/wot-thing-description` | GET | *None* |
| `192.168.178.57/things/bit_block/actions/sound` | POST | `{"repeat": 0, "data": [[57, 200], [0, 0]]}` |
| `192.168.178.57/things/bit_block/actions/stop_sound` | POST | `{}` |
| `192.168.178.57/things/bit_block/actions/moon_light` | POST | `{"repeat": 1, "data": [[1000, 255, 0, 0], [1000, 0, 255, 0], [1000, 50, 0, 200], [1000, 50, 150, 155], [1000, 100, 0, 50], [0, 0, 0, 0]]}` |
| `192.168.178.57/things/bit_block/actions/moon_light` | POST | `{"repeat": 1, "data": [[1000, 255, 0, 0], [1000, 0, 255, 0], [1000, 0, 0, 255], [0, 0, 0, 0]]}` |
| `192.168.178.57/things/bit_block/actions/head_light` | POST | `{"repeat": 1, "data": [[1000, 255, 0, 0], [1000, 0, 255, 0], [1000, 0, 0, 255], [0, 0, 0, 0]]}` |