# Segmentation Functions

from music21 import *
from music21.converter.subConverters import ConverterMusicXML
import os
import subprocess
import difflib
import itertools

class Segmentor:
    def __init__(self, midi_file_path):
        self.best_num = 0
        self.segments = []

        # prepare midi for manipulation
        self.midi_path = midi_file_path
        self.midi = converter.parse(self.midi_path)
        self.notes = self.midi.flat.notes
        
        # create folder for song if it doesn't already exist
        #   ~ folder will be named the same name as input file name
        self.output_folder_name = self.midi_path.split('.')[0]
        if not os.path.exists(self.output_folder_name):
            os.makedirs(self.output_folder_name)
            print(f"Folder '{self.output_folder_name}' created.")
        else:
            print(f"Folder '{self.output_folder_name}' already exists.")
        self.output_folder_path = "./" + self.output_folder_name
    
    def create_midi_from_notes(self, segment):
        midi_stream = stream.Stream()
        for element in segment:
            if isinstance(element, note.Note):
                midi_stream.append(element)
            elif isinstance(element, note.Chord):
                midi_stream.append(element)
        return midi_stream
    
    def midi_to_note_name(self, midi_note):
        return note.Note(midi_note).nameWithOctave
        
    def convert_to_note_names(self):
        return [[self.midi_to_note_name(midi_note.pitch.midi) for midi_note in row] for row in self.segments]
    
    def save_midi(self, midi_stream, output_file):
        output_path = os.path.join(self.output_folder_path, output_file)
        midi_stream.write('midi', fp=output_path)
    
    # Create MIDI streams for each segment and save them as .mid files
    def save_segments_as_midi(self):
        for i, segment in enumerate(self.segments):
            midi_stream = self.create_midi_from_notes(segment)
            output_file = f"segment_{i+1}.mid"
            self.save_midi(midi_stream, output_file)
            print(f"Segment {i+1} saved as {os.path.join(self.output_folder_path, output_file)}")
            midi_stream.show()

    def show_segments_as_midi(self):
        for i, segment in enumerate(self.segments):
            midi_stream = self.create_midi_from_notes(segment)
            print(f"Segment {i+1} saved")
            midi_stream.show()

    def segment_and_save(self, segment_length):
        self.segments = []
        for i in range(0, len(self.notes), segment_length):
            segment = self.notes[i:i+segment_length]
            # add the below line if you don't want to include remainder segment
            # if len(segment) == segment_length:
            self.segments.append(segment)
        self.save_segments_as_midi()
        

    def segment(self, segment_length):
        self.segments = []
        for i in range(0, len(self.notes), segment_length):
            segment = self.notes[i:i+segment_length]
            # add the below line if you don't want to include remainder segment
            # if len(segment) == segment_length:
            self.segments.append(segment)
        # self.show_segments_as_midi()
        print(self.convert_to_note_names())
        return self.segments

    def analyze_for_best_sectioning(self, iter_range):
        iter_range+=1
        self.best_num = 0
        for i in range(1, iter_range):
            segments = self.segment(i)
            # print(repeat.RepeatFinder(segments).getSimilarMeasureGroups())
            # skip if first iteration since nothing to compare it to
            if i==1: 
                None
            else:
                # for each previous segment, find similarity
                similarity = 0
                for j in range(1, i):
                    sm = difflib.SequenceMatcher(None, segments[j], segments[j-1])
                    similarity += sm.ratio()
                similarity = similarity / j+1
                print("Similarity for " + str(i) + " notes at a time:" + str(similarity))





    def find_similar_note_groups(self):
        return repeat.RepeatFinder(self.midi).getSimilarMeasureGroups()

    def create_folder(self, file_path):
        output_folder_name = file_path.split('.')[0]
        if not os.path.exists(output_folder_name):
            os.makedirs(output_folder_name)
            print(f"Folder '{output_folder_name}' created.")
        else:
            print(f"Folder '{output_folder_name}' already exists.")
        output_folder_path = "./" + output_folder_name
        return output_folder_name, output_folder_path

    def convert_midi_to_wav(self, midi_file):
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

    def create_folder(self, file_path):
        output_folder_name = file_path.split('.')[0]
        if not os.path.exists(output_folder_name):
            os.makedirs(output_folder_name)
            print(f"Folder '{output_folder_name}' created.")
        else:
            print(f"Folder '{output_folder_name}' already exists.")
        output_folder_path = "./" + output_folder_name
        return output_folder_name, output_folder_path
    
    # not needed anymore
    def parse_midi(self):
        midi = converter.parse(self.midi_path)
        notes_to_parse = midi.flat.notes
        return notes_to_parse
