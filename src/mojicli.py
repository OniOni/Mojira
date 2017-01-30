import argparse
import json

class Moji(object):

    def __init__(self, json_file: str):
        self.file = json_file

    def load(self) -> dict:
        with open(self.file) as fd:
            return json.load(fd)

    @property
    def moji(self) -> None:
        if not hasattr(self, '_moji'):
            self._moji = self.load()

        return self._moji

    def search(self, keyword) -> list:
        return [
            {'name': key, 'moji': res['char']}
            for key, res in self.moji.items()
            if keyword in res['keywords']
        ]

if __name__ == "__main__":
    m = Moji('emojis.json')

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('search', type=str)


    args = parser.parse_args()
    print("Searching for", args.search)
    res = m.search(args.search)
    print("\n".join("{}: {}".format(el['name'], el['moji']) for el in res))
