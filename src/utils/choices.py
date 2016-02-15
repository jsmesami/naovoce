class Choices:
    """
    Encapsulates the choices definitions and conversions.
    Allows for using custom symbols for individual choices and stores
    choices as numbers in the database, instead of 1-letter strings.
    Original code @ https://github.com/tuttle/python-useful
    Example::

        class Payment(models.Model):
            STATUS = Choices(initial      = (100, _('Awaiting Payment')),
                             success      = (200, _('Paid OK')),
                             nok_failure  = (300, _('Payment Failed')))
            ...
            status = models.IntegerField(...,
                                         choices=STATUS.choices,
                                         default=STATUS.initial)

    Second choice can be referred as Payment.STATUS.success throughout
    the code, equals to 200.

    Two more convenience methods are included::

        Payment.STATUS.name_of(200) -> 'success'
        Payment.STATUS.text_of(200) -> 'Paid OK'
    """
    def __init__(self, **kwargs):
        defs = kwargs.items()

        self.__names = {choice[0]: name for name, choice in defs}
        self.__texts = {choice[0]: choice[1] for name, choice in defs}

        self.names = self.__names.values()
        self.texts = self.__texts.values()

        for name, choice in defs:
            setattr(self, name, choice[0])

        self.choices = sorted((choice for name, choice in defs), key=lambda t: t[0])

    def name_of(self, index):
        return self.__names.get(index)

    def text_of(self, index):
        return self.__texts.get(index)
