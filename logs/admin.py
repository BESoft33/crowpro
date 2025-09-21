from django.contrib import admin
from admincharts.admin import AdminChartMixin
from .models import RequestLog
from django.db.models import Count


class RequestLogAdmin(AdminChartMixin, admin.ModelAdmin):
    list_display = ['method', 'path', 'user', 'remote_addr', 'country', 'status_code', 'created_at']
    list_filter = ['method', 'status_code', 'country', 'device', 'created_at']
    search_fields = ['path', 'user_agent', 'remote_addr', 'referrer']

    chart_settings = [
        {
            "label": "Requests by Method",
            "chart_type": "bar",
            "datasets": [
                {
                    "queryset": RequestLog.objects.all(),
                    "field": "method",
                }
            ],
        },
        {
            "label": "Requests by Status",
            "chart_type": "pie",
            "datasets": [
                {
                    "queryset": RequestLog.objects.all(),
                    "field": "status_code",
                }
            ],
        },
        # {
        #     "label": "Top 10 Endpoints",
        #     "chart_type": "pie",
        #     "datasets": [
        #         {
        #             "queryset": RequestLog.objects.filter(path__in=[
        #                 r.path for r in RequestLog.objects.values('path')
        #                 .annotate(count=Count('id')).order_by('-count')[:10]
        #             ]),
        #             "field": "path",
        #         }
        #     ]
        # }
    ]


admin.site.register(RequestLog, RequestLogAdmin)
