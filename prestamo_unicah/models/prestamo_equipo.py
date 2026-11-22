from odoo import api, fields, models


class PrestamoEquipo(models.Model):
    _name = "prestamo.equipo"
    _description = "Equipo para préstamo"

    name = fields.Char(string="Nombre", required=True)
    codigo = fields.Char(string="Código de inventario", required=True, copy=False)
    categoria = fields.Selection(
        [
            ("laptop", "Laptop"),
            ("proyector", "Proyector"),
            ("audio", "Audio"),
            ("laboratorio", "Laboratorio"),
        ],
        string="Categoría",
        required=True,
        default="laptop",
    )
    estado = fields.Selection(
        [
            ("disponible", "Disponible"),
            ("prestado", "Prestado"),
            ("mantenimiento", "En mantenimiento"),
        ],
        string="Estado",
        required=True,
        default="disponible",
        group_expand=True,
    )
    linea_ids = fields.One2many("prestamo.linea", "equipo_id", string="Líneas de préstamo")
    veces_prestado = fields.Integer(string="Veces prestado", compute="_compute_veces_prestado")
    notas = fields.Text(string="Notas")
    active = fields.Boolean(string="Activo", default=True)

    @api.depends("linea_ids.prestamo_id")
    def _compute_veces_prestado(self):
        for equipo in self:
            equipo.veces_prestado = len(equipo.linea_ids.prestamo_id)
