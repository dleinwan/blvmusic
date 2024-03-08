# Segmentation Functions

from music21 import *
from music21.converter.subConverters import ConverterMusicXML
import os
import subprocess
import difflib
import itertools
import numpy

class Segmentor:
    def __init__(self, input_path_to_midi):
        self.name = os.path.splitext(os.path.basename(input_path_to_midi))[0]
        print(self.name)
        # prepare midi for manipulation
        self.path_to_midi = input_path_to_midi
        self.full_stream_midi = converter.parse(self.path_to_midi)
        self.midi = self.full_stream_midi.parts[0]
        self.notes = self.midi.flat.notes
        
        self.path_to_main_folder = None
        self.path_to_wav_output_folder = None
        self.path_to_segmented_midi_folder = None

        # create folder for song if it doesn't already exist
        #   ~ folder will be named the same name as input file name and located in /songs folder
        if not os.path.exists("songs/" + self.name):
            self.path_to_main_folder = "songs/" + self.name
            self.path_to_wav_output_folder = "songs/" + self.name + "/" + self.name + "_wav"
            self.path_to_segmented_midi_folder = "songs/" + self.name + "/" + self.name + "_midi"

            os.makedirs(self.path_to_main_folder)
            print(f"Folder '{self.name}' created in songs/ folder.")
            os.makedirs(self.path_to_wav_output_folder)
            print(f"Folder '{self.name}' created in songs/ folder.")
            os.makedirs(self.path_to_segmented_midi_folder)
            print(f"Folder '{self.name}' created in songs/ folder.")

        # for analyzing similarity
        self.best_num = None
        self.segments = None
        self.segments_similarity_score = None
        self.segment_similarity_dictionary = {}
        self.similarity_matrix = numpy.zeros((50, 50))
        
    def create_midi_from_notes(self, segment):
        midi_stream = stream.Stream()
        for element in segment:
            if isinstance(element, note.Note):
                midi_stream.append(element)
            elif isinstance(element, note.Chord):
                midi_stream.append(element)
        return midi_stream
    
    def show_midi(self):
        midi_stream = self.create_midi_from_notes(self.notes)
        midi_stream.show()
    
    def midi_to_note_name(self, midi_note):
        return note.Note(midi_note).nameWithOctave
        
    def convert_to_note_names(self):
        return [[self.midi_to_note_name(midi_note.pitch.midi) for midi_note in row] for row in self.segments]
    
    # Create MIDI streams for each segment and save them as .mid files
    def save_segments_as_midi(self):
        for i, segment in enumerate(self.segments):
            midi_stream = self.create_midi_from_notes(segment)
            segment_file_name = f"segment_{i+1}.mid"
            segment_full_path = self.path_to_segmented_midi_folder + "/" + segment_file_name
            midi_stream.write('midi', fp=segment_full_path)
            print(f"Segment {i+1} saved as {segment_full_path}")
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
        self.convert_to_note_names()
        self.save_segments_as_midi()
        
    def segment(self, segment_length, offset):
        self.segments = []
        for i in range((0+offset), len(self.notes), segment_length):
            segment = self.notes[i:i+segment_length]
            # add the below line if you don't want to include remainder segment
            # if len(segment) == segment_length:
            self.segments.append(segment)
        # self.show_segments_as_midi()
        self.convert_to_note_names()
        return self.segments

    def analyze_for_best_sectioning(self, iter_range):
        iter_range+=1
        self.best_num = 0
        similarity_matrix = numpy.zeros((iter_range, iter_range))
        for i in range(2, iter_range): # skip segments of 1 and start at 2
            # print(repeat.RepeatFinder(segments).getSimilarMeasureGroups())
            print("i: " + str(i))
            for k in range(0, i):
                segments = self.segment(i, offset=k)
                print("k: " + str(k))
                # for each previous segment, find similarity
                similarity = 0
                for j in range(1, len(segments)):
                    # print("j: " + str(j))
                    # if len(segments) >= i:
                    sm = difflib.SequenceMatcher(None, segments[j], segments[j-1])
                    similarity += sm.ratio()
                    # else:
                    #     print("For " + str(i) + " note segments, there are only " + str(len(segments)) + " segments.")
                dict_key = str(i) + "notes"
                self.segments_similarity_score = similarity / len(segments)
                self.segment_similarity_dictionary[dict_key] = similarity / len(segments)
                similarity_matrix[i][k] =  self.segments_similarity_score
                # print("Similarity for " + str(i) + " notes at a time:" + str(similarity))

        print("Similarity dictionary for " + self.path_to_midi + ": ")
        print(self.segment_similarity_dictionary)
        for row in similarity_matrix:
            for element in row:
                formatted = '{:.2f}'.format(element)
                print(formatted, end=" ")
            print()
        # print(similarity_matrix)

    def find_similar_note_groups(self):
        return repeat.RepeatFinder(self.midi).getSimilarMeasureGroups()

    def convert_midi_to_wav(self):
        for file in os.listdir(self.path_to_segmented_midi_folder):
            # Construct the output file path by replacing the MIDI extension with WAV extension
            wav_file = os.path.basename(file) + ".wav"
            temp_output_file_path = os.path.join(self.path_to_wav_output_folder, wav_file)
            print(temp_output_file_path)

            temp_full_midi_file_path = self.path_to_segmented_midi_folder + "/" + file
            print(temp_full_midi_file_path)
        
            # Convert MIDI to WAV using fluidsynth
            default_soundfont = "/Users/dani/opt/anaconda3/envs/cv_flute/share/soundfonts/default.sf2"
            default_soundfont_path = os.path.expanduser(default_soundfont)
            subprocess.call(["fluidsynth", "-F", default_soundfont, temp_full_midi_file_path, "-F", temp_output_file_path])

    # def create_folder(self, file_path, ext):
    #     output_folder_name = file_path.split('.')[0]
    #     if ext != None:
    #         output_folder_name = output_folder_name + ext
    #     if not os.path.exists(output_folder_name):
    #         os.makedirs(output_folder_name)
    #         print(f"Folder '{output_folder_name}' created.")
    #     else:
    #         print(f"Folder '{output_folder_name}' already exists.")
    #     output_folder_path = "./" + output_folder_name
    #     return output_folder_name, output_folder_path

    # def convert_folder_of_midi_to_wav(self, input_folder_path):
    #     # ext = "_wav"
    #     # output_folder_name, output_folder_path = self.create_folder(input_folder_path, ext)
    #     # Iterate through MIDI files in the folder
    #     for midi_file_name in os.listdir(input_folder_path):
    #         print("input folder path")
    #         print(input_folder_path)
    #         print("midi_file_name:")
    #         print(midi_file_name)
    #         full_midi_file_path = input_folder_path + "/" + midi_file_name
    #         print("full_midi_file_path:")
    #         print(full_midi_file_path)
    #         output_file_path = os.path.join(self.path_to_wav_output_folder, midi_file_name)
    #         if midi_file_name.lower().endswith('.mid') or midi_file_name.lower().endswith('.midi'):
    #             # Convert MIDI file to WAV
    #             self.convert_midi_to_wav(full_midi_file_path, midi_file_name, output_file_path, output_folder_name, output_folder_path)
    
    # not needed anymore
    # def parse_midi(self):
    #     midi = converter.parse(self.midi_path)
    #     notes_to_parse = midi.flat.notes
    #     return notes_to_parse
    
    # def create_folder(self, file_path):
    #     output_folder_name = file_path.split('.')[0]
    #     if not os.path.exists(output_folder_name):
    #         os.makedirs(output_folder_name)
    #         print(f"Folder '{output_folder_name}' created.")
    #     else:
    #         print(f"Folder '{output_folder_name}' already exists.")
    #     output_folder_path = "./" + output_folder_name
    #     return output_folder_name, output_folder_path
