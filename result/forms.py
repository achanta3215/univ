from django.forms import ModelForm
from .models import Result

class ResultForm(ModelForm):
    #course = MySlugFormField()
    def __init__(self, *args, **kwargs):
        #self.user = user
        super(ResultForm, self).__init__(*args, **kwargs)
        # self.get_queryset.filter(usn='13BT6CS004')
        self.fields['usn'].queryset = Result.objects.filter(usn='13BT6CS004')
        # self.fields['usn'].get_queryset.filter(usn='13BT6CS004')
        self.fields['usn'].initial = '13BT6CS004'
        #self.fields['email'].initial = user.email
    
    class Meta:
        model = Result
        fields = ['usn','course','intmarks','extmarks']

    def save(self, commit=True):
        self.user.email = self.cleaned_data['email']
        if commit:
            self.user.save()
        return self.user
    
    
        
    