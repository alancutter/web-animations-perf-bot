class Build(object):
  def __init__(self, datetime, commit):
    self.datetime = datetime
    self.commit = commit

  def __repr__(self):
    return 'Build(datetime=%s, commit=%s)' % (repr(self.datetime), repr(self.commit))

  def tuple(self):
    return (self.datetime, self.commit)