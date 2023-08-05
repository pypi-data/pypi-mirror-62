from __future__ import unicode_literals

from django.core import validators
from django.forms import ChoiceField, MultipleChoiceField, TypedChoiceField, TypedMultipleChoiceField, DateTimeField
from django.shortcuts import _get_queryset

from .widgets import SelectCallback, SelectCallbackMultiple, Select2AjaxWidget, Select2AjaxMultipleWidget


class RelatedChoiceFieldMixin(object):
    widget = SelectCallback

    def __init__(self, model, add_empty=False,
                 label_name=None, value_name=None,
                 empty_label=None, empty_value=None,
                 coerce=None, filter=None, **kwargs):
        self.model = model
        self.add_empty = add_empty
        self.label_name = label_name
        self.value_name = value_name or 'pk'
        self.empty_label = empty_label
        self.empty_value = empty_value
        self.coerce = coerce or self.model_coerce
        self.filter = filter
        super(ChoiceField, self).__init__(**kwargs)
        self._choices_data = None
        self._request = None

    def __deepcopy__(self, memo):
        result = super(ChoiceField, self).__deepcopy__(memo)
        result._choices_data = None
        result.widget.choices_callback = result.choices_callback
        return result

    def model_coerce(self, value):
        return _get_queryset(self.model).get(**{self.value_name: value})

    def choices_callback(self):
        return self.choices

    @property
    def choices(self):
        if self._choices_data is None:
            self._choices_data = self.populate()
        return self._choices_data

    @choices.setter
    def choices(self, value):
        self._choices_data = value

    def populate(self):
        choices = []
        if self.add_empty:
            choices.append((self.empty_value or '',
                            self.empty_label or '-------'))

        def _get_field(obj, fieldname=None):
            if fieldname:
                value = getattr(obj, fieldname)
                if callable(value):
                    value = value()
            else:
                value = str(obj)
            return value

        qs = _get_queryset(self.model)
        if self.filter:
            if callable(self.filter):
                _data = self.filter(self._request)
            else:
                _data = self.filter
            qs = qs.filter(**_data)

        for item in qs:
            label = _get_field(item, self.label_name)
            value = _get_field(item, self.value_name)
            choices.append((str(value), label))
        return choices


class AjaxChoiceFieldMixin(object):
    widget = Select2AjaxWidget

    def __init__(self, model, add_empty=False, label_name=None,
                 value_name=None, data_url=None, filter=None, **kwargs):
        self.model = model
        self.label_name = label_name
        self.value_name = value_name or 'pk'
        self.filter = filter
        super(AjaxChoiceFieldMixin, self).__init__(**kwargs)
        self.add_empty = add_empty
        self.data_url = data_url
        self._request = None

    @property
    def add_empty(self):
        return self._add_empty

    @add_empty.setter
    def add_empty(self, value):
        # Setting add_empty also sets the add_empty on the widget.
        self._add_empty = self.widget.add_empty = value

    @property
    def data_url(self):
        return self._data_url

    @data_url.setter
    def data_url(self, value):
        # Setting data_url also sets the data_url on the widget.
        self._data_url = self.widget.data_url = value

    @staticmethod
    def _get_field(obj, field_name=None):
        if field_name:
            value = getattr(obj, field_name)
            if callable(value):
                value = value()
        else:
            value = str(obj)
        return value

    def ajax_populate(self, form, name):
        _choices = []
        value = form.get_value_for(name)

        qs = _get_queryset(self.model)

        if self.filter:
            if callable(self.filter):
                _data = self.filter(self._request)
            else:
                _data = self.filter
            qs = qs.filter(**_data)

        if value not in validators.EMPTY_VALUES:
            if not isinstance(value, (list, tuple)):
                value = [value]
            qs = qs.filter(**{'%s__in' % self.value_name: value})
        else:
            qs = qs.none()

        for item in qs:
            label = self._get_field(item, self.label_name)
            value = self._get_field(item, self.value_name)
            _choices.append((str(value), label))
        self.choices = _choices


class AjaxTypedChoiceFieldMixin(AjaxChoiceFieldMixin):

    def __init__(self, model, coerce=None, **kwargs):
        super(AjaxTypedChoiceFieldMixin, self).__init__(model, **kwargs)
        self.coerce = coerce or self.model_coerce

    def model_coerce(self, value):
        return _get_queryset(self.model).get(**{self.value_name: value})


class RelatedChoiceField(RelatedChoiceFieldMixin, TypedChoiceField):
    pass


class RelatedMultipleChoiceField(RelatedChoiceFieldMixin, TypedMultipleChoiceField):
    widget = SelectCallbackMultiple


class AjaxChoiceField(AjaxChoiceFieldMixin, ChoiceField):
    widget = Select2AjaxWidget


class AjaxMultipleChoiceField(AjaxChoiceFieldMixin, MultipleChoiceField):
    widget = Select2AjaxMultipleWidget


class AjaxTypedChoiceField(AjaxTypedChoiceFieldMixin, TypedChoiceField):
    widget = Select2AjaxWidget


class AjaxTypedMultipleChoiceField(AjaxTypedChoiceFieldMixin, TypedMultipleChoiceField):
    widget = Select2AjaxMultipleWidget


class DateTimeNaiveField(DateTimeField):
    def clean(self, value):
        value = super(DateTimeNaiveField, self).clean(value)
        if value:
            value = value.replace(tzinfo=None)
        return value
