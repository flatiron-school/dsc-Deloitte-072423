from mrjob.job import MRJob
from mrjob.step import MRStep

class MRCountSongs(MRJob):
    
    def steps(self):
        return [
            MRStep(mapper=self.mapper),
            MRStep(reducer=self.reducer)
        ]
    
    # Each line in will be read as a key, value
    # Each line has no key, so we ignore it with `_`
    def mapper(self, _, song):
        # Each line is a tuple: (song_names, 1) 
        yield (song, 1)

    # Combine all tuples with the same key
    def reducer(self, key, values):
        # Key is the song name
        # Sum up values in the tuple to get total song plays
        yield (key, sum(values))
        
# Runs this if I call it via the terminal        
if __name__ == "__main__":
    MRCountSongs.run()