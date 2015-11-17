from django.contrib import admin
from .models import Department,Student,Course,Result,UserAugment
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .forms import ResultForm
from django.forms.models import BaseInlineFormSet
from django.forms.models import ModelForm
from django.forms import formset_factory
from django.forms import ModelForm

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserAugment
class MyUserAdmin(UserAdmin,admin.ModelAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('department',)}),
    )
    def get_queryset(self, request):
        qs = super(MyUserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(dept=request.department)
    
     #def queryset(self, request):

admin.site.register(UserAugment, MyUserAdmin)

"""class UserAdmin(admin.ModelAdmin):
    
    def has_change_permission(self, request, obj=None ):
        return self.user_has_permission(request.obj)
    def user_has_permission(self, request, obj ):
        if hasattr(request.user,'department') and obj is not None:
            return request.user.department == obj.dept
        return False"""
    
class ListFilter(admin.SimpleListFilter):
    parameter_name = 'dept'
    title = ('Department')
    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            list_of_departments = []
            queryset = Department.objects.values_list('dname')
            for department in queryset:
                list_of_departments.append(department[0])
            return ( (t,t) for t in list_of_departments)

    def queryset(self, request, queryset):
        if request.user.is_superuser:
            if self.value():
                return queryset.filter(dept=self.value())
            return queryset
            
class StudentAdmin(admin.ModelAdmin):
    list_filter = (ListFilter,)
    # list_filter = (
    #     ('dept', admin.RelatedFieldListFilter),
    # )
    ordering = ['usn',]
    search_fields = ('usn','sname',)
    list_display = ['usn','sname']
    user = get_user_model()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "dept":
                kwargs["initial"] = request.user.department
                kwargs["queryset"] = Department.objects.filter(dname=request.user.department)
        return super(StudentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    # if user.is_superuser():
    #     list_filter = ('dept',)
    # # fieldsets = (
    #     ('None', {
    #         'fields': ('usn', 'sname', 'dept', 'sem')
    #     }),
    #     ('Advanced options', {
    #         'classes': ('collapse','wide'),
    #         'fields': ('usn', 'sname', 'sem')
    #     }),
    #  )
    #fields = ['usn']
    def get_queryset(self, request):
        qs = super(StudentAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(dept=request.user.department)

class CustomInlineFormset(BaseInlineFormSet):
    """
    Custom formset that support initial data
    """
    # def __init__(self, *args, **kwargs):
    #     kwargs['initial'] = [{ 'usn': '13BT6CS001', }]
    #     super(CustomInlineFormset, self).__init__(*args, **kwargs)
    def initial_form_count(self):
        """
        set 0 to use initial_extra explicitly.
        """
        if self.initial_extra:
            return 0
        else:
            return BaseInlineFormSet.initial_form_count(self)

    def total_form_count(self):
        """
        here use the initial_extra len to determine needed forms
        """
        if self.initial_extra:
            count = len(self.initial_extra) if self.initial_extra else 0
            count += self.extra
            return count
        else:
            return BaseInlineFormSet.total_form_count(self)


class CustomModelForm(ModelForm):
    """
    Custom model form that support initial data when save
    """
    def __init__(self, *args, **kwargs):
        #self.user = user
        self.request = kwargs.pop('request', None)
        super(CustomModelForm, self).__init__(*args, **kwargs)
        #validUsn = Student.objects.values_list('usn').filter(dept=self.request.user.department)
        # self.get_queryset.filter(usn=validUsn)
       # self.fields['usn'].queryset = Result.objects.filter(usn='13BT6CS004')
        
        # return qs
    
    def has_changed(self):
        """
        Returns True if we have initial data.
        """
        has_changed = ModelForm.has_changed(self)
        return bool(self.initial or has_changed)



class CustomInlineAdmin(admin.TabularInline):
    """
    Custom inline admin that support initial data
    """
    form = CustomModelForm
    formset = CustomInlineFormset
    ordering=['usn']
    def  get_queryset(self, request):
        qs = super(CustomInlineAdmin,self).get_queryset(request)
        qs.filter(usn='13BT6CS004')
        return qs
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "usn":
                kwargs["queryset"] = Student.objects.filter(dept=request.user.department)
        return super(CustomInlineAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    # def get_form(self, request, obj=None, **kwargs):
    # 
    #     AdminForm = super(CustomInlineAdmin, self).get_form(request, obj, **kwargs)
    # 
    #     class AdminFormWithRequest(AdminForm):
    #         def __new__(cls, *args, **kwargs):
    #             kwargs['request'] = request
    #             return AdminForm(*args, **kwargs)
    # 
    #     return AdminFormWithRequest
#     (initial=[{'usn': '13BT6CS004'}])



class ResultInline(CustomInlineAdmin):
        model = Result
        #prepopulated_fields = {"usn": ("intmarks",)}
        #raw_id_fields = ("usn",)
        extra = 3
        # formset = 

class MySuperUserForm(ModelForm):
    class Meta:
        model = Result
        fields = ['usn', 'intmarks', 'extmarks']
        # list_display = ['usn', 'intmarks', 'extmarks']
        # list_editable = ['usn', 'intmarks', 'extmarks']
# class  AnalysisInline(admin.TabularInline):
#     form = ModelForm
#     formset = BaseInlineFormSet
#     model = Result
#     fields = ['usn']
    

    

class CourseAdmin(admin.ModelAdmin):
    # inlines = [ResultInline,AnalysisInline]
    inlines = [ResultInline]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "dname":
                kwargs["initial"] = request.user.department
                kwargs["queryset"] = Department.objects.filter(dname=request.user.department)
        return super(CourseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_formsets(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # hide MyInline in the add view
            if isinstance(inline, ResultInline) and obj is None:
                continue
            yield inline.get_formset(request, obj)
    # def  get_queryset(self, request):
    #     qs = super(CourseAdmin,self).get_queryset(request)
    #     return qs.none()
    ResultFormSet = formset_factory(ResultInline)
    # def get_form(self,request,obj=None,**kwargs ):
    #     if request.user.is_superuser:
    #         if not kwargs['form']:
    #             kwargs['form'] = {}
    #         kwargs['form'] = MySuperUserForm
    #         return super(CourseAdmin,self).get_form(request,obj,**kwargs)
    
    # def _create_formsets(self, request, obj, change):
    #     """overide to provide initial data for inline formset"""
    #     formsets = []
    #     inline_instances = []
    #     prefixes = {}
    #     get_formsets_args = [request]
    #     if change:
    #         get_formsets_args.append(obj)
    #     for FormSet, inline in self.get_formsets_with_inlines(*get_formsets_args):
    #         prefix = FormSet.get_default_prefix()
    #         prefixes[prefix] = prefixes.get(prefix, 0) + 1
    #         if prefixes[prefix] != 1 or not prefix:
    #             prefix = "%s-%s" % (prefix, prefixes[prefix])
    #         formset_params = {
    #             'instance': obj,
    #             'prefix': prefix,
    #             'queryset': inline.get_queryset(request),
    #         }
    #         if request.method == 'POST':
    #             formset_params.update({
    #                 'data': request.POST,
    #                 'files': request.FILES,
    #                 'save_as_new': '_saveasnew' in request.POST
    #             })
    # 
    #         if change:
    #             formsets.append(FormSet(**formset_params))
    #             inline_instances.append(inline)
    #         else:
    #             if isinstance(inline, ResultInline):
    #                 inline_initial_data = [
    #                     {'usn': '13BT6CS004'},
    #                     {'usn': '13BT6CS003'}
    #                 ]
    #                 formset_params['initial'] = inline_initial_data
    #                 formsets.append(FormSet(**formset_params))
    #                 inline_instances.append(inline)
    #             else:
    #                 formsets.append(FormSet(**formset_params))
    #                 inline_instances.append(inline)
    # 
    #     return formsets, inline_instances




class ResultAdmin(admin.ModelAdmin): #Result admin
    form = ResultForm
    list_display = ['get_usn','get_internals','get_course','okay']
    #ordering = ['usn','course']
    
    def get_usn(self,obj):
        return ("%s" % (obj.usn))
    get_usn.short_description = 'USN'
    
    def get_internals(self,obj):
        return("%s"%(obj.intmarks))
    get_internals.short_description = 'INTERNALS'
    
    def get_course(self, obj):
        return("%s"%(obj.course))
    get_course.short_description = 'COURSE'
    
    def get_queryset(self, request):
        qs = super(ResultAdmin, self).get_queryset(request)
        #validUsn = Student.objects.values_list('usn').filter(dept=request.user.department)
        #qs = qs.filter(usn='13BT6CS004')
        qs = qs.order_by('usn')
        #qs = qs.filter(usn='13BT6CS001')
        return qs
    
    def okay(self,obj):
        return False
    okay.boolean=True
    okay.short_description = 'Name'
    
admin.site.register(Course,CourseAdmin)
admin.site.register(Department)
admin.site.register(Student,StudentAdmin)
admin.site.register(Result,ResultAdmin)
#admin.site.register(UserAugment,UserAdmin)