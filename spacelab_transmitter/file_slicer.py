#
#  file_slicer.py
#
#  Copyright The SpaceLab-Transmitter Contributors.
#
#  This file is part of SpaceLab-Transmitter.
#
#  SpaceLab-Transmitter is free software; you can redistribute it
#  and/or modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  SpaceLab-Transmitter is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public
#  License along with SpaceLab-Transmitter; if not, see <http://www.gnu.org/licenses/>.
#
#

class FileSlicer:
    """A class for slicing files into integer lists with additional functionality."""
    
    def __init__(self, filename, chunk_size):
        self.filename = filename
        self.chunk_size = chunk_size
        self.chunks = []
    
    def slice_file(self):
        """Slice the file into chunks of integers."""
        self.chunks = []
        try:
            with open(self.filename, 'rb') as file:
                chunk_count = 0
                while True:
                    chunk_data = file.read(self.chunk_size)
                    if not chunk_data:
                        break
                    
                    int_list = list(chunk_data)
                    self.chunks.append(int_list)
                    chunk_count += 1
                
                return True
                
        except Exception as e:
            return False
    
    def get_chunk(self, index):
        """Get a specific chunk by index."""
        if 0 <= index < len(self.chunks):
            return self.chunks[index]
        return None
    
    def get_total_chunks(self):
        return len(self.chunks)

    def get_total_bytes(self):
        """Get total number of bytes processed."""
        return sum(len(chunk) for chunk in self.chunks)
    
    def find_byte_pattern(self, pattern):
        """Find a pattern (list of integers) in the chunks."""
        pattern = [int(b) for b in pattern]  # Ensure pattern is integers
        matches = []
        
        for chunk_idx, chunk in enumerate(self.chunks):
            for i in range(len(chunk) - len(pattern) + 1):
                if chunk[i:i+len(pattern)] == pattern:
                    matches.append((chunk_idx, i))
        
        return matches
    
    def reconstruct_file(self, output_filename):
        """Reconstruct the original file from chunks."""
        try:
            with open(output_filename, 'wb') as file:
                for chunk in self.chunks:
                    file.write(bytes(chunk))
            return True
        except Exception as e:
            return False
