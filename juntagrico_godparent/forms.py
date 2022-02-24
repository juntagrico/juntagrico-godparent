from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm, Form, BooleanField, ModelMultipleChoiceField, CheckboxSelectMultiple
from django.utils.translation import gettext as _
from juntagrico.config import Config
from juntagrico.dao.activityareadao import ActivityAreaDao

from juntagrico_godparent import customizable
from juntagrico_godparent.models import Godparent, Godchild


@customizable
class RegisterForm(Form):
    areas = ModelMultipleChoiceField(queryset=ActivityAreaDao.all_visible_areas_ordered(), widget=CheckboxSelectMultiple,
                                     label=_('Tätigkeitsbereiche'), required=False,
                                     help_text=_('Aktuell bist du in diesen Tätigkeitsbereichen eingetragen. '
                                                 'Bitte prüfe ob dies noch stimmt.'))
    accept_terms = BooleanField(label=_('Ich bin einverstanden, dass meine E-Mail-Adresse und Telefonnummer '
                                        'dem vermittelten Mitglied mitgeteilt werden.'))

    def __init__(self, *args, editing=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', _('Ändern') if editing else _('Anmelden')))
        if editing:
            del self.fields['accept_terms']


@customizable
class GodparentForm(RegisterForm, ModelForm):
    class Meta:
        model = Godparent
        fields = ('max_godchildren', 'languages', 'slots', 'children', 'areas', 'other', 'comments')


@customizable
class GodchildForm(RegisterForm, ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['children'].help_text = _(f'Falls du Kinder hast, die du zu den '
                                              f'Einsätzen bei {Config.organisation_name()} mitbringen möchtest, '
                                              f'hat sich eine Einführung durch ein Mitglied bewährt, das selbst Kinder hat.')
        self.fields['children'].label = _('Gotti/Götti mit eigenen Kindern bevorzugen')

    class Meta:
        model = Godchild
        fields = ('languages', 'slots', 'children', 'talents', 'areas', 'other', 'comments')
