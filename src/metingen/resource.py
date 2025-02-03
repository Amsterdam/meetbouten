from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from import_export.fields import Field
from import_export.resources import Error, ModelResource
from import_export.widgets import ForeignKeyWidget

from .models import Hoogtepunt, MetingControle, MetingHerzien, MetingVerrijking


class SimpleError(Error):
    def __init__(self, error, traceback=None, row=None, number=None):
        super().__init__(error, traceback=traceback, row=row, number=number)
        self.traceback = " "


class MetingControleResource(ModelResource):
    hoogtepunt = Field(
        column_name="hoogtepunt",
        attribute="hoogtepunt",
        widget=ForeignKeyWidget(Hoogtepunt, field="nummer"),
    )

    class Meta:
        model = MetingControle
        import_id_fields = ("hoogtepunt",)
        exclude = ("id",)
        use_bulk = True

    def before_import(self, dataset, **kwargs):
        # import_export Version 4 change: param dry-run passed in kwargs
        # during 'confirm' step, dry_run is True
        dry_run = kwargs.get("dry_run", False)
        if not dry_run:
            truncate(MetingControle)

    def before_import_row(self, row, **kwargs):
        if not (Hoogtepunt.objects.filter(nummer=row["hoogtepunt"]).exists()):
            error = ObjectDoesNotExist(
                f"Provided hoogtepunt {row['hoogtepunt']} does not exist."
            )
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


class MetingVerrijkingResource(ModelResource):
    hoogtepunt = Field(
        column_name="hoogtepunt",
        attribute="hoogtepunt",
        widget=ForeignKeyWidget(Hoogtepunt, field="nummer"),
    )

    class Meta:
        model = MetingVerrijking
        import_id_fields = ("hoogtepunt",)
        exclude = "id"

    def before_import(self, dataset, **kwargs):
        # import_export Version 4 change: param dry-run passed in kwargs
        print(kwargs)
        # during 'confirm' step, dry_run is True
        dry_run = kwargs.get("dry_run", False)
        if not dry_run:
            truncate(MetingVerrijking)

    def before_import_row(self, row, **kwargs):
        if not (Hoogtepunt.objects.filter(nummer=row["hoogtepunt"]).exists()):
            error = ObjectDoesNotExist(
                f"Provided hoogtepunt {row['hoogtepunt']} does not exist."
            )
            raise error

        _hoogtepunt = Hoogtepunt.objects.get(nummer=row["hoogtepunt"])

        row["x"] = _hoogtepunt.geom.x
        row["y"] = _hoogtepunt.geom.y
        row["file_name"] = kwargs["import_file"].name

        if MetingHerzien.objects.filter(hoogtepunt=_hoogtepunt.id).exists():
            _last_meting = MetingHerzien.objects.filter(
                hoogtepunt=_hoogtepunt.id
            ).latest("inwindatum")

            row["hoogte"] = _last_meting.hoogte
            row["inwindatum"] = _last_meting.inwindatum

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
    def before_import(self, dataset, **kwargs):
        # truncate table before import when dry_run = False
        if not kwargs['dry_run']:
            truncate(modelobject)
    """

    raw_query = f"""
        TRUNCATE TABLE {model._meta.db_table} RESTART IDENTITY
        """

    with connection.cursor() as cursor:
        cursor.execute(raw_query, {})
