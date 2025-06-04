from django.contrib import admin
from .models import User, Form, Submission, UserProfile, Tag, FormTag

class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 0

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class FormTagInline(admin.TabularInline):
    model = FormTag
    extra = 1

class FormAdmin(admin.ModelAdmin):
    inlines = [FormTagInline]

class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline]

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('form', 'user', 'submission_date')
    list_filter = ('form', 'user')
    search_fields = ('form__title', 'user__username', 'user__email')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(User, UserAdmin)
admin.site.register(Form, FormAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
