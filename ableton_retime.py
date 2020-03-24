import gzip
from xml.etree import ElementTree

if __name__ == '__main__':
    filename = 'example Project/example.als'
    target_filename = 'example Project/example retimed.als'
    current_bpm = 120
    target_bpm = 80
    scale_factor = target_bpm / current_bpm

    def scale_attrib(el, attrib):
        value = el.get(attrib)
        if value is not None:
            el.set(attrib, str(float(value) * scale_factor))

    with gzip.open(filename) as f:
        tree = ElementTree.parse(f)

    for midi_clip in tree.iter('MidiClip'):
        scale_attrib(midi_clip, 'Time')

        for current_start in midi_clip.iter('CurrentStart'):
            scale_attrib(current_start, 'Value')

        for current_end in midi_clip.iter('CurrentEnd'):
            scale_attrib(current_end, 'Value')

        for current_end in midi_clip.iter('LoopStart'):
            scale_attrib(current_end, 'Value')

        for current_end in midi_clip.iter('LoopEnd'):
            scale_attrib(current_end, 'Value')

        for current_end in midi_clip.iter('OutMarker'):
            scale_attrib(current_end, 'Value')

        for current_end in midi_clip.iter('HiddenLoopStart'):
            scale_attrib(current_end, 'Value')

        for current_end in midi_clip.iter('HiddenLoopEnd'):
            scale_attrib(current_end, 'Value')

        for midi_note in midi_clip.iter('MidiNoteEvent'):
            scale_attrib(midi_note, 'Time')
            scale_attrib(midi_note, 'Duration')

    for audio_clip in tree.iter('AudioClip'):
        scale_attrib(audio_clip, 'Time')

        for current_start in audio_clip.iter('CurrentStart'):
            scale_attrib(current_start, 'Value')

        for current_end in audio_clip.iter('CurrentEnd'):
            scale_attrib(current_end, 'Value')

    with gzip.open(target_filename, 'wb') as f:
        tree.write(f, encoding='UTF-8', xml_declaration=True)
