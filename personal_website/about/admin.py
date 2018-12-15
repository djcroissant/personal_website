from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin

from .models import Bio


admin.site.register(Bio, MarkdownxModelAdmin)
