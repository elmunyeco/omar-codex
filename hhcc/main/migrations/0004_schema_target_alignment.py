from django.db import migrations


TARGET_COLLATION = "utf8mb4_uca1400_ai_ci"
TARGET_CHARSET = "utf8mb4"
TARGET_TABLES = [
    "auth_group",
    "auth_group_permissions",
    "auth_permission",
    "auth_user",
    "auth_user_groups",
    "auth_user_user_permissions",
    "tipos_documentos",
    "pacientes",
    "historias_clinicas",
    "condiciones_medicas",
    "condiciones_medicas_historias",
    "signos_vitales",
    "comentarios_visitas",
    "indicaciones_visitas",
    "carotidas",
    "estudios_ecocardiograma",
    "conclusiones_ecocardiograma",
    "segmentos_ecocardiograma",
    "stress",
    "mmii",
    "django_admin_log",
    "django_content_type",
    "django_migrations",
    "django_session",
]


def _table_exists(cursor, table_name):
    cursor.execute(
        """
        SELECT COUNT(1)
        FROM information_schema.tables
        WHERE table_schema = DATABASE() AND table_name = %s
        """,
        [table_name],
    )
    return bool(cursor.fetchone()[0])


def _index_exists(cursor, table_name, index_name):
    cursor.execute(
        """
        SELECT COUNT(1)
        FROM information_schema.statistics
        WHERE table_schema = DATABASE()
          AND table_name = %s
          AND index_name = %s
        """,
        [table_name, index_name],
    )
    return bool(cursor.fetchone()[0])


def _foreign_key_exists(cursor, table_name, constraint_name):
    cursor.execute(
        """
        SELECT COUNT(1)
        FROM information_schema.table_constraints
        WHERE table_schema = DATABASE()
          AND table_name = %s
          AND constraint_type = 'FOREIGN KEY'
          AND constraint_name = %s
        """,
        [table_name, constraint_name],
    )
    return bool(cursor.fetchone()[0])


def _drop_unique_paciente_doc(cursor):
    cursor.execute(
        """
        SELECT s.index_name
        FROM information_schema.statistics s
        WHERE s.table_schema = DATABASE()
          AND s.table_name = 'pacientes'
          AND s.non_unique = 0
        GROUP BY s.index_name
        HAVING GROUP_CONCAT(s.column_name ORDER BY s.seq_in_index) = 'idTipoDoc_id,numDoc'
        """
    )
    for (index_name,) in cursor.fetchall():
        cursor.execute(f"ALTER TABLE pacientes DROP INDEX `{index_name}`")


def forwards(apps, schema_editor):
    if schema_editor.connection.vendor != "mysql":
        return

    with schema_editor.connection.cursor() as cursor:
        for table_name in ("comentarios", "random_hc"):
            if _table_exists(cursor, table_name):
                cursor.execute(f"DROP TABLE `{table_name}`")

        cursor.execute(
            f"ALTER DATABASE `{schema_editor.connection.settings_dict['NAME']}` "
            f"CHARACTER SET {TARGET_CHARSET} COLLATE {TARGET_COLLATION}"
        )

        if _table_exists(cursor, "pacientes"):
            cursor.execute(
                "ALTER TABLE pacientes MODIFY idTipoDoc_id bigint(20) NOT NULL DEFAULT 1"
            )
            cursor.execute("ALTER TABLE pacientes MODIFY obraSocial varchar(50) NULL")
            cursor.execute("ALTER TABLE pacientes MODIFY afiliado varchar(50) NULL")
            cursor.execute("ALTER TABLE pacientes MODIFY telefono varchar(50) NULL")
            cursor.execute("ALTER TABLE pacientes MODIFY celular varchar(50) NULL")
            cursor.execute("ALTER TABLE pacientes MODIFY profesion varchar(50) NULL")
            _drop_unique_paciente_doc(cursor)
            if not _index_exists(cursor, "pacientes", "nombre_apellido_idx"):
                cursor.execute(
                    "ALTER TABLE pacientes ADD FULLTEXT INDEX nombre_apellido_idx (nombre, apellido)"
                )

        if _table_exists(cursor, "indicaciones_visitas"):
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM indicaciones_visitas iv
                LEFT JOIN historias_clinicas hc ON hc.id = iv.historia_clinica_id
                WHERE hc.id IS NULL
                """
            )
            orphan_count = cursor.fetchone()[0]
            if orphan_count:
                raise RuntimeError(
                    "No se puede agregar FK a indicaciones_visitas: "
                    f"hay {orphan_count} filas huerfanas."
                )
            if not _index_exists(cursor, "indicaciones_visitas", "indicaciones_fecha_idx"):
                cursor.execute(
                    "ALTER TABLE indicaciones_visitas ADD INDEX indicaciones_fecha_idx (fecha)"
                )
            if not _foreign_key_exists(
                cursor,
                "indicaciones_visitas",
                "indicaciones_visitas_historia_clinica_id_d87c8a7b_fk_historias",
            ):
                cursor.execute(
                    """
                    ALTER TABLE indicaciones_visitas
                    ADD CONSTRAINT indicaciones_visitas_historia_clinica_id_d87c8a7b_fk_historias
                    FOREIGN KEY (historia_clinica_id) REFERENCES historias_clinicas(id)
                    """
                )

        for table_name in TARGET_TABLES:
            if _table_exists(cursor, table_name):
                cursor.execute(
                    f"ALTER TABLE `{table_name}` CONVERT TO CHARACTER SET "
                    f"{TARGET_CHARSET} COLLATE {TARGET_COLLATION}"
                )


class Migration(migrations.Migration):

    dependencies = [
        ("carotidas", "0004_alter_carotidasestudio_com_derecha_and_more"),
        ("ecocardiograma", "0002_alter_conclusiónecocardiograma_comentario_concordancia_and_more"),
        ("ecostress", "0003_alter_ecostressestudio_conclusion_and_more"),
        ("main", "0003_rename_idpaciente_idx_historia_paciente_idx_and_more"),
        ("mmii", "0004_alter_mmiiestudio_art_fem_comun_derecha_and_more"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(forwards, migrations.RunPython.noop),
            ],
            state_operations=[
                migrations.AlterUniqueTogether(
                    name="paciente",
                    unique_together=set(),
                ),
            ],
        ),
    ]
