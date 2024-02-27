# Segmentation Functions

from music21 import *
from music21.converter.subConverters import ConverterMusicXML
import os
import subprocess

# music21 configuration stuff
# %config InlineBackend.figure_format = 'svg'
musescore_path = "/Applications/MuseScore 4.app/Contents/MacOS/mscore"
environment.set("musescoreDirectPNGPath", musescore_path)
environment.set("musicxmlPath", musescore_path)

def parse_midi(file_path):
    midi = converter.parse(file_path)
    notes_to_parse = midi.flat.notes
    return notes_to_parse

def split_into_sections(notes, section_length=3):
    sections = []
    for i in range(0, len(notes), section_length):
        section = notes[i:i+section_length]
        # if len(section) == section_length:
        sections.append(section)
    return sections

def create_midi_from_notes(notes):
    midi_stream = stream.Stream()
    for element in notes:
        if isinstance(element, note.Note):
            midi_stream.append(element)
        elif isinstance(element, note.Chord):
            midi_stream.append(element)
    return midi_stream

def save_midi(midi_stream, output_folder, output_file):
    output_path = os.path.join(output_folder, output_file)
    midi_stream.write('midi', fp=output_path)

def create_folder(file_path):
    output_folder_name = file_path.split('.')[0]
    if not os.path.exists(output_folder_name):
        os.makedirs(output_folder_name)
        print(f"Folder '{output_folder_name}' created.")
    else:
        print(f"Folder '{output_folder_name}' already exists.")
    return output_folder_name, os.path.basename(file_path)

def convert_midi_to_wav(midi_file, output_folder):
    # Construct the output file path by replacing the MIDI extension with WAV extension
    wav_file = os.path.splitext(os.path.basename(midi_file))[0] + ".wav"
    output_file = os.path.join(output_folder, wav_file)
    
    # Convert MIDI to WAV using fluidsynth
    subprocess.call(["fluidsynth", "-ni", "/path/to/soundfont.sf2", midi_file, "-F", output_file])

def convert_folder_of_midi_to_wav(folder_path, output_folder):
    """
    Converts all MIDI files in a folder to WAV files.
    
    Args:
        folder_path (str): The path to the folder containing MIDI files.
        output_folder (str): The path to the output folder.
    """
    # Iterate through MIDI files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_name.lower().endswith('.mid') or file_name.lower().endswith('.midi'):
            # Convert MIDI file to WAV
            convert_midi_to_wav(file_path, output_folder)
