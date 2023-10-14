class Item:
    def __init__(self, key, content):
        self.key = key
        self.content = content

    def __str__(self):
        return '{}, {}'.format(self.key, self.content)