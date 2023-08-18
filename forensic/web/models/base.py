from django.db import models


class DefaultToStringMixin:
    """ This class implements a default '__str__' method usable for most models

    It tries the attributes 'name', 'denotation' and 'denotation' for not empty names.
    If an 'inventory_number' attribute exists it is returned with the result of the above tries in brackets attached.
    If the resulting string would be not empty the first non empty name is returned.
    Otherwise, the superclasses '__str__' method is called.
    """

    def __str__(self):
        for attr in ["name", "denotation"]:
            base = str(getattr(self, attr, None) or "")
            if len(base) > 0:
                break
        if len(base) > 0:
            base = "(%s)" % base
        if getattr(self, "inventory_number", None) is not None:
            return "%s %s" % (str(getattr(self, "inventory_number")), base)
        if len(base) > 0:
            return base[1:-1]
        return super().__str__()


class MainModel(models.Model):
    state = models.CharField(max_length=30, null=False)

    class Meta:
        abstract = True

