# hurray for Python, because of http://bugs.python.org/issue5509 we need to make sure that these end up in __main__
# hence we import them in the correct way in update.py, so that historical/data.py can call things the way we intend them...

class env_with_proof:
  def __init__(self, name, type, label, tag, b, e, text, bp, ep, proof):
    self.name = name
    self.type = type
    self.label = label
    self.tag = tag
    self.b = b
    self.e = e
    self.text = text
    self.bp = bp
    self.ep = ep
    self.proof = proof

class env_without_proof:
  def __init__(self, name, type, label, tag, b, e, text):
    self.name = name
    self.type = type
    self.label = label
    self.tag = tag
    self.b = b
    self.e = e
    self.text = text

class env_history:
  def __init__(self, commit, env, commits, envs):
    self.commit = commit
    self.env = env
    self.commits = commits
    self.envs = envs

class history:
  def __init__(self, commit, env_histories, commits):
    self.commit = commit
    self.env_histories = env_histories
    self.commits = commits
