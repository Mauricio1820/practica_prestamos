from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


DIAS_MAXIMOS_ESTUDIANTE = 7
LIMITE_EQUIPOS_ESTUDIANTE = 2


class PrestamoPrestamo(models.Model):
    _name = "prestamo.prestamo"
    _description = "Préstamo de equipo"
    _inherit = ["mail.thread"]
    _order = "fecha_prestamo desc, id desc"

    name = fields.Char(string="Motivo", required=True)
    partner_id = fields.Many2one("res.partner", string="Solicitante", required=True)
    tipo_solicitante = fields.Selection(
        [("estudiante", "Estudiante"), ("docente", "Docente")],
        string="Tipo de solicitante",
        required=True,
        default="estudiante",
    )
    fecha_prestamo = fields.Date(
        string="Fecha de préstamo", required=True, default=fields.Date.context_today
    )
    fecha_devolucion = fields.Date(string="Fecha de devolución", required=True)
    state = fields.Selection(
        [
            ("borrador", "Borrador"),
            ("prestado", "Prestado"),
            ("devuelto", "Devuelto"),
            ("atrasado", "Atrasado"),
        ],
        string="Estado",
        required=True,
        default="borrador",
        tracking=True,
    )

    linea_ids = fields.One2many("prestamo.linea", "prestamo_id", string="Equipos")
    cantidad_equipos = fields.Integer(
        string="Cantidad de equipos", compute="_compute_cantidad_equipos", store=True
    )
    dias_prestamo = fields.Integer(
        string="Días de préstamo", compute="_compute_dias_prestamo", store=True
    )

    @api.depends("linea_ids")
    def _compute_cantidad_equipos(self):
        for prestamo in self:
            prestamo.cantidad_equipos = len(prestamo.linea_ids)

    @api.depends("fecha_prestamo", "fecha_devolucion")
    def _compute_dias_prestamo(self):
        for prestamo in self:
            if prestamo.fecha_prestamo and prestamo.fecha_devolucion:
                dias = (prestamo.fecha_devolucion - prestamo.fecha_prestamo).days
                prestamo.dias_prestamo = dias
            else:
                prestamo.dias_prestamo = 0

    def action_prestar(self):
        for prestamo in self:
            if prestamo.state != "borrador":
                raise UserError("Solo se puede prestar un préstamo en borrador.")
            if not prestamo.linea_ids:
                raise UserError("Agregue al menos un equipo al préstamo.")
            if prestamo.tipo_solicitante == "estudiante" and len(prestamo.linea_ids) > LIMITE_EQUIPOS_ESTUDIANTE:
                raise UserError(f"Un estudiante puede llevar hasta {LIMITE_EQUIPOS_ESTUDIANTE} equipos.")
            for equipo in prestamo.linea_ids.equipo_id:
                if equipo.estado != "disponible":
                    raise UserError(f"El equipo {equipo.name} ya no está disponible.")
            prestamo.linea_ids.equipo_id.write({"estado": "prestado"})
            prestamo.state = "prestado"
            prestamo.message_post(
                body=f"Se prestaron {prestamo.cantidad_equipos} equipo(s) "
                     f"a {prestamo.partner_id.name}."
            )

    def action_devolver(self):
        for prestamo in self:
            if prestamo.state not in ("prestado", "atrasado"):
                raise UserError("Solo se puede devolver un préstamo activo.")
            prestamo.linea_ids.equipo_id.write({"estado": "disponible"})
            prestamo.state = "devuelto"
            prestamo.message_post(body="Los equipos fueron devueltos.")

    @api.constrains("fecha_prestamo", "fecha_devolucion", "tipo_solicitante")
    def _check_fechas(self):
        for prestamo in self:
            dias = (prestamo.fecha_devolucion - prestamo.fecha_prestamo).days
            if dias < 0:
                raise ValidationError("La devolución no puede ser anterior al préstamo.")
            if prestamo.tipo_solicitante == "estudiante" and dias > DIAS_MAXIMOS_ESTUDIANTE:
                raise ValidationError(f"Un estudiante puede llevar el equipo hasta {DIAS_MAXIMOS_ESTUDIANTE} días.")

    @api.constrains("linea_ids")
    def _check_equipos_repetidos(self):
        for prestamo in self:
            if len(prestamo.linea_ids) != len(set(prestamo.linea_ids.equipo_id.ids)):
                raise ValidationError("El mismo equipo aparece dos veces en el préstamo.")
