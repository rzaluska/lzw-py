import struct
from io import BytesIO

from BinaryStreams.OutputBinaryFileStream import OutputBinaryFileStream
from CompressedStreams import CLEAR_TABLE, NEW_CODE_INDEX, INITIAL_DICTIONARY_SIZE


class OutputCompressedFileStream:
    def __init__(self, output_binary_file_stream: OutputBinaryFileStream, max_bits_size):
        """

        :param output_binary_file_stream: wyjsciowy strumen bitowy do opakowania
        """
        self.max_bits_size = max_bits_size
        self.output_binary_file_stream = output_binary_file_stream

    def compress(self, input_binary_file_object: BytesIO):
        """

        Kompresuje wskazany plik
        
        Wynik kompresji jest zapisywany w opakowanym strumieniu
        output_binary_file_stream

        :param input_binary_file_object: plik z którego czytać dane do skompresowania
        """
        self.clear_dictionary()
        bytes_sequence = b""
        self.validator = []
        while True:
            input_byte = input_binary_file_object.read(1)
            if input_byte == b"":
                break
            new_bytes_sequence = bytes_sequence + input_byte
            if new_bytes_sequence in self.dictionary:
                bytes_sequence = new_bytes_sequence
            else:
                self.validator.append(self.dictionary[bytes_sequence])
                self.output_binary_file_stream.write(self.dictionary[bytes_sequence])
                self.dictionary[new_bytes_sequence] = self.new_value_index
                self.new_value_index += 1
                bytes_sequence = input_byte

                if self.new_value_index + 1 == 2 ** self.max_bits_size:
                    self.output_binary_file_stream.write(CLEAR_TABLE)
                    self.validator.append(CLEAR_TABLE)
                    self.output_binary_file_stream.reset_bit_code_size()
                    self.clear_dictionary()

                if self.new_value_index == 2 ** self.output_binary_file_stream.current_bits_size:
                    self.output_binary_file_stream.increase_bit_code_size()

        if bytes_sequence:
            self.validator.append(self.dictionary[bytes_sequence])
            self.output_binary_file_stream.write(self.dictionary[bytes_sequence])

    def clear_dictionary(self):
        num_elements = INITIAL_DICTIONARY_SIZE
        self.dictionary = {bytes([i]): i for i in range(num_elements)}
        self.new_value_index = NEW_CODE_INDEX
