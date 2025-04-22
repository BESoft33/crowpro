from django.contrib import admin
from admincharts.admin import AdminChartMixin
from .models import RequestLog
from django.db.models import Count
from django.db.models.functions import TruncDay


class RequestLogAdmin(AdminChartMixin, admin.ModelAdmin):
    list_display = ['method', 'path', 'user', 'remote_addr', 'country', 'status_code', 'created_at']
    list_filter = ['method', 'status_code', 'country', 'device', 'created_at']
    search_fields = ['path', 'user_agent', 'remote_addr', 'referrer']

    # Define charts
    admincharts_settings = {
        'charts': [
            {
                'title': 'Requests by Day',
                'x_field': 'created_at',
                'y_field': 'id',
                'chart_type': 'line',
                'group_by': TruncDay('created_at'),
            },
            {
                'title': 'Top Countries',
                'x_field': 'country',
                'y_field': 'id',
                'chart_type': 'bar',
                'group_by': 'country',
            },
            {
                'title': 'Device Distribution',
                'x_field': 'device',
                'y_field': 'id',
                'chart_type': 'pie',
                'group_by': 'device',
            },
            {
                'title': 'Status Code Distribution',
                'x_field': Count('status_code'),
                'y_field': 'id',
                'chart_type': 'bar',
                'group_by': 'status_code',
            },
            {
                'title': 'Browser Usage',
                'x_field': 'browser',
                'y_field': 'id',
                'chart_type': 'bar',
                'group_by': 'browser',
            },
        ]
    }

    def changelist_view(self, request, extra_context=None):
        qs = self.model.objects.all()
        # Debug output of the grouping query:
        grouped_qs = qs.annotate(day=TruncDay('created_at')) \
                       .values('day') \
                       .annotate(total=Count('id'))
        print("Grouped data for chart:", list(grouped_qs))
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(RequestLog, RequestLogAdmin)
