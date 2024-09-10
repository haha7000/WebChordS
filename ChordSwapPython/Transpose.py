def transpose_chord(chord, half_steps):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    root_note = chord[0]
    root_index = notes.index(root_note)
    
    new_index = (root_index + half_steps) % 12
    return notes[new_index] + chord[1:]

