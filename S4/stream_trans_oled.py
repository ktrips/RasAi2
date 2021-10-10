#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the streaming API.

NOTE: This module requires the additional dependency `pyaudio`. To install
using pip:

    pip install pyaudio

Example usage:
    python transcribe_streaming_mic.py
"""

# [START speech_transcribe_streaming_mic]
from __future__ import division

import time
from grove.i2c import Bus

_COMMAND_MODE = 0x80
_DATA_MODE = 0x40
_NORMAL_DISPLAY = 0xA6

_DISPLAY_OFF = 0xAE
_DISPLAY_ON = 0xAF
_INVERSE_DISPLAY = 0xA7
_SET_BRIGHTNESS = 0x81


BasicFont = [[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x00, 0x5F, 0x00, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x00, 0x07, 0x00, 0x07, 0x00, 0x00, 0x00],
             [0x00, 0x14, 0x7F, 0x14, 0x7F, 0x14, 0x00, 0x00],
             [0x00, 0x24, 0x2A, 0x7F, 0x2A, 0x12, 0x00, 0x00],
             [0x00, 0x23, 0x13, 0x08, 0x64, 0x62, 0x00, 0x00],
             [0x00, 0x36, 0x49, 0x55, 0x22, 0x50, 0x00, 0x00],
             [0x00, 0x00, 0x05, 0x03, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x1C, 0x22, 0x41, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x41, 0x22, 0x1C, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x08, 0x2A, 0x1C, 0x2A, 0x08, 0x00, 0x00],
             [0x00, 0x08, 0x08, 0x3E, 0x08, 0x08, 0x00, 0x00],
             [0x00, 0xA0, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x08, 0x08, 0x08, 0x08, 0x08, 0x00, 0x00],
             [0x00, 0x60, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x20, 0x10, 0x08, 0x04, 0x02, 0x00, 0x00],
             [0x00, 0x3E, 0x51, 0x49, 0x45, 0x3E, 0x00, 0x00],
             [0x00, 0x00, 0x42, 0x7F, 0x40, 0x00, 0x00, 0x00],
             [0x00, 0x62, 0x51, 0x49, 0x49, 0x46, 0x00, 0x00],
             [0x00, 0x22, 0x41, 0x49, 0x49, 0x36, 0x00, 0x00],
             [0x00, 0x18, 0x14, 0x12, 0x7F, 0x10, 0x00, 0x00],
             [0x00, 0x27, 0x45, 0x45, 0x45, 0x39, 0x00, 0x00],
             [0x00, 0x3C, 0x4A, 0x49, 0x49, 0x30, 0x00, 0x00],
             [0x00, 0x01, 0x71, 0x09, 0x05, 0x03, 0x00, 0x00],
             [0x00, 0x36, 0x49, 0x49, 0x49, 0x36, 0x00, 0x00],
             [0x00, 0x06, 0x49, 0x49, 0x29, 0x1E, 0x00, 0x00],
             [0x00, 0x00, 0x36, 0x36, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x00, 0xAC, 0x6C, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x08, 0x14, 0x22, 0x41, 0x00, 0x00, 0x00],
             [0x00, 0x14, 0x14, 0x14, 0x14, 0x14, 0x00, 0x00],
             [0x00, 0x41, 0x22, 0x14, 0x08, 0x00, 0x00, 0x00],
             [0x00, 0x02, 0x01, 0x51, 0x09, 0x06, 0x00, 0x00],
             [0x00, 0x32, 0x49, 0x79, 0x41, 0x3E, 0x00, 0x00],
             [0x00, 0x7E, 0x09, 0x09, 0x09, 0x7E, 0x00, 0x00],
             [0x00, 0x7F, 0x49, 0x49, 0x49, 0x36, 0x00, 0x00],
             [0x00, 0x3E, 0x41, 0x41, 0x41, 0x22, 0x00, 0x00],
             [0x00, 0x7F, 0x41, 0x41, 0x22, 0x1C, 0x00, 0x00],
             [0x00, 0x7F, 0x49, 0x49, 0x49, 0x41, 0x00, 0x00],
             [0x00, 0x7F, 0x09, 0x09, 0x09, 0x01, 0x00, 0x00],
             [0x00, 0x3E, 0x41, 0x41, 0x51, 0x72, 0x00, 0x00],
             [0x00, 0x7F, 0x08, 0x08, 0x08, 0x7F, 0x00, 0x00],
             [0x00, 0x41, 0x7F, 0x41, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x20, 0x40, 0x41, 0x3F, 0x01, 0x00, 0x00],
             [0x00, 0x7F, 0x08, 0x14, 0x22, 0x41, 0x00, 0x00],
             [0x00, 0x7F, 0x40, 0x40, 0x40, 0x40, 0x00, 0x00],
             [0x00, 0x7F, 0x02, 0x0C, 0x02, 0x7F, 0x00, 0x00],
             [0x00, 0x7F, 0x04, 0x08, 0x10, 0x7F, 0x00, 0x00],
             [0x00, 0x3E, 0x41, 0x41, 0x41, 0x3E, 0x00, 0x00],
             [0x00, 0x7F, 0x09, 0x09, 0x09, 0x06, 0x00, 0x00],
             [0x00, 0x3E, 0x41, 0x51, 0x21, 0x5E, 0x00, 0x00],
             [0x00, 0x7F, 0x09, 0x19, 0x29, 0x46, 0x00, 0x00],
             [0x00, 0x26, 0x49, 0x49, 0x49, 0x32, 0x00, 0x00],
             [0x00, 0x01, 0x01, 0x7F, 0x01, 0x01, 0x00, 0x00],
             [0x00, 0x3F, 0x40, 0x40, 0x40, 0x3F, 0x00, 0x00],
             [0x00, 0x1F, 0x20, 0x40, 0x20, 0x1F, 0x00, 0x00],
             [0x00, 0x3F, 0x40, 0x38, 0x40, 0x3F, 0x00, 0x00],
             [0x00, 0x63, 0x14, 0x08, 0x14, 0x63, 0x00, 0x00],
             [0x00, 0x03, 0x04, 0x78, 0x04, 0x03, 0x00, 0x00],
             [0x00, 0x61, 0x51, 0x49, 0x45, 0x43, 0x00, 0x00],
             [0x00, 0x7F, 0x41, 0x41, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x02, 0x04, 0x08, 0x10, 0x20, 0x00, 0x00],
             [0x00, 0x41, 0x41, 0x7F, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x04, 0x02, 0x01, 0x02, 0x04, 0x00, 0x00],
             [0x00, 0x80, 0x80, 0x80, 0x80, 0x80, 0x00, 0x00],
             [0x00, 0x01, 0x02, 0x04, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x20, 0x54, 0x54, 0x54, 0x78, 0x00, 0x00],
             [0x00, 0x7F, 0x48, 0x44, 0x44, 0x38, 0x00, 0x00],
             [0x00, 0x38, 0x44, 0x44, 0x28, 0x00, 0x00, 0x00],
             [0x00, 0x38, 0x44, 0x44, 0x48, 0x7F, 0x00, 0x00],
             [0x00, 0x38, 0x54, 0x54, 0x54, 0x18, 0x00, 0x00],
             [0x00, 0x08, 0x7E, 0x09, 0x02, 0x00, 0x00, 0x00],
             [0x00, 0x18, 0xA4, 0xA4, 0xA4, 0x7C, 0x00, 0x00],
             [0x00, 0x7F, 0x08, 0x04, 0x04, 0x78, 0x00, 0x00],
             [0x00, 0x00, 0x7D, 0x00, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x80, 0x84, 0x7D, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x7F, 0x10, 0x28, 0x44, 0x00, 0x00, 0x00],
             [0x00, 0x41, 0x7F, 0x40, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x7C, 0x04, 0x18, 0x04, 0x78, 0x00, 0x00],
             [0x00, 0x7C, 0x08, 0x04, 0x7C, 0x00, 0x00, 0x00],
             [0x00, 0x38, 0x44, 0x44, 0x38, 0x00, 0x00, 0x00],
             [0x00, 0xFC, 0x24, 0x24, 0x18, 0x00, 0x00, 0x00],
             [0x00, 0x18, 0x24, 0x24, 0xFC, 0x00, 0x00, 0x00],
             [0x00, 0x00, 0x7C, 0x08, 0x04, 0x00, 0x00, 0x00],
             [0x00, 0x48, 0x54, 0x54, 0x24, 0x00, 0x00, 0x00],
             [0x00, 0x04, 0x7F, 0x44, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x3C, 0x40, 0x40, 0x7C, 0x00, 0x00, 0x00],
             [0x00, 0x1C, 0x20, 0x40, 0x20, 0x1C, 0x00, 0x00],
             [0x00, 0x3C, 0x40, 0x30, 0x40, 0x3C, 0x00, 0x00],
             [0x00, 0x44, 0x28, 0x10, 0x28, 0x44, 0x00, 0x00],
             [0x00, 0x1C, 0xA0, 0xA0, 0x7C, 0x00, 0x00, 0x00],
             [0x00, 0x44, 0x64, 0x54, 0x4C, 0x44, 0x00, 0x00],
             [0x00, 0x08, 0x36, 0x41, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x00, 0x7F, 0x00, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x41, 0x36, 0x08, 0x00, 0x00, 0x00, 0x00],
             [0x00, 0x02, 0x01, 0x01, 0x02, 0x01, 0x00, 0x00],
             [0x00, 0x02, 0x05, 0x05, 0x02, 0x00, 0x00, 0x00]]


class GroveOledDisplay128x64(object):
    HORIZONTAL = 0x00
    VERTICAL = 0x01
    PAGE = 0x02

    def __init__(self, bus=None, address=0x3C):
        self.bus = Bus(bus)
        self.address = address

        self.off()
        self.inverse = False
        self.mode = self.HORIZONTAL

        self.clear()
        self.on()

    def on(self):
        self.send_command(_DISPLAY_ON)

    def off(self):
        self.send_command(_DISPLAY_OFF)

    def send_command(self, command):
        self.bus.write_byte_data(self.address, _COMMAND_MODE, command)

    def send_data(self, data):
        self.bus.write_byte_data(self.address, _DATA_MODE, data)

    def send_commands(self, commands):
        for c in commands:
            self.send_command(c)

    def clear(self):
        self.off()
        for i in range(8):
            self.set_cursor(i, 0)
            self.puts(' ' * 16)

        self.on()
        self.set_cursor(0, 0)

    @property
    def inverse(self):
        return self._inverse

    @inverse.setter
    def inverse(self, enable):
        self.send_command(_INVERSE_DISPLAY if enable else _NORMAL_DISPLAY)
        self._inverse = enable

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self.send_command(0x20)
        self.send_command(mode)
        self._mode = mode

    def set_cursor(self, row, column):
        self.send_command(0xB0 + row)
        self.send_command(0x00 + (8*column & 0x0F))
        self.send_command(0x10 + ((8*column>>4)&0x0F))

    def putc(self, c):
        C_add = ord(c)
        if C_add < 32 or C_add > 127:     # Ignore non-printable ASCII characters
            c = ' '
            C_add = ord(c)

        for i in range(0, 8):
            self.send_data(BasicFont[C_add-32][i])

    def puts(self, text):
        for c in text:
            self.putc(c)

    def show_image(self, image):
        from PIL import Image
        import numpy as np
        
        im = Image.open(image)

        bw = im.convert('1')
        pixels = np.array(bw.getdata())
        page_size = 128 * 8

        self.set_cursor(0, 0)
        for page in range(8):
            start = page_size * page
            end = start + page_size

            for i in range(start, start + 128):
                data = np.packbits(pixels[i:end:128][::-1])[0]
                self.send_data(data)


import re
import sys

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue

from google.cloud import translate
origin_lang = 'ja-JP'
trans_lang  = 'en-US'
def translate_text(text, trans_lang):
    if trans_lang == '':
        return text
    else:
      target_lang = trans_lang.split("-")[0]
      translate_client = translate.Client()
      result = translate_client.translate(text, target_language=target_lang)
      return result['translatedText']

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break

            num_chars_printed = 0


def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = origin_lang #'en-US'  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.

        display = GroveOledDisplay128x64()
        display.set_cursor(0, 0)

        listen_print_loop('Origin: ' + responses)
        trans_res = translate_text(responses, trans_lang)
        listen_print_loop('Trans: ' + trans_res)

        display.puts('Trans: ' + trans_res)

if __name__ == '__main__':
    main()
# [END speech_transcribe_streaming_mic]
