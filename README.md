# ableton-retime
A python script for retiming Ableton Live projects.


This is useful in situations where you want to adjust the global BPM without affecting playback of the arrangement. For example, perhaps you recorded some midi or audio tracks freely, and now you want to adjust the BPM to match what you recorded. Or, perhaps you have a project that is technically in time, but you think it makes sense to halve or double the BPM, without actually changing the playback speed.

Unfortunately, there is not a simple way to achieve this within Ableton, as far as I'm aware. However, since Ableton projects are just compressed XML files, they can be manipulated fairly easily by scripts such as this.

The script retimes:
- Midi clips
- Audio clips (including those used as samples in instruments such as Simpler)
- Loop and warp markers
- Automation events

Some effects may still need manual adjustment, such as delays that are synced to the BPM.

## Example Usage
```
python ableton_retime.py --current-bpm 120 --target-bpm 80 input_project.als output_project.als
```
This reads input_project.als, scales it by 67% (80/120), and writes the result to output_project.als. This can be tried with the included example project.

Although the script performs the scaling, it does not currently modify the global BPM. Therefore, when you open the output project in Ableton, you should then manually set the BPM to match the target. The arrangement should then playback the same as before, even though the BPM has changed!

## Requirements
Tested with python3.7 with an Ableton 9 project.


Any testing / feedback is welcome.
