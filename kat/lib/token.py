class Token:
    def __init__(self, kind, substance=None, line_nr=None, line=None):
        self.kind = kind
        self.line = line
        self.line_nr = line_nr
        self.substance = substance

    #  def __call__(self):
        #  return self.kind
