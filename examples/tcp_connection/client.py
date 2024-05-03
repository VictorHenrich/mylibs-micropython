from typing import Mapping, Any, Optional
from tempfile import TemporaryFile
import requests
import pyaudio
import speech_recognition as speech

from stream.client import StreamClient, AbstractStreamClientHandler


class StreamClientHandler(AbstractStreamClientHandler):
    def on_receive(self, data: bytes) -> None:
        print(f"\nCLIENT HANDLER DATA: {data}")


class BoardControlService:
    __WIT_IA_URL: str = "https://api.wit.ai"

    def __init__(self, host: str, port: int, wit_token: str) -> None:
        self.__stream_client: StreamClient = StreamClient(
            socket_handler_class=StreamClientHandler, host=host, port=port
        )

        self.__wit_token: str = wit_token

    def __get_understanding_wit(self, response: requests.Response) -> Mapping[str, Any]:
        response_data: Mapping[str, Any] = response.json()

        if not response_data.get("entities"):
            raise Exception("The type of pin was not identified by the text passed!")

        component_data: Mapping[str, Any] = response_data["entities"][
            "component:component"
        ][0]

        entities_data: Mapping[str, Any] = component_data["entities"]

        mode_data: Optional[Mapping[str, Any]] = None

        pin_data: Mapping[str, Any] = entities_data["wit$number:number"][0]

        connect_data: Mapping[str, Any] = response_data["entities"][
            "activate_action:activate_action"
        ][0]

        if entities_data and entities_data.get("mode:mode"):
            mode_data = entities_data["mode:mode"][0]

        pin_id: int = int(pin_data["value"])

        pin_value: bool = connect_data["value"].lower() == "connect"

        pin_mode: str = "in" if not mode_data else mode_data["value"]

        return {"id": pin_id, "value": pin_value, "mode": pin_mode}

    def __integrate_wit(self, text: str) -> Mapping[str, Any]:
        url: str = f"{BoardControlService.__WIT_IA_URL}/message"

        query_params: Mapping[str, Any] = {"q": text}

        headers: Mapping[str, Any] = {"Authorization": f"Bearer {self.__wit_token}"}

        response: requests.Response = requests.get(
            url, params=query_params, headers=headers
        )

        return self.__get_understanding_wit(response)

    # def execute(self) -> None:
    #     self.__stream_client.start()

    #     while True:
    #         audio: pyaudio.PyAudio = pyaudio.PyAudio()

    #         recognizer = speech.Recognizer()

    #         stream: pyaudio.Stream = audio.open(
    #             input=True,
    #             format=pyaudio.paInt16,
    #             channels=1,
    #             rate=44000,
    #             frames_per_buffer=1024
    #         )

    #         with TemporaryFile(suffix=".mp3") as buffer:
    #             try:
    #                 print("SPEAK: ")

    #                 while True:
    #                     chunck: bytes = stream.read(1024)

    #                     buffer.write(chunck)

    #             except KeyboardInterrupt:
    #                 print("...PROCESSING AUDIO...")

    #                 buffer.seek(0)

    #                 with speech.AudioFile(buffer.name) as data:
    #                     text: str = recognizer.recognize_google(data, language="pt-BR")

    #                     print(f"Transcribed text: {text}")

    #                     command_data: Mapping[str, Any] = self.__integrate_wit(text)

    #                     self.__stream_client.send_data(command_data)

    def execute(self) -> None:
        self.__stream_client.start()

        while True:
            recognizer = speech.Recognizer()

            with speech.Microphone() as source:
                print("SPEAK: ")

                audio_data: bytes = recognizer.listen(source)

                print("...PROCESSING...")

                text: str = recognizer.recognize_google(audio_data, language="pt-BR")

                print(f"Transcribed text: {text}")

                command_data: Mapping[str, Any] = self.__integrate_wit(text)

                self.__stream_client.send_data(command_data)
