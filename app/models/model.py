class Model(dict):
    __getattr__ = dict.get
    __delattr__ = dict.__delattr__
    __setattr__ = dict.__setattr__

    def save(self):
        if not self._id:
            self.collection.insert_one(self)
        else:
            self.collection.replace_one({"_id": self._id}, self)

    def reload(self):
        if self._id:
            self.update(self.collection.find_one({"_id": self._id}))

    def remove(self):
        if self._id:
            self.collection.delete_one({"_id": self._id})
            self.clear()

    def find(self, filters: dict):
        self.update(self.collection.find_one(filters))
