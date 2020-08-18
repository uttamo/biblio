from django.forms import ModelForm, Select
from .models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        # (value, label) pairs
        widgets = {
            'rating': Select(choices=([
                (1, '1 ★'),
                (2, '2 ★★'),
                (3, '3 ★★★'),
                (4, '4 ★★★★'),
                (5, '5 ★★★★★'),
                (6, '6 ★★★★★★'),
                (7, '7 ★★★★★★★'),
                (8, '8 ★★★★★★★★'),
                (9, '9 ★★★★★★★★★'),
                (10, '10 ★★★★★★★★★★')
            ])),
        }

        labels = {
            'text': 'Review',
        }
