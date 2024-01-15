# Generated by Django 4.1.12 on 2023-11-14 14:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("referentie_tabellen", "0002_seed_static_tables"),
        ("metingen", "0010_auto_20230406_1208"),
    ]

    operations = [
        migrations.AlterField(
            model_name="grondslagpunt",
            name="bron",
            field=models.ForeignKey(
                db_column="bro_id",
                on_delete=django.db.models.deletion.PROTECT,
                to="referentie_tabellen.bron",
            ),
        ),
        migrations.AlterField(
            model_name="grondslagpunt",
            name="type",
            field=models.ForeignKey(
                db_column="typ_nummer",
                on_delete=django.db.models.deletion.PROTECT,
                to="referentie_tabellen.type",
            ),
        ),
        migrations.AlterField(
            model_name="grondslagpunt",
            name="wijze_inwinning",
            field=models.ForeignKey(
                blank=True,
                db_column="wijze_inwinning",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="referentie_tabellen.wijzeninwinning",
            ),
        ),
        migrations.AlterField(
            model_name="hoogtepunt",
            name="merk",
            field=models.ForeignKey(
                db_column="mer_id",
                on_delete=django.db.models.deletion.PROTECT,
                to="referentie_tabellen.merk",
            ),
        ),
        migrations.AlterField(
            model_name="hoogtepunt",
            name="status",
            field=models.ForeignKey(
                blank=True,
                db_column="sta_id",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="referentie_tabellen.status",
            ),
        ),
        migrations.AlterField(
            model_name="hoogtepunt",
            name="type",
            field=models.ForeignKey(
                db_column="typ_nummer",
                on_delete=django.db.models.deletion.PROTECT,
                to="referentie_tabellen.type",
            ),
        ),
        migrations.AlterField(
            model_name="meting",
            name="bron",
            field=models.ForeignKey(
                db_column="bro_id",
                on_delete=django.db.models.deletion.PROTECT,
                to="referentie_tabellen.bron",
            ),
        ),
        migrations.AlterField(
            model_name="meting",
            name="hoogtepunt",
            field=models.ForeignKey(
                db_column="hoo_id",
                on_delete=django.db.models.deletion.PROTECT,
                to="metingen.hoogtepunt",
            ),
        ),
        migrations.AlterField(
            model_name="meting",
            name="metingtype",
            field=models.ForeignKey(
                db_column="mty_id",
                on_delete=django.db.models.deletion.PROTECT,
                to="referentie_tabellen.metingtype",
            ),
        ),
        migrations.AlterField(
            model_name="meting",
            name="wijze_inwinning",
            field=models.ForeignKey(
                blank=True,
                db_column="wijze_inwinning",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="referentie_tabellen.wijzeninwinning",
            ),
        ),
        migrations.AlterField(
            model_name="metingcontrole",
            name="bron",
            field=models.ForeignKey(
                db_column="bro_id",
                on_delete=django.db.models.deletion.PROTECT,
                to="referentie_tabellen.bron",
            ),
        ),
        migrations.AlterField(
            model_name="metingcontrole",
            name="hoogtepunt",
            field=models.ForeignKey(
                db_column="hoo_id",
                on_delete=django.db.models.deletion.PROTECT,
                to="metingen.hoogtepunt",
            ),
        ),
        migrations.AlterField(
            model_name="metingcontrole",
            name="metingtype",
            field=models.ForeignKey(
                db_column="mty_id",
                on_delete=django.db.models.deletion.PROTECT,
                to="referentie_tabellen.metingtype",
            ),
        ),
        migrations.AlterField(
            model_name="metingcontrole",
            name="wijze_inwinning",
            field=models.ForeignKey(
                blank=True,
                db_column="wijze_inwinning",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="referentie_tabellen.wijzeninwinning",
            ),
        ),
        migrations.AlterField(
            model_name="metingherzien",
            name="bron",
            field=models.ForeignKey(
                db_column="bro_id",
                on_delete=django.db.models.deletion.PROTECT,
                to="referentie_tabellen.bron",
            ),
        ),
        migrations.AlterField(
            model_name="metingherzien",
            name="hoogtepunt",
            field=models.ForeignKey(
                db_column="hoo_id",
                on_delete=django.db.models.deletion.PROTECT,
                to="metingen.hoogtepunt",
            ),
        ),
        migrations.AlterField(
            model_name="metingherzien",
            name="metingtype",
            field=models.ForeignKey(
                db_column="mty_id",
                on_delete=django.db.models.deletion.PROTECT,
                to="referentie_tabellen.metingtype",
            ),
        ),
        migrations.AlterField(
            model_name="metingherzien",
            name="wijze_inwinning",
            field=models.ForeignKey(
                blank=True,
                db_column="wijze_inwinning",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="referentie_tabellen.wijzeninwinning",
            ),
        ),
        migrations.AlterField(
            model_name="metingreferentiepunt",
            name="hoogtepunt",
            field=models.ForeignKey(
                db_column="hoo_id",
                on_delete=django.db.models.deletion.PROTECT,
                to="metingen.hoogtepunt",
            ),
        ),
        migrations.AlterField(
            model_name="metingreferentiepunt",
            name="meting",
            field=models.ForeignKey(
                db_column="met_id",
                on_delete=django.db.models.deletion.PROTECT,
                to="metingen.meting",
            ),
        ),
        migrations.AlterField(
            model_name="metingverrijking",
            name="hoogtepunt",
            field=models.ForeignKey(
                db_column="hoo_id",
                on_delete=django.db.models.deletion.PROTECT,
                to="metingen.hoogtepunt",
            ),
        ),
        migrations.AlterField(
            model_name="metrefpuntenherz",
            name="hoogtepunt",
            field=models.ForeignKey(
                db_column="hoo_id",
                on_delete=django.db.models.deletion.PROTECT,
                to="metingen.hoogtepunt",
            ),
        ),
        migrations.AlterField(
            model_name="metrefpuntenherz",
            name="meting",
            field=models.ForeignKey(
                db_column="met_id",
                on_delete=django.db.models.deletion.PROTECT,
                to="metingen.metingherzien",
            ),
        ),
    ]
