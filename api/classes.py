class Class:

    def __init__(self, crn, name, opening, days, time, semester):
        self.crn = crn
        self.name = name
        self.opening = opening
        self.days = days
        self.time = time
        self.semester = semester

    def days_str(self):
        return str(self.days).replace("'", "")

    def __str__(self):
        return '%s (%s) on %s at %s' % (self.name, self.crn, self.days_str(), self.time)
