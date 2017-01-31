import argparse
import json


class Mojira(object):

    def __init__(self, json_file: str) -> None:
        self.file = json_file

    def load(self) -> dict:
        with open(self.file) as fd:
            return json.load(fd)

    def items(self) -> list:
        return list(self.moji.items())

    @property
    def moji(self) -> dict:
        if not hasattr(self, '_moji'):
            self._moji = self.load()

        return self._moji

    def search(self, keyword: str) -> list:
        return [
            {'name': key, 'moji': res['char']}
            for key, res in self.items()
            if keyword in res['keywords']
        ]

    def filter(self, keyword: str):
        return MojiView(self, [k for k, v in self.items() if keyword in v['keywords']])


class MojiView(Mojira):

    def __init__(self, mojira: Mojira, keys: list) -> None:
        self.mojira = mojira
        self.keys = keys
        self._moji = mojira._moji

    def items(self) -> list:
        return [(key, self.moji[key]) for key in self.keys]


if __name__ == "__main__":
    m = Mojira('emojis.json')

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('search', type=str)


    args = parser.parse_args()
    print("Searching for", args.search)
    res = m.search(args.search)
    print("\n".join("{}: {}".format(el['name'], el['moji']) for el in res))
