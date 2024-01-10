from django.forms import ModelForm, Form, BooleanField, ModelMultipleChoiceField, CheckboxSelectMultiple, CharField
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from juntagrico.config import Config
from juntagrico.dao.activityareadao import ActivityAreaDao

from juntagrico_godparent.models import Godparent, Godchild
from juntagrico_godparent.util.customize import customizable


def contact_admin_link(text):
    return mark_safe(
        escape(
            text
        ).format('<a href="mailto:{0}">{0}</a>'.format(Config.info_email()))
    )


@customizable
class RegisterForm(Form):
    areas = ModelMultipleChoiceField(queryset=ActivityAreaDao.all_visible_areas_ordered(),
                                     widget=CheckboxSelectMultiple,
                                     label=_('Tätigkeitsbereiche'), required=False,
                                     help_text=_('Aktuell bist du in diesen Tätigkeitsbereichen eingetragen. '
                                                 'Bitte prüfe ob dies noch stimmt.<br>'
                                                 'Wenn du die Auswahl hier änderst, wirst du in die entsprechenden'
                                                 'Tätigkeitsbereiche eingetragen.'))
    email = CharField(label=_('E-Mail-Adresse'), disabled=True,
                      help_text=contact_admin_link(
                          _('Überprüfe deine E-Mail-Adresse. Kontaktiere {} um sie zu ändern.')))
    phone = CharField(label=_('Telefonnummer'), help_text='Überprüfe deine Telefonnummer')
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
        fields = ('max_godchildren', 'languages', 'slots', 'children', 'areas', 'comments')


@customizable
class GodchildForm(RegisterForm, ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['children'].help_text = _(f'Falls du Kinder hast, die du zu den '
                                              f'Einsätzen bei {Config.organisation_name()} mitbringen möchtest, '
                                              f'hat sich eine Einführung durch ein Mitglied bewährt, das selbst Kinder hat.')
        self.fields['children'].label = _('Gotte/Götti mit eigenen Kindern bevorzugen')

    class Meta:
        model = Godchild
        fields = ('languages', 'slots', 'children', 'talents', 'areas', 'comments')
