from django.forms import BaseForm


def apply_form_customizations(form):
    for element in ('label', 'help_text'):
        for field, new in getattr(form, f'override_{element}s', {}).items():
            setattr(form.fields[field], element, new)

        for field, new in getattr(form, f'append_{element}s', {}).items():
            setattr(form.fields[field], element, getattr(form.fields[field], element) + new)


def customizable(klass):
    """ decorator that makes a django form easier to customize
    :return:
    """
    if not issubclass(klass, BaseForm):
        raise TypeError(f'Decorator {__name__} can only be applied to subclasses of django.forms.BaseForm')
    orig_init = klass.__init__

    def __init__(self, *args, **kws):
        orig_init(self, *args, **kws)
        # only apply customization once
        if not getattr(self, '_is_customized', False):
            apply_form_customizations(self)
            self._is_customized = True

    klass.__init__ = __init__
    return klass
