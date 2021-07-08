from collections import UserList


class SliceableList(UserList):
    """
    UserList subclass that supports slicing.

    A instance of a UserList subclass will unfortunately always return a `list`
    when sliced instead of the subclass.

    This SliceableList when sliced will return a SliceableList, not a `list`.
    """

    def __getitem__(self, i):
        # UserList types seem to break if sliced
        # See https://stackoverflow.com/a/27552501
        res = self.data[i]
        return self.__class__(res) if isinstance(i, slice) else res

    def __repr__(self) -> str:
        items = ",\n".join([f"    {repr(i)}" for i in self])
        return f"{self.__class__.__name__}([\n{items}\n])"
