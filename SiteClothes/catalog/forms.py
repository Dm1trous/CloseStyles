from django import forms

from .models import Comment, Topic, PromoCode

class CreateTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = [
            'title'
        ]


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'body', 'author', 'post'
        ]

    def __init__(self, *args, **kwargs):
        ...
        super(CreateCommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].required = False

class ApplyPromoCodeForm(forms.Form):
    promocode = forms.CharField(label='Промокод', required=False)

    def clean_promocode(self):
        data = self.cleaned_data['promocode'].strip()
        try:
            PromoCode.objects.get(code=data, active=True)
        except PromoCode.DoesNotExist:
            raise forms.ValidationError("Такой промокод не найден или неактивен.")
        return data