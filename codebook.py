# Codebook and Note classes
# CLASS Codebook contains self.codes which is a LIST of CLASS Notes which self populates with codes.csv 
# codes.csv contains note and fingering information, as well as enharmonic information, octave, etc. 

from matplotlib import pyplot as plt
import csv
import os
from scipy.io import wavfile
from pydub import AudioSegment


'''

Class Note
~ instantiated for each line of codes.csv by Codebook class (see below)

'''
class Note:

    def __init__(self, row):
        self.id = row['ID']
        self.name = row['name']
        self.pitchSharp = row['pitchSharp']
        self.pitchFlat = row['pitchFlat']
        self.octave = row['octave']
        self.homeKeys = row['homeKeys']
        self.thumb = row['thumb']
        self.leftPinky = row['leftPinky']
        self.rightPinky = row['rightPinky']
        self.init_fingering()
        self.init_audio()

    def init_fingering(self):

        self.fingering = ''

        if self.homeKeys != '0':
            self.fingering = self.homeKeys

        if self.thumb != 'n':
            self.fingering = self.fingering + self.thumb
        
        if self.leftPinky != 'n':
            self.fingering = self.fingering + self.leftPinky

        if self.rightPinky != 'n':
            self.fingering = self.fingering + self.rightPinky

    def init_audio(self):
        # start with sounding pitch audio
        sound_audio_path = "./clips/pitches/" + self.name + ".wav"
        sound_audio = AudioSegment.from_file(sound_audio_path, format="wav",
                                   frame_rate=44100, channels=1, sample_width=2)
        output_audio = AudioSegment.from_file(sound_audio_path, format="wav",
                                   frame_rate=44100, channels=1, sample_width=2)
        # sound + note name + fingering + sound
        # append note name
        note_name_audio_path = "./clips/names/" + self.name[0] + ".wav"
        # name_audio = AudioSegment.from_wav(note_name_audio_path)
        name_audio = AudioSegment.from_file(note_name_audio_path, format="wav",
                                frame_rate=44100, channels=1, sample_width=2)
        output_audio = output_audio.append(name_audio, crossfade=0)
        # append accidental 
        if self.name[1]=="s":
            sharp_audio_path = "./clips/names/sharp.wav"
            sharp_audio = AudioSegment.from_file(sharp_audio_path, format="wav",
                                   frame_rate=44100, channels=1, sample_width=2)
            output_audio = output_audio.append(sharp_audio, crossfade=0)
        elif self.name[1]=="f":
            flat_audio_path = "./clips/names/flat.wav"
            flat_audio = AudioSegment.from_file(flat_audio_path, format="wav",
                                   frame_rate=44100, channels=1, sample_width=2)
            output_audio = output_audio.append(flat_audio, crossfade=0)
        else:
            output_audio = output_audio
        # append octave
        octave_audio_path = "./clips/fingering_codes/" + self.octave + ".wav"
        octave_audio = AudioSegment.from_file(octave_audio_path, format="wav",
                                   frame_rate=44100, channels=1, sample_width=2)
        output_audio = output_audio.append(octave_audio, crossfade=0)
        # append fingering
        for element in self.fingering:
            fingering_audio_path = "./clips/fingering_codes/" + element + ".wav"
            fingering_audio = AudioSegment.from_file(fingering_audio_path, format="wav",
                                   frame_rate=44100, channels=1, sample_width=2)
            output_audio = output_audio.append(fingering_audio, crossfade=0)
        # append sounding pitch again
        output_audio = output_audio.append(sound_audio, crossfade=0)
        # export to output_audio folder
        output_audio_file_name = "./output_audio/" + self.name + ".wav"
        output_audio.export(output_audio_file_name, format="wav", bitrate=44100)

'''

Class Codebook
~ instantiated with codes.csv

'''
class Codebook:

    def __init__(self, file_path_to_csv):
        self.codes = []
        with open(file_path_to_csv, newline='') as csvfile:
            data = csv.DictReader(csvfile)
            for row in data:
                # print(', '.join(row))
                self.codes.append(Note(row))
                
    def print_all_notes(self):
        for item in self.codes:
            print(item.name)
    
    def find_note_by_id(self, id_num):
        for item in self.codes:
            if item.id == str(id_num):
                note = item
        return note

    def find_note_by_name(self, name_string):
        note = None

        for item in self.codes:
            if item.name == name_string:
                note = item

        if note == None:
            for item in self.codes:
                if (item.pitchSharp + item.octave) == name_string:
                    note = item
                if (item.pitchFlat + item.octave) == name_string:
                    note = item
        return note
    
    def find_note_by_pitchSharp(self, pitchSharp_string):
        for item in self.codes:
            if item.pitchSharp == pitchSharp_string:
                note = item
        return note
    
    def find_note_by_pitchFlat(self, pitchFlat_string):
        for item in self.codes:
            if item.pitchFlat == pitchFlat_string:
                note = item
        return note
    
    def find_note_by_fingering(self, fingering_string):
        for item in self.codes:
            if item.fingering == fingering_string:
                note = item
        return note
    
    # def stich_reference_audio(self, num_notes, param2, )