class Section:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    def tuple_str(tup):
        return str(tup).replace("'", "")

    def __str__(self):
        return '%s (%s) on %s at %s' % (getattr(self, 'name'), getattr(self, 'crn'),
                                        getattr(self, 'days'),
                                        Section.tuple_str((getattr(self, 'start_time'), getattr(self, 'end_time'))))

    def __eq__(self, other):
        if isinstance(other, Section):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self == other