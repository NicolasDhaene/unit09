from django import forms
from django.forms.extras.widgets import SelectDateWidget
from datetime import datetime
from .models import Menu, Item


class MenuForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), widget=forms.SelectMultiple())
    expiration_date = forms.DateTimeField(
                            widget=SelectDateWidget(attrs={"style": "width: 15%; "
                                                           "display: inline-block; "
                                                           "font-weight:normal"},
                                                    years=range(int(datetime.now().year), 2025)))

    class Meta:
        model = Menu
        exclude = ("created_date",)

    def clean(self):
        form_data = self.cleaned_data
        form_season = form_data.get("season")

        if not form_season:
            raise forms.ValidationError(
                "You are required to fill the ""season"" field"
            )
        return form_data
