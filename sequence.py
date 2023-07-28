class Sequence:
    def __init__(self):
        self.pictographs = []

    def add_pictograph(self, pictograph):
        self.pictographs.append(pictograph)

    def get_pictograph(self, index):
        return self.pictographs[index]

    def update_pictograph(self, index, new_pictograph):
        self.pictographs[index] = new_pictograph

    def display(self):
        for i, pictograph in enumerate(self.pictographs):
            print(f"Pictograph {i}: {pictograph}")
