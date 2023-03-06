from import_export.resources import ModelResource, Error
from .models import MetingControle, Hoogtepunt

from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from django.core.exceptions import ObjectDoesNotExist
from django.db import connection


class SimpleError(Error):
    def __init__(self, error, traceback=None, row=None):
        super().__init__(error, traceback=traceback, row=row)
        self.traceback = " "


class MetingControleResource(ModelResource):
    hoogtepunt = Field(
        column_name="hoogtepunt",
        attribute="hoogtepunt",
        widget=ForeignKeyWidget(Hoogtepunt, field="nummer"),
    )

    class Meta:
        model = MetingControle
        import_id_fields = ('hoogtepunt',)
        exclude = ('id',)
        use_bulk = True

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        if not dry_run:
            truncate(MetingControle)

    def before_import_row(self, row, row_number=None, **kwargs):
        if not (Hoogtepunt.objects.filter(nummer=row['hoogtepunt']).exists()):
            error = ObjectDoesNotExist(f"Provided hoogtepunt {row['hoogtepunt']} does not exist.")
            raise error

        row["inwindatum"] = kwargs.get("inwindatum")
        row["bron"] = kwargs.get("bron").id
        row["wijze_inwinning"] = kwargs.get("wijze_inwinning").id
        row["metingtype"] = kwargs.get("metingtype").id

    @classmethod
    def get_error_result_class(self):
        """
        Returns a class which has custom formatting of the error.
        Used here to simplify the trace error
        """
        return SimpleError


def truncate(model):
    """
    truncate db table and restart AutoField primary_key for import

    use as follows:
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        # truncate table before import when dry_run = False
        if not dry_run:
            truncate(modelobject)
    """

    raw_query = f"""
        TRUNCATE TABLE {model._meta.db_table} RESTART IDENTITY
        """

    with connection.cursor() as cursor:
        cursor.execute(raw_query, {})
