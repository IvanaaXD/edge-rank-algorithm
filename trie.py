

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.posts = {}

    def __str__(self):
        pass


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, status_id):
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end = True
        current.posts.setdefault(status_id, 0)
        current.posts[status_id] += 1

    def search(self, words):
        results = {}
        for word in words:
            current = self.root
            for c in word:
                if c not in current.children:
                    break
                current = current.children[c]
            for status_id, value in current.posts.items():
                results.setdefault(status_id, 0)
                results[status_id] += value
        return results

    def pretraga(self, prefix):
        current = self.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]
        return self._traverse(current, prefix)

    def _traverse(self, node, prefix):
        results = []
        if node.is_end:
            results.append(prefix)
        for char, child in node.children.items():
            results.extend(self._traverse(child, prefix + char))
        return results
