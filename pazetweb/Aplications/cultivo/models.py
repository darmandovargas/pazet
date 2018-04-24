# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.gis.db import models as Geomodels
from Aplications.orgtecol.models import Municipio
from django.db import models

TIPO_CULTIVO_CHOICES=(('Herbáseos Frutas y Granos','Herbáseos Frutas y Granos'),('Herbáseos Vegetales de Hoja','Herbáseos Vegetales de Hoja'),('Herbáseos Raices y Tuberculos','Herbáseos Raices y Tuberculos'),('Herbáseos Cultivos Forrajeros','Herbáseos Cultivos Forrajeros'),('Arbóreos','Arbóreos'),)
# Entidades con base en el diagrama entidad relación de éste link https://creately.com/diagram/jf8m2e4f1/U2DcDvIRWlTIsZRmVhb0niDZBIg%3D
class Cultivo(models.Model):
    cul_id = models.BigAutoField(primary_key=True)
    cul_nombre = models.CharField("Tipo de Cultivo", max_length=50)
    cul_variedad = models.CharField("Tipo de Cultivo", blank=True, null=True, max_length=50)
    cul_nombre_cientifico = models.CharField("Tipo de Cultivo", blank=True, null=True, max_length=50)
    cul_nombre_bernaculo = models.CharField("Tipo de Cultivo", blank=True, null=True, max_length=50)
    cul_tipo_cultivo=models.CharField("",max_length=100,null=False,default="",choices=TIPO_CULTIVO_CHOICES)
    cul_created = models.DateTimeField("Registro", auto_now_add=True)
    cul_updated = models.DateTimeField("Actualización", auto_now=True)
    municipios = models.ManyToManyField(Municipio, through="RegionCultivo", related_name="cultivos")

    def __unicode__(self):
        return '{}'.format(self.cul_nombre)

    class Meta:
        managed = True
        db_table = 'cultivo'
        verbose_name = 'Cultivo'
        verbose_name_plural = 'Cultivos'

class RegionCultivo(models.Model):
    regcul_id = models.BigAutoField(primary_key=True)
    cul = models.ForeignKey(Cultivo, verbose_name="Cultivo", related_name='regioncultivo')
    mun = models.ForeignKey(Municipio, verbose_name="Municipio", related_name='regioncultivo')
    cul_created = models.DateTimeField("Registro", auto_now_add=True)
    cul_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.regcul_id)

    class Meta:
        managed = True
        db_table = 'cul_region_cultivo'
        verbose_name = 'Región Cultivo'
        verbose_name_plural = 'Regiones Cultivo'

class NivelFreatico(models.Model):
    nivfre_id = models.BigAutoField(primary_key=True)
    nivfre_nombre = models.CharField("Tipo de Cultivo", max_length=50)
    nivfre_coordenadas = Geomodels.PointField("Coordenadas Nivel Freático", srid=4326, help_text="Seleccione un punto de ubicación")
    nivfre_altitud = models.IntegerField("Altitud", blank=True, null=True)
    mun = models.ForeignKey(Municipio, verbose_name="Municipio")
    nivfre_created = models.DateTimeField("Registro", auto_now_add=True)
    nivfre_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.nivfre_nombre)


    class Meta:
        managed = True
        db_table = 'cul_nivel_freatico'
        verbose_name = 'Nivel Freático'
        verbose_name_plural = 'Niveles Freáticos'

class FechaSiembra(models.Model):
    fecsiem_id = models.BigAutoField(primary_key=True)
    cul = models.ForeignKey(Cultivo, verbose_name="Cultivo")
    fecsiem_fecha_siembra = models.DateField("Fecha Siembra")
    fecsiem_created = models.DateTimeField("Registro", auto_now_add=True)
    fecsiem_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.fecsiem_id)

    class Meta:
        managed = True
        db_table = 'cul_fecha_siembra'
        verbose_name = 'Fecha Siembra'
        verbose_name_plural = 'Fechas Siembras'

class AqFisioConserva(models.Model):
    aqfisoconser_id = models.BigAutoField(primary_key=True)
    cul_id = models.OneToOneField(Cultivo)
    aqfisioconser_Temp_base = models.FloatField("Temperatura Mínima", blank=True, null=True)
    aqfisioconser_Temp_corte = models.FloatField("Temperatura de Corte", blank=True, null=True)
    aqfisioconser_cs = models.FloatField("Covertura de Suelo", blank=True, null=True)
    aqfisioconser_ccd = models.FloatField("Coeficiente de Crecimiento de Dosel", blank=True, null=True)
    aqfisioconser_cdd = models.FloatField("Coeficiente de Declinación Dosel", blank=True, null=True)
    aqfisioconser_if = models.FloatField("Longitud del Estado de Flotación", blank=True, null=True)
    aqfisioconser_determinancia = models.SmallIntegerField("Determinancia")
    aqfisioconser_nr = models.FloatField("Factor de Forma", blank=True, null=True)
    aqfisioconser_stres_frutas = models.FloatField("Estres de Frutas Potenciales", blank=True, null=True)
    aqfisioconser_kcbx = models.FloatField("Coeficiente para la Transpiración del Cultivo Máximo", blank=True, null=True)
    aqfisioconser_fedad = models.FloatField("Factor de Declinación del Cultivo Máximo", blank=True, null=True)
    aqfisioconser_erel = models.FloatField("Efecto de la Cobertura del Dosel", blank=True, null=True)
    aqfisioconser_sx_top = models.FloatField("Máxima Extracción de Agua Superior", blank=True, null=True)
    aqfisioconser_sx_bot = models.FloatField("Máxima Extracción de Agua Inferior", blank=True, null=True)
    aqfisioconser_wpnormal = models.FloatField("Productividad hídrica ET0 y CO2")
    aqfisioconser_wpnormal_cosecha = models.FloatField("Productividad Hídrica Formación", blank=True, null=True)
    aqfisioconser_suma_et0estres = models.FloatField("Sumatoria de ET0", blank=True, null=True)
    aqfisioconser_ro_exp_super = models.FloatField("Umbral de Agotamiento Superior", blank=True, null=True)
    aqfisioconser_ro_exp_inferior = models.FloatField("Umbral de Agotamiento Inferior", blank=True, null=True)
    aqfisioconser_f_exp = models.FloatField("Factor de Forma Expansión del Dosel", blank=True, null=True)
    aqfisioconser_ro_sto = models.FloatField("Umbral de Agotamiento Estomatal", blank=True, null=True)
    aqfisioconser_f_sto = models.FloatField("Factor de Forma Estomático", blank=True, null=True)
    aqfisioconser_ro_sen_superior = models.FloatField("Umbral de Agotamiento Senescencia del Dosel", blank=True, null=True)
    aqfisioconser_f_sen = models.FloatField("Factor de Forma para Estrés Hídrico", blank=True, null=True)
    aqfisioconser_tipo_fruto =  models.SmallIntegerField("Tipo Fruto")
    aqfisioconser_tipo_siembra = models.SmallIntegerField("Tipo Siembra")
    aqfisioconser_ro = models.FloatField("Factor de Agotamiento de Agua en el Suelo", blank=True, null=True)
    aqfisioconser_ro_pol_super = models.FloatField("Umbral de Agotamiento de Agua", blank=True, null=True)
    aqfisioconser_incre_icxstresagua = models.FloatField("Posible Incremento de IC", blank=True, null=True)
    aqfisioconser_coef_crece_vegeta_cosecha = models.FloatField("Coeficiente Impacto Positivo", blank=True, null=True)
    aqfisioconser_increx_ic = models.FloatField("Incremento Máximo IC", blank=True, null=True)
    aqfisioconser_tmin_reducepol = models.FloatField("Temperatura Mínima del Aire", blank=True, null=True)
    aqfisioconser_tmax_reducepol = models.FloatField("Temperatura Máxima del Aire", blank=True, null=True)
    aqfisioconser_mincrecerxabimomas = models.FloatField("Mínimo Crecimiento Requerido", blank=True, null=True)
    aqfisioconser_created = models.DateTimeField("Registro", auto_now_add=True)
    aqfisioconser_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.aqfisoconser_id)

    class Meta:
        managed = True
        db_table = 'cul_aq_fisiologia_conservadoras'
        verbose_name = 'AQ Fisiologia Conservadora'
        verbose_name_plural = 'AQ Fisiologias Conservadoras'

class AqFisioNoConser(models.Model):
    aqfisonoconser_id = models.BigAutoField(primary_key=True)
    cul = models.ForeignKey(Cultivo, verbose_name="Cultivo")
    mun_id = models.OneToOneField(Municipio)
    aqfisionoconser_plantasxha = models.FloatField("Densidad de Siembra", blank=True, null=True)
    aqfisionoconser_t0 = models.SmallIntegerField("Tiempo Transcurrido")
    aqfisionoconser_cdx = models.SmallIntegerField("Máxima cobertura")
    aqfisionoconser_ts = models.FloatField("Tiempo de Siembra Inicio", blank=True, null=True)
    aqfisionoconser_tm = models.FloatField("Tiempo de Siembra Madurez", blank=True, null=True)
    aqfisionoconser_tf = models.FloatField("Tiempo de Siembra Floración", blank=True, null=True)
    aqfisionoconser_z0 = models.FloatField("Profundidad Mínima", blank=True, null=True)
    aqfisionoconser_zx = models.FloatField("Profundidad Máxima", blank=True, null=True)
    aqfisionoconser_txr = models.SmallIntegerField("Tiempo desde Siembra")
    aqfisionoconser_ic0 = models.FloatField("Inicio de Cosecha", blank=True, null=True)
    aqfisionoconser_tic = models.FloatField("Tiempo Requerido", blank=True, null=True)
    aqfisionoconser_teta_aer = models.FloatField("Porcentaje de Humedad", blank=True, null=True)
    aqfisionoconser_stres_fertil = models.FloatField("Estrés Fertilidad", blank=True, null=True)
    aqfisionoconser_ffertil_expdosel = models.FloatField("Coeficiente de Factor de Forma Expansión Dosel", blank=True, null=True)
    aqfisionoconser_ffertil_doselx = models.FloatField("Coeficiente de Factor de Forma Máxima Dosel", blank=True, null=True)
    aqfisonoconser_ffertil_wp = models.FloatField("Coeficiente de Factor de Forma Productividad Hídrica", blank=True, null=True)
    aqfisionoconser_ffertil_declinadosel = models.FloatField("Factor de Forma Cobertura Dosel", blank=True, null=True)
    aqfisionoconser_created = models.DateTimeField("Registro", auto_now_add=True)
    aqfisionoconser_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.aqfisonoconser_id)

    class Meta:
        managed = True
        db_table = 'cul_aq_fisiologia_noconservadoras'
        verbose_name = 'AQ Fisiologia No Conservadora'
        verbose_name_plural = 'AQ Fisiologias No Conservadoras'

class ReqNutricion(models.Model):
    reqnut_id = models.BigAutoField(primary_key=True)
    cul_id = models.OneToOneField(Cultivo)
    reqnut_ph_min = models.FloatField("Ph Mínimo", blank=True, null=True)
    reqnut_ph_max = models.FloatField("Ph Máximo", blank=True, null=True)
    reqnut_ce_min = models.FloatField("Conductividad Eléctrica Mínima", blank=True, null=True)
    reqnut_ce_max = models.FloatField("Conductividad Eléctrica Máxima", blank=True, null=True)
    reqnut_sat_alt_min = models.FloatField("Saturación Mínimo", blank=True, null=True)
    reqnut_sat_alt_max = models.FloatField("Saturación Máximo", blank=True, null=True)
    reqnut_al_inter_min = models.FloatField("Aluminio Mínimo", blank=True, null=True)
    reqnut_al_inter_max = models.FloatField("Aluminio Máximo", blank=True, null=True)
    reqnut_mo_min = models.FloatField("Materia Orgánica Mínima", blank=True, null=True)
    reqnut_mo_max = models.FloatField("Materia Orgánica Máxima", blank=True, null=True)
    reqnut_p_min = models.FloatField("Mínimo Nivel Fósforo", blank=True, null=True)
    reqnut_p_max = models.FloatField("Máximo Nivel Fósforo", blank=True, null=True)
    reqnut_s_min = models.FloatField("Mínimo Nivel Azufre", blank=True, null=True)
    reqnut_s_max = models.FloatField("Máximo Nivel Azufre", blank=True, null=True)
    reqnut_k_min = models.FloatField("Mínimo Nivel Potasio", blank=True, null=True)
    reqnut_k_max = models.FloatField("Máximo Nivel Potasio", blank=True, null=True)
    reqnut_ca_min = models.FloatField("Mínimo Nivel Calcio", blank=True, null=True)
    reqnut_ca_max = models.FloatField("Máximo Nivel Calcio", blank=True, null=True)
    reqnut_mg_min = models.FloatField("Mínimo Nivel Magnesio", blank=True, null=True)
    reqnut_mg_max = models.FloatField("Máximo Nivel Magnesio", blank=True, null=True)
    reqnut_fe_min = models.FloatField("Mínimo Hierro", blank=True, null=True)
    reqnut_fe_max = models.FloatField("Máximo Hierro", blank=True, null=True)
    reqnut_mn_min = models.FloatField("Mínimo Manganeso", blank=True, null=True)
    reqnut_mn_max = models.FloatField("Máximo Manganeso", blank=True, null=True)
    reqnut_cu_min =  models.FloatField("Mínimo Cobre", blank=True, null=True)
    reqnut_cu_max = models.FloatField("Máximo Cobre", blank=True, null=True)
    reqnut_b_min = models.FloatField("Mínimo Boro", blank=True, null=True)
    reqnut_b_max = models.FloatField("Máximo boro", blank=True, null=True)
    reqnut_co_min = models.FloatField("Mínimo Carbono", blank=True, null=True)
    reqnut_co_max = models.FloatField("Máximo Carbono", blank=True, null=True)
    reqnut_Acidez_min = models.FloatField("Acidez Mínima", blank=True, null=True)
    reqnut_Acidez_max = models.FloatField("Acidez Máxima", blank=True, null=True)
    reqnut_na_min = models.FloatField("Sódio Mínimo", blank=True, null=True)
    reqnut_na_max = models.FloatField("Sódio Máximo", blank=True, null=True)
    reqnut_z_min = models.FloatField("Zinc Mínimo", blank=True, null=True)
    reqnut_z_max = models.FloatField("Zinc Máximo", blank=True, null=True)
    reqnut_created = models.DateTimeField("Registro", auto_now_add=True)
    reqnut_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.reqnut_id)

    class Meta:
        managed = True
        db_table = 'cul_req_nutricion'
        verbose_name = 'Requisito Nutrición'
        verbose_name_plural = 'Requisitos Nutrición'

class ReqFisico(models.Model):
    reqfis_id = models.BigAutoField(primary_key=True)
    cul_id = models.OneToOneField(Cultivo)
    reqfis_drenaje_opt = models.CharField("Clase de Drenaje Óptimo", blank=True, null=True, max_length=15)
    reqfis_drenaje_mod = models.CharField("Clase de Drenaje Moderado", blank=True, null=True, max_length=15)
    reqfis_drenaje_rest = models.CharField("Clase de Drenaje Restrictivo", blank=True, null=True, max_length=15)
    reqfis_pendient_opt = models.FloatField("Pendiente Óptima", blank=True, null=True)
    reqfis_pendient_mod = models.FloatField("Pendiente Moderada", blank=True, null=True)
    reqfis_pendient_rest = models.FloatField("Pendiente Restrictiva", blank=True, null=True)
    reqfis_profectiva_opt = models.FloatField("Profundidad Óptima", blank=True, null=True)
    reqfis_profectiva_mod = models.FloatField("Profundidad Moderada", blank=True, null=True)
    reqfis_profectiva_rest = models.FloatField("Profundidad Restrictiva", blank=True, null=True)
    reqfis_textura_opt = models.CharField("Textura Óptima", max_length=15)
    reqfis_textura_mod = models.CharField("Textura Moderada", max_length=15)
    reqfis_textura_rest = models.CharField("Textura Restringida", max_length=15)
    reqfis_created = models.DateTimeField("Registro", auto_now_add=True)
    reqfis_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.reqfis_id)

    class Meta:
        managed = True
        db_table = 'cul_req_fisico'
        verbose_name = 'Requisito Físico'
        verbose_name_plural = 'Requisitos Físicos'

class TipoRiego(models.Model):
    tiporiego_id = models.BigAutoField(primary_key=True)
    cul = models.ForeignKey(Cultivo, verbose_name="Cultivo")
    tiporiego_metodo = models.SmallIntegerField("Tipo Riego Método", blank=True, null=True)
    tiporiego_humedecimiento = models.FloatField("Profundidad Moderada", blank=True, null=True)
    tiporiego = models.SmallIntegerField("Superficie de Suelo Humedecido")
    tiporiego_created = models.DateTimeField("Registro", auto_now_add=True)
    tiporiego_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.tiporiego_id)

    class Meta:
        managed = True
        db_table = 'cul_tipo_riego'
        verbose_name = 'Tipo de Riego'
        verbose_name_plural = 'Tipos de Riegos'

class EventoRiego(models.Model):
    eventoriego_id = models.BigAutoField(primary_key=True)
    tiporiego = models.ForeignKey(TipoRiego, verbose_name="Tipo de Riego")
    eventoriego_n = models.SmallIntegerField("Número de Eventos")
    eventoriego_dia_n = models.CharField("Día Riego", max_length=200)
    eventoriego_lamina_n = models.CharField("Lámina Aplicada", blank=True, null=True, max_length=200)
    eventoriego_cew_n = models.CharField("Conductividad Eléctrica", blank=True, null=True, max_length=200)
    eventoriego_gen_crit_tiempo = models.SmallIntegerField("Criterio de Tiempo", blank=True, null=True)
    eventoriego_gen_crit_lamina = models.SmallIntegerField("Criterio de Lámina", blank=True, null=True)
    eventoriego_gen_n = models.SmallIntegerField("Número de Eventos")
    eventoriego_gen_desdedia_n = models.CharField("Día Criterio Riego", blank=True, null=True, max_length=200)
    eventoriego_gen_intervalo_n = models.CharField("Intervalo Criterio Riego", blank=True, null=True, max_length=200)
    eventoriego_gen_lamina_n = models.CharField("Lámina de Aplicación", blank=True, null=True, max_length=200)
    eventoriego_gen_cew_n = models.CharField("Conductividad Eléctrica Riego", blank=True, null=True, max_length=200)
    eventoriego_req_agotamiento = models.FloatField("Agotamiento Permitido",  blank=True, null=True)
    eventoriego_created = models.DateTimeField("Registro", auto_now_add=True)
    eventoriego_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.eventoriego_id)

    class Meta:
        managed = True
        db_table = 'cul_evento_riego'
        verbose_name = 'Evento Riego'
        verbose_name_plural = 'Eventos Riegos'