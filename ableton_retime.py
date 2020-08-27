import gzip
from xml.etree import ElementTree
import argparse


def ableton_retime(*, source_file, target_file, current_bpm, target_bpm):
    with gzip.open(source_file) as f:
        tree = ElementTree.parse(f)

    print(f'Opened project "{source_file}"')

    scale_factor = target_bpm / current_bpm
    print(f'Scale factor: {target_bpm} / {current_bpm} = {scale_factor * 100}%')

    count = 0

    def scale_attrib(el, attrib):
        nonlocal count
        if el is not None:
            value = el.get(attrib)
            if value is not None:
                value = float(value)
                if value != -63072000:
                    el.set(attrib, str(value * scale_factor))
                    count += 1

    for el in tree.iter():
        if el.tag in ('MidiClip', 'AudioClip'):
            clip = el
            is_warped = clip.find('IsWarped').get('Value') == 'true'

            scale_attrib(clip, 'Time')
            scale_attrib(clip.find('CurrentStart'), 'Value')
            scale_attrib(clip.find('CurrentEnd'), 'Value')

            if is_warped:
                scale_attrib(clip.find('./Loop/LoopStart'), 'Value')
                scale_attrib(clip.find('./Loop/LoopEnd'), 'Value')
                scale_attrib(clip.find('./Loop/OutMarker'), 'Value')
                scale_attrib(clip.find('./Loop/HiddenLoopStart'), 'Value')
                scale_attrib(clip.find('./Loop/HiddenLoopEnd'), 'Value')

        elif el.tag in ('MidiNoteEvent', 'FloatEvent', 'BoolEvent', 'EnumEvent'):
            event = el
            scale_attrib(event, 'Time')
            scale_attrib(event, 'Duration')

        elif el.tag == 'WarpMarker':
            marker = el
            scale_attrib(marker, 'BeatTime')

    print(f'Retimed {count} attributes')

    with gzip.open(target_file, 'wb') as f:
        tree.write(f, encoding='UTF-8', xml_declaration=True)

    print(f'Saved retimed project to "{target_file}"')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retime an Ableton Live project.')
    parser.add_argument('source_file', help='The path of the project to read.')
    parser.add_argument('target_file', help='The path at which to save the retimed project.')
    parser.add_argument('--current-bpm', type=float, required=True, help="The project's current bpm value.")
    parser.add_argument('--target-bpm', type=float, required=True, help='The target bpm value.')

    args = parser.parse_args()

    ableton_retime(
        source_file=args.source_file,
        target_file=args.target_file,
        current_bpm=args.current_bpm,
        target_bpm=args.target_bpm
    )
