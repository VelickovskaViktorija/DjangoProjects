# FILE: admin.py
# Конфигурација на админ панелот според зададените правила
from django.contrib import admin
from .models import Agent, Feature, Property
from django.utils import timezone

class AgentAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class FeatureAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'area', 'listed_date', 'is_reserved', 'is_sold')
    filter_horizontal = ('features', 'agents',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(listed_date=timezone.now().date())
        try:
            agent = Agent.objects.get(email=request.user.email)
            return qs.filter(agents=agent)
        except Agent.DoesNotExist:
            return qs.none()

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            try:
                agent = Agent.objects.get(email=request.user.email)
                return agent in obj.agents.all()
            except Agent.DoesNotExist:
                return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj and obj.features.exists():
            return False
        return True

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not request.user.is_superuser:
            try:
                agent = Agent.objects.get(email=request.user.email)
                obj.agents.add(agent)
            except Agent.DoesNotExist:
                pass

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        if obj.is_sold:
            for agent in obj.agents.all():
                agent.sales_count += 1
                agent.save()

admin.site.register(Agent, AgentAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Property, PropertyAdmin)