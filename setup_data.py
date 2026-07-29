import json
import os
from PIL import Image, ImageDraw, ImageFont

songs = [
    {"id": "song_1", "title": "Blinding Lights", "artist": "The Weeknd", "genre": "Pop", "cover": "blinding_lights.jpg", "danceability": 0.5, "energy": 0.7, "valence": 0.3},
    {"id": "song_2", "title": "Shape of You", "artist": "Ed Sheeran", "genre": "Pop", "cover": "shape_of_you.jpg", "danceability": 0.8, "energy": 0.6, "valence": 0.9},
    {"id": "song_3", "title": "Billie Jean", "artist": "Michael Jackson", "genre": "Pop", "cover": "billie_jean.jpg", "danceability": 0.9, "energy": 0.6, "valence": 0.8},
    {"id": "song_4", "title": "Someone Like You", "artist": "Adele", "genre": "Ballad", "cover": "someone_like_you.jpg", "danceability": 0.3, "energy": 0.2, "valence": 0.1},
    {"id": "song_5", "title": "Lose Yourself", "artist": "Eminem", "genre": "Hip-Hop", "cover": "lose_yourself.jpg", "danceability": 0.7, "energy": 0.9, "valence": 0.4},
    {"id": "song_6", "title": "Smells Like Teen Spirit", "artist": "Nirvana", "genre": "Grunge", "cover": "smells_like_teen_spirit.jpg", "danceability": 0.5, "energy": 0.9, "valence": 0.7},
    {"id": "song_7", "title": "Rolling in the Deep", "artist": "Adele", "genre": "Pop", "cover": "rolling_in_the_deep.jpg", "danceability": 0.7, "energy": 0.7, "valence": 0.5},
    {"id": "song_8", "title": "Happier", "artist": "Marshmello", "genre": "Electronic", "cover": "happier.jpg", "danceability": 0.7, "energy": 0.8, "valence": 0.6},
    {"id": "song_9", "title": "Bohemian Rhapsody", "artist": "Queen", "genre": "Rock", "cover": "bohemian_rhapsody.jpg", "danceability": 0.4, "energy": 0.4, "valence": 0.2},
    {"id": "song_10", "title": "Stairway to Heaven", "artist": "Led Zeppelin", "genre": "Rock", "cover": "stairway_to_heaven.jpg", "danceability": 0.3, "energy": 0.3, "valence": 0.2},
    {"id": "song_11", "title": "Hotel California", "artist": "Eagles", "genre": "Rock", "cover": "hotel_california.jpg", "danceability": 0.6, "energy": 0.5, "valence": 0.6},
    {"id": "song_12", "title": "Uptown Funk", "artist": "Bruno Mars", "genre": "Funk", "cover": "uptown_funk.jpg", "danceability": 0.8, "energy": 0.9, "valence": 0.9},
    {"id": "song_13", "title": "Perfect", "artist": "Ed Sheeran", "genre": "Ballad", "cover": "perfect.jpg", "danceability": 0.6, "energy": 0.4, "valence": 0.4},
    {"id": "song_14", "title": "All of Me", "artist": "John Legend", "genre": "Ballad", "cover": "all_of_me.jpg", "danceability": 0.4, "energy": 0.3, "valence": 0.3},
    {"id": "song_15", "title": "Thinking Out Loud", "artist": "Ed Sheeran", "genre": "Pop", "cover": "thinking_out_loud.jpg", "danceability": 0.6, "energy": 0.4, "valence": 0.5},
    {"id": "song_16", "title": "Stay", "artist": "The Kid LAROI", "genre": "Pop", "cover": "stay.jpg", "danceability": 0.6, "energy": 0.7, "valence": 0.5},
    {"id": "song_17", "title": "Sunflower", "artist": "Post Malone", "genre": "Hip-Hop", "cover": "sunflower.jpg", "danceability": 0.7, "energy": 0.5, "valence": 0.9}
]

os.makedirs('static/images', exist_ok=True)

with open('songs.json', 'w') as f:
    json.dump(songs, f, indent=4)

colors = [
    (255, 99, 71), (138, 43, 226), (46, 139, 87), (210, 105, 30), 
    (100, 149, 237), (220, 20, 60), (0, 206, 209), (255, 140, 0),
    (139, 0, 139), (85, 107, 47), (153, 50, 204), (143, 188, 143),
    (72, 61, 139), (0, 250, 154), (199, 21, 133), (25, 25, 112), (218, 112, 214)
]

for i, song in enumerate(songs):
    img = Image.new('RGB', (300, 300), color=colors[i % len(colors)])
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        font = ImageFont.load_default()
    
    # Just draw the initials or a simple label
    text = "".join([w[0] for w in song["title"].split()])
    
    # Better text rendering if possible
    draw.text((100, 100), text, fill=(255, 255, 255), font=font)
    img.save(os.path.join('static/images', song["cover"]))

print("Generated songs.json and cover images.")
