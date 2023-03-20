from metingen.models import MetingHerzien


class AdminChartMixin:
    change_list_template = "admin/generic_change_list.html"

    list_chart_data = {}
    list_chart_type = "scatter"
    list_chart_config = None  # Override the combined settings

    measurement_points = []

    class Media:
        css = {"all": ("admincharts/admincharts.css",)}
        js = (
            "admincharts/chart.min.js",
            "admincharts/admincharts.js",
        )

    def get_list_chart_queryset(self, changelist):
        if self.measurement_points:
            querysets = []
            for mp in self.measurement_points:
                metingen = list(MetingHerzien.objects.filter(hoogtepunt=mp.hoogtepunt).order_by("inwindatum"))
                metingen.append(mp)  # Add the measurement point itself
                querysets.append(metingen)
            return querysets
        return []

    def get_list_chart_config(self, queryset):
        if self.list_chart_config:
            return self.list_chart_config

        return {
            "type": self.list_chart_type,
            "data": self.get_list_chart_data(queryset),
        }

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        # This could be a redirect and not have context_data
        if not hasattr(response, "context_data"):
            return response

        if "cl" in response.context_data:
            changelist = response.context_data["cl"]
            chart_queryset = self.get_list_chart_queryset(changelist)
            response.context_data["adminchart_queryset"] = chart_queryset
            response.context_data[
                "adminchart_chartjs_config"
            ] = self.get_list_chart_config(chart_queryset)
            print(response.context_data[
                "adminchart_chartjs_config"
            ])
        else:
            response.context_data["adminchart_queryset"] = None
            response.context_data["adminchart_chartjs_config"] = None

        return response

    def get_list_chart_data(self, querysets):
        datasets = []
        labels = []
        for qs in querysets:
            if len(qs) == 0:
                continue

            # Set init_val to the first value in the queryset
            init_val = qs[0].hoogte if len(querysets) > 1 else 0

            # Don't display copies of graphs
            label = str(qs[0].hoogtepunt)
            if label not in labels:
                labels.append(label)
                datasets.append(
                    {
                        "label": label,
                        "data": [{'x': meting.inwindatum, 'y': meting.hoogte - init_val} for meting in qs],
                        "color": "green",
                        "borderColor": "green",
                        "showLine": True,
                    }
                )

        return {
            "labels": labels,
            "datasets": datasets,
        }
