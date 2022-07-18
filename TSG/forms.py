from django.forms import ModelForm
from django import forms
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError


from TSG.models import Notification, Tsg, Flat, NotificationSection, Announcement
from django.forms import CheckboxSelectMultiple


class FlatSelectWidget(CheckboxSelectMultiple):
    class Media:
        css = {
            'all': ('css/flatSelect.css', )
        }
        js = ('js/flatSelect.js', )

    def __init__(self, tsg, attrs=None, choices=()):
        self.tsg = tsg
        super(CheckboxSelectMultiple, self).__init__(attrs)
        self.choices = list(choices)

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = []
        tsg = self.tsg

        output = [u'<div class="tree">']

        output.append(u'<li class="drop"> <span class="top_drop"><input type="checkbox" > %s <i>+</i></span>' % tsg.name)
        output.append(u'<ul >')


        houseSet = tsg.house_set.all()
        showHouse = len(houseSet) > 1

        for house in houseSet:
            if showHouse:
                output.append(u'<li class="drop"> <span><input type="checkbox" > %s <i>+</i></span>' % house.address)
                output.append(u'<ul >')

            entranceSet = house.entrance_set.all()
            showEntrance = len(entranceSet) > 1

            for entrance in entranceSet:
                if showEntrance:
                    output.append(u'<li class="drop"><span><input type="checkbox" > %s  <i>+</i></span>' % entrance.name)
                    output.append(u'<ul >')

                for flat in entrance.flat_set.all():
                    cbAttrs = dict(attrs)
                    cbAttrs['class'] = 'flat_cb'
                    cb = forms.CheckboxInput(cbAttrs, check_test=lambda v: v in value)
                    rendered_cb = cb.render(name, str(flat.id))
                    output.append(u'<li> <span><label>%s %s</label></span></li>' % (rendered_cb, flat.__str__()))

                if showEntrance:
                    output.append(u'</ul>')
                    output.append(u'</li>')

            if showHouse:
                output.append(u'</ul>')
                output.append(u'</li>')


        # for (val, label) in self.choices:
        #     cb = forms.CheckboxInput(attrs, check_test=lambda v: v in value)
        #     rendered_cb = cb.render(name, val)
        #     output.append(u'<li><label>%s %s</label></li>' % (rendered_cb, label))
        output.append(u'</ul>')
        output.append(u'</li>')
        output.append(u'</div>')

        print(mark_safe(u'\n'.join(output)))
        return mark_safe(u'\n'.join(output))


class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = ['tsg', 'section', 'theme', 'preview_text', 'text', 'recipients', ]
        # exclude = ['creation_date', ]
        error_messages = {
            'recipients': {
                'required': 'Выберите хотя бы одну квартиру'
            }
        }

    def clean_tsg(self):
        return self.fields['tsg'].clean(self.tsg)

    def clean_theme(self):
        if self.cleaned_data['theme'] is None:
            return str(self.cleaned_data['section'])
        return self.cleaned_data['theme']

    def clean_section(self):
        if self.cleaned_data['section'].tsg.pk != self.tsg.pk:
            raise ValidationError("Выберите раздел")
        return self.cleaned_data['section']

    def __init__(self, tsg, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.tsg = tsg
        self.fields['tsg'].widget = forms.HiddenInput()
        self.fields['tsg'].required = False
        self.fields['recipients'].widget = FlatSelectWidget(tsg)
        self.fields['recipients'].queryset = Flat.objects.filter(entrance__house__TSG__id=tsg.pk)
        self.fields['section'].queryset = NotificationSection.objects.filter(tsg__id=tsg.pk)


class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = ['tsg', 'theme', 'text', ]
        # exclude = ['creation_date', ]
        error_messages = {
            'text': {
                'required': 'Напишите текст объявления'
            }
        }

    def __init__(self, tsg, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.tsg = tsg
        self.fields['tsg'].widget = forms.HiddenInput()
        self.fields['tsg'].required = False

    def clean_tsg(self):
        return self.fields['tsg'].clean(self.tsg)

