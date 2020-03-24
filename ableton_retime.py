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

    print(f'Opened {filename}')

    for clip in tree.iter():
        if clip.tag in ('MidiClip', 'AudioClip'):
            name = clip.find('Name').get('Value')
            is_warped = clip.find('IsWarped').get('Value') == 'true'

            print(f'Found {"warped" if is_warped else "unwarped"} {clip.tag} "{name}"')

            scale_attrib(clip, 'Time')
            scale_attrib(clip.find('CurrentStart'), 'Value')
            scale_attrib(clip.find('CurrentEnd'), 'Value')

            for midi_note in clip.findall('./Notes//MidiNoteEvent'):
                scale_attrib(midi_note, 'Time')
                scale_attrib(midi_note, 'Duration')

            for warp_marker in clip.findall('./WarpMarkers/WarpMarker'):
                scale_attrib(warp_marker, 'BeatTime')

            if is_warped:
                scale_attrib(clip.find('./Loop/LoopStart'), 'Value')
                scale_attrib(clip.find('./Loop/LoopEnd'), 'Value')
                scale_attrib(clip.find('./Loop/OutMarker'), 'Value')
                scale_attrib(clip.find('./Loop/HiddenLoopStart'), 'Value')
                scale_attrib(clip.find('./Loop/HiddenLoopEnd'), 'Value')

    with gzip.open(target_filename, 'wb') as f:
        tree.write(f, encoding='UTF-8', xml_declaration=True)

    print(f'Saved to {target_filename}')
