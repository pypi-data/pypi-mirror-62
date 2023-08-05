import django_filters

from waldur_core.core import filters as core_filters

from . import models


class DeploymentPlanFilter(django_filters.FilterSet):
    project = core_filters.URLFilter(view_name='project-detail', field_name='project__uuid')
    project_uuid = django_filters.UUIDFilter(field_name='project__uuid')
    customer = core_filters.URLFilter(view_name='customer-detail', field_name='project__customer__uuid')
    customer_uuid = django_filters.UUIDFilter(field_name='project__customer__uuid')

    o = django_filters.OrderingFilter(
        fields=('name', 'created')
    )

    class Meta:
        model = models.DeploymentPlan
        fields = ('project', 'project_uuid', 'customer', 'customer_uuid')
