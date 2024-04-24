import json
import logging


from src.models.db import db_session
from src.models.deporte import Deporte
from src.models.deportista import Deportista
from src.models.ejercicio_deporte import EjercicioDeporte
from src.models.menu import Menu
from src.models.plan import Plan
from src.models.plan_alimenticio import PlanAlimenticio
from src.models.plan_deportista import PlanDeportista
from src.models.plan_ejercicio import PlanEjercicio
from src.models.resultado_sesion import ResultadoSesion
from src.models.sesion import EstadoSesionEnum, Sesion
from src.models.tipo_plan_alimenticio import TipoPlanAlimenticio
from src.models.plan_subscripcion import PlanSubscripcion
from src.models.detalle_subscripcion import DetalleSubscripcion


logger = logging.getLogger(__name__)


def precargar_informacion():
    _precargar_deporte()
    _precargar_plan()
    _precargar_ejercicio_deporte()
    _precargar_plan_ejercicio()
    _precargar_tipo_plan_alimenticio()
    _precargar_menu()
    _precargar_plan_alimenticio()
    _precargar_plan_subscripcion()
    _precargar_detalle_subscripcion()

    _precargar_deportista()
    _precargar_plan_deportista()

    _precargar_sesiones()


def _precargar_deporte():
    if not Deporte.query.all():
        deportes = ["Atletismo", "Ciclismo"]
        for deporte in deportes:
            db_session.add(Deporte(nombre=deporte))
        db_session.commit()
        print("Deportes precargados")


def _precargar_plan():
    if not Plan.query.all():
        with open("cfg/plan.json", encoding="utf-8") as plan_file:
            plan_cfg = json.load(plan_file)

        for plan in plan_cfg['planes']:
            db_session.add(Plan(**plan))

        db_session.commit()
        print("Planes precargados")


def _precargar_ejercicio_deporte():
    if not EjercicioDeporte.query.all():
        atletismo: Deporte = Deporte.query.filter_by(
            nombre="Atletismo").first()
        ciclismo: Deporte = Deporte.query.filter_by(nombre="Ciclismo").first()

        with open("cfg/ejercicios.json", encoding="utf-8") as ejercicios_file:
            ejercicios_cfg = json.load(ejercicios_file)

        for ejercicio in ejercicios_cfg['atletismo']:
            ejercicio["id_deporte"] = atletismo.id
            db_session.add(EjercicioDeporte(**ejercicio))

        for ejercicio in ejercicios_cfg['ciclismo']:
            ejercicio["id_deporte"] = ciclismo.id
            db_session.add(EjercicioDeporte(**ejercicio))

        db_session.commit()
        print("Ejercicios de deporte precargados")


def _precargar_plan_ejercicio():
    if not PlanEjercicio.query.all():
        with open("cfg/plan_ejercicios.json", encoding="utf-8") as plan_ejercicios_file:
            plan_ejercicios_cfg = json.load(plan_ejercicios_file)

        for cfg in plan_ejercicios_cfg['planes']:
            plan: Plan = Plan.query.filter_by(
                nombre=cfg['nombre_plan']).first()

            for ejercicio in cfg['ejercicios']:
                tmp: EjercicioDeporte = EjercicioDeporte.query.filter_by(
                    nombre=ejercicio).first()

                nuevo_ejercicio = {
                    "id_plan": plan.id,
                    "orden": cfg['ejercicios'].index(ejercicio),
                    "id_ejercicio_deporte": tmp.id
                }

                db_session.add(PlanEjercicio(**nuevo_ejercicio))
        db_session.commit()
        print("Planes de ejercicio precargados")


def _precargar_tipo_plan_alimenticio():
    if not TipoPlanAlimenticio.query.all():
        tipos = ["Estándar", "Vegetariano", "Vegano"]
        for tipo in tipos:
            db_session.add(TipoPlanAlimenticio(nombre=tipo))
        db_session.commit()
        print("Tipos de plan alimenticio precargados")


def _precargar_menu():
    if not Menu.query.all():
        with open("cfg/menu.json", encoding="utf-8") as menu_file:
            menu_cfg = json.load(menu_file)

        for menu in menu_cfg['menus']:
            del menu["tipo_menu"]
            db_session.add(Menu(**menu))
        db_session.commit()
        print("Menús precargados")


def _precargar_plan_alimenticio():
    if not PlanAlimenticio.query.all():
        with open("cfg/plan_alimenticio.json", encoding="utf-8") as plan_alimenticio_file:
            plan_alimenticio_cfg = json.load(plan_alimenticio_file)

        for cfg in plan_alimenticio_cfg['planes']:
            plan: Plan = Plan.query.filter_by(
                nombre=cfg['plan']).first()

            tipo_plan_alimenticio: TipoPlanAlimenticio = TipoPlanAlimenticio.query.filter_by(
                nombre=cfg['tipo_menu']).first()

            for menu in cfg['menus']:
                tmp: Menu = Menu.query.filter_by(nombre=menu).first()

                nuevo_plan_menu = {
                    "id_tipo_plan_alimenticio": tipo_plan_alimenticio.id,
                    "id_menu": tmp.id,
                    "id_plan": plan.id,
                }

                db_session.add(PlanAlimenticio(**nuevo_plan_menu))
        db_session.commit()
        print("Planes alimenticios precargados")


def _precargar_plan_subscripcion():
    if not PlanSubscripcion.query.all():
        planesSubs = ["Gratis", "Intermedio", "Premium"]
        for planes in planesSubs:
            db_session.add(PlanSubscripcion(nombre=planes))
        db_session.commit()
        print("Planes de Subscripcion precargados")


def _precargar_detalle_subscripcion():
    if not DetalleSubscripcion.query.all():
        with open("cfg/detalle_subscripcion.json", encoding="utf-8") as detalle_subscripcion_file:
            detalle_subscripcion_cfg = json.load(detalle_subscripcion_file)

        for cfg in detalle_subscripcion_cfg['detalle_subscripcion']:
            planSubscripcion: PlanSubscripcion = PlanSubscripcion.query.filter_by(
                nombre=cfg['nombre']).first()

            db_session.add(DetalleSubscripcion(
                id_plan_subscripcion=planSubscripcion.id, beneficios=cfg['beneficios']))
        db_session.commit()
        print("Detalles de subscripcion precargados")


def _precargar_deportista():
    if not Deportista.query.all():
        with open("cfg/deportista.json", encoding="utf-8") as deportista_file:
            deportista_cfg = json.load(deportista_file)

        for deportista in deportista_cfg['deportistas']:

            ps: PlanSubscripcion = PlanSubscripcion.query.filter_by(
                nombre=deportista['plan_subscripcion_nombre']).first()

            deportista['id_plan_subscripcion'] = ps.id

            db_session.add(Deportista(**deportista))
        db_session.commit()
        print("Deportistas precargados")


def _precargar_plan_deportista():
    if not PlanDeportista.query.all():
        with open("cfg/plan_deportista.json", encoding="utf-8") as plan_deportista_file:
            plan_deportista_cfg = json.load(plan_deportista_file)

        for cfg in plan_deportista_cfg['planes_deportistas']:
            plan: Plan = Plan.query.filter_by(
                nombre=cfg['nombre_plan']).first()

            deportista: Deportista = Deportista.query.filter_by(
                email=cfg['email_deportista']).first()

            db_session.add(PlanDeportista(
                id_deportista=deportista.id, id_plan=plan.id))
        db_session.commit()
        print("Planes deportistas precargados")


def _precargar_sesiones():
    if not Sesion.query.all():
        with open("cfg/sesiones.json", encoding="utf-8") as sesion_file:
            sesion_cfg = json.load(sesion_file)

        for sesion in sesion_cfg['sesiones']:
            plan: Plan = Plan.query.filter_by(
                nombre=sesion['nombre_plan_deportista']).first()

            plan_deportista: PlanDeportista = PlanDeportista.query.filter_by(
                id_plan=plan.id).first()

            nueva_sesion = Sesion(
                id_plan_deportista=plan_deportista.id,
                email=plan_deportista.deportista.email,
                estado=EstadoSesionEnum[sesion['estado']],
                fecha_sesion=sesion['fecha_sesion']
            )
            db_session.add(nueva_sesion)
            db_session.commit()

            resultado_sesion: ResultadoSesion = ResultadoSesion(
                id_sesion=nueva_sesion.id,
                fecha_inicio=sesion['resultado']['fecha_inicio'],
                fecha_fin=sesion['resultado']['fecha_fin'],
                vo2_max=sesion['resultado']['vo2_max'],
                ftp=sesion['resultado']['ftp']
            )

            db_session.add(resultado_sesion)
            db_session.commit()
        print("Sesiones precargadas")
