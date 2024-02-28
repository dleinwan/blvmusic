# Segmentation Functions

from music21 import *
from music21.converter.subConverters import ConverterMusicXML
import os
import subprocess

class Segmentor:
    def __init__(self, midi_file_path):
        # prepare midi for manipulation
        self.midi_path = midi_file_path
        midi = converter.parse(self.midi_path)
        self.notes = midi.flat.notes
        
        # create folder for song if it doesn't already exist
        #   ~ folder will be named the same name as input file name
        self.output_folder_name = self.midi_path.split('.')[0]
        if not os.path.exists(self.output_folder_name):
            os.makedirs(self.output_folder_name)
            print(f"Folder '{self.output_folder_name}' created.")
        else:
            print(f"Folder '{self.output_folder_name}' already exists.")
        self.output_folder_path = "./" + self.output_folder_name

    def segment(self, segment_length):
        self.sections = []
        for i in range(0, len(self.notes), segment_length):
            section = self.notes[i:i+segment_length]
            # add the below line if you don't want to include remainder section
            # if len(section) == section_length:
            self.sections.append(section)
    
    def create_midi_from_notes(self, section):
        midi_stream = stream.Stream()
        for element in section:
            if isinstance(element, note.Note):
                midi_stream.append(element)
            elif isinstance(element, note.Chord):
                midi_stream.append(element)
        return midi_stream
    
    def save_midi(self, midi_stream, output_file):
        output_path = os.path.join(self.output_folder_path, output_file)
        midi_stream.write('midi', fp=output_path)
    
    # Create MIDI streams for each section and save them as .mid files
    def save_segments_as_midi(self):
        for i, section in enumerate(self.sections):
            midi_stream = self.create_midi_from_notes(section)
            output_file = f"section_{i+1}.mid"
            self.save_midi(midi_stream, output_file)
            print(f"Section {i+1} saved as {os.path.join(self.output_folder_path, output_file)}")
            midi_stream.show()

    def create_folder(self, file_path):
        output_folder_name = file_path.split('.')[0]
        if not os.path.exists(output_folder_name):
            os.makedirs(output_folder_name)
            print(f"Folder '{output_folder_name}' created.")
        else:
            print(f"Folder '{output_folder_name}' already exists.")
        output_folder_path = "./" + output_folder_name
        return output_folder_name, output_folder_path

    def convert_midi_to_wav(midi_file):
        file_name, folder_path = self.create_folder(midi_file)
        # Construct the output file path by replacing the MIDI extension with WAV extension
        wav_file = os.path.splitext(os.path.basename(midi_file))[0] + ".wav"
        output_file = os.path.join(file_name, wav_file)
        
        # Convert MIDI to WAV using fluidsynth
        subprocess.call(["fluidsynth", "-ni", "/path/to/soundfont.sf2", midi_file, "-F", output_file])

    def convert_folder_of_midi_to_wav(self, folder_path):
        # Iterate through MIDI files in the folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if file_name.lower().endswith('.mid') or file_name.lower().endswith('.midi'):
                # Convert MIDI file to WAV
                self.convert_midi_to_wav(file_path)

    # not needed anymore
    def parse_midi(self):
        midi = converter.parse(self.midi_path)
        notes_to_parse = midi.flat.notes
        return notes_to_parse
    
    # not needed anymore
    def create_folder(self, file_path):
        output_folder_name = file_path.split('.')[0]
        if not os.path.exists(output_folder_name):
            os.makedirs(output_folder_name)
            print(f"Folder '{output_folder_name}' created.")
        else:
            print(f"Folder '{output_folder_name}' already exists.")
        output_folder_path = "./" + output_folder_name
        return output_folder_name, output_folder_path
