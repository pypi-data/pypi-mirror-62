# THIS FILE IS AUTO-GENERATED. DO NOT EDIT

class ModeldbAddExperimentTag(dict):
  def __init__(self, id=None, tag=None):
    self.id = id
    self.tag = tag

  def __setattr__(self, name, value):
    self[name] = value

  def __delattr__(self, name):
    del self[name]

  def __getattr__(self, name):
    if name in self:
      return self[name]
    else:
      raise AttributeError
