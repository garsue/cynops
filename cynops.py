#!/usr/bin/python
# vim: fileencoding=utf-8


class Relation(object):
    """Relation class based on relational model"""
    def __init__(self, head):
        """Instantiate Relation object. Argument as hedding is frozenset"""
        self.head = head
        self.body = set()
        self._protoruple = {}.fromkeys(head)

    def add(self, ruple):
        """Add ruple as dictionary"""
        for attr in self._protoruple:
            self._protoruple[attr] = ruple[attr]
        self.body.add(frozenset(self._protoruple.items()))

    def __eq__(self, other):
        result = []
        result.append(self.head == other.head)
        for self_ruple in (dict(ruple) for ruple in self.body):
            for other_ruple in (dict(ruple) for ruple in other.body):
                if self_ruple == other_ruple:
                    result.append(True)
        return all(result)

    def __str__(self):
        return str(self.body)

    def display(self):
        result = '\t'.join(self.head) + '\n' + '-' * 70 + '\n'
        for ruple in (dict(ruple) for ruple in self.body):
            for attr in ruple:
                result += str(ruple[attr]) + '\t'
            else:
                result += '\n'
        print result

    def restrict(self, target):
        """Return restriction. Argument is dictionary."""
        result = Relation(self.head)
        for ruple in (dict(ruple) for ruple in self.body):
            for attr in target:
                if ruple[attr] == target[attr]:
                    result.add(ruple)
        return result

    def project(self, target):
        """Return projection. Argument is frozenset."""
        result = Relation(target)
        result_ruple = {}
        for ruple in (dict(ruple) for ruple in self.body):
            for attr in result.head:
                result_ruple[attr] = ruple[attr]
            result.add(result_ruple)
        return result

    def join(self, other):
        """Return join. Argument is Relation"""
        result = Relation(self.head | other.head)
        result_ruple = {}
        inter_attrs = self.head & other.head
        for ruple1 in (dict(ruple1) for ruple1 in self.body):
            result_ruple.update(ruple1)
            for ruple2 in (dict(ruple2) for ruple2 in other.body):
                if all(ruple1[attr] == ruple2[attr] for attr in inter_attrs):
                    result_ruple.update(ruple2)
                    result.add(result_ruple)
        return result

    def union(self, other):
        """Return union. Argument is type-compatible Relation."""
        if self.head != other.head:
            return None
        result = Relation(self.head)
        result.body.update(self.body | other.body)
        return result

    def difference(self, other):
        """Return difference. Argument is type-compatible Relation."""
        if self.head != other.head:
            return None
        result = Relation(self.head)
        result.body.update(self.body - other.body)
        return result

    def semijoin(self, other):
        return self.join(other).project(self.head)

    def rename(self, target):
        """Return renamed Relation. Argument is dictionary."""
        def new_head(target):
            for attr in self.head:
                if attr in target:
                    yield target[attr]
                else:
                    yield attr
        head = frozenset(new_head(target))
        result = Relation(head)
        result_ruple = {}
        for ruple in (dict(ruple) for ruple in self.body):
            for attr in self.head:
                if attr in target:
                    result_ruple[target[attr]] = ruple[attr]
                else:
                    result_ruple[attr] = ruple[attr]
            result.add(result_ruple)
        return result

    def semidifference(self, other):
        return self.difference(self.semijoin(other))


if __name__ == '__main__':
    pass
