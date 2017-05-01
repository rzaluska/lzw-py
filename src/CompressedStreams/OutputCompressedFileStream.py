import struct
from io import BytesIO

from BinaryStreams.OutputBinaryFileStream import OutputBinaryFileStream


class OutputCompressedFileStream:
    def __init__(self, output_binary_file_stream: OutputBinaryFileStream):
        """

        :param output_binary_file_stream: wyjsciowy strumen bitowy do opakowania
        """
        self.output_binary_file_stream = output_binary_file_stream

    def compress(self, input_binary_file_object: BytesIO):
        """

        Kompresuje wskazany plik

        :param input_binary_file_object: plik do którego czytać dane do skompresowania
        """
        self.dict_size = 256
        self.dictionary = {chr(i): i for i in range(self.dict_size)}

        w = ""
        input_byte = input_binary_file_object.read(1)
        while input_byte != b'':
            input_byte = chr(struct.unpack("B", input_byte)[0])
            wc = w + input_byte
            if wc in self.dictionary:
                w = wc
            else:
                self.output_binary_file_stream.write(self.dictionary[w])
                # Add wc to the dictionary.
                self.dictionary[wc] = self.dict_size
                self.dict_size += 1
                w = input_byte

                if self.dict_size == 2 ** self.output_binary_file_stream.current_bits_size + 1:
                    self.output_binary_file_stream.increase_bit_code_size()

            input_byte = input_binary_file_object.read(1)

        # Output the code for w.
        if w:
            self.output_binary_file_stream.write(self.dictionary[w])
