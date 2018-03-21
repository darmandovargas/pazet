# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.gis.db import models as Geomodels
from Aplications.entidades.models import EntdsEntidad
from Aplications.orgtecol.models import Departamento
from django.db import models

# Create your models here.
class SueloEstudio(models.Model):
    estu_id = models.SmallIntegerField(primary_key=True)
    depto = models.ForeignKey(Departamento, blank=True, null=True, db_column='depto_codigodane')
    entds = models.ForeignKey(EntdsEntidad, models.DO_NOTHING, blank=True, null=True)
    estu_nombre = models.CharField(max_length=200)
    estu_publicacion = models.SmallIntegerField(blank=True, null=True)
    estu_nivel_detalle = models.CharField(max_length=10, blank=True, null=True)
    estu_escala = models.CharField(max_length=10, blank=True, null=True)
    estu_created = models.DateTimeField(blank=True, null=True)
    estu_updated = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return '{}'.format(self.estu_nombre)

    class Meta:
        managed = False
        db_table = 'suelo_estudio'
        verbose_name = 'Estudio de suelo'
        verbose_name_plural = 'Estudios de suelo'


class SueloPerfil(models.Model):
    perf_codigo = models.CharField(max_length=50, primary_key=True)
    unca_codigo = models.SmallIntegerField(blank=True, null=True)
    estu = models.ForeignKey(SueloEstudio, blank=True, null=True)
    pend_id = models.SmallIntegerField(blank=True, null=True)
    dren_id = models.SmallIntegerField(blank=True, null=True)
    eros_id = models.SmallIntegerField(blank=True, null=True)
    prof_id = models.SmallIntegerField(blank=True, null=True)
    uso_id = models.SmallIntegerField(blank=True, null=True)
    fert_id = models.SmallIntegerField(blank=True, null=True)
    perf_perfil = models.CharField(max_length=100)
    perf_cod_obs = models.CharField(max_length=50, blank=True, null=True)
    perf_coordenadas = Geomodels.PointField("Coordenadas", srid=4326, help_text="Hubicación del perfil")
    perf_fecha = models.DateField(blank=True, null=True)
    perf_taxonomia = models.CharField(max_length=100, blank=True, null=True)
    perf_sitio = models.CharField(max_length=100, blank=True, null=True)
    perf_altitud = models.FloatField(blank=True, null=True)
    perf_forma_terreno = models.CharField(max_length=100, blank=True, null=True)
    perf_clima_ambiental = models.CharField(max_length=100, blank=True, null=True)
    perf_ppt_avg_anual = models.CharField(max_length=100, blank=True, null=True)
    perf_clima_edafico = models.CharField(max_length=100, blank=True, null=True)
    perf_vegetacion_anual = models.CharField(max_length=100, blank=True, null=True)
    perf_limitantes_uso = models.CharField(max_length=100, blank=True, null=True)
    perf_inundaciones = models.CharField(max_length=100, blank=True, null=True)
    perf_nivel_freatico = models.CharField(max_length=100, blank=True, null=True)
    perf_created = models.DateTimeField(blank=True, null=True)
    perf_updated = models.DateTimeField(blank=True, null=True)

    @property
    def perf_lat(self):
        return float("{0:.3f}".format(self.perf_coordenadas.y))

    @property
    def perf_lng(self):
        return float("{0:.3f}".format(self.perf_coordenadas.x))

    def __unicode__(self):
        return '{}'.format(self.perf_codigo)

    class Meta:
        managed = False
        db_table = 'suelo_perfil'
        verbose_name = 'Perfil de suelo'
        verbose_name_plural = 'Perfiles de suelo'


class SueloHorizonte(models.Model):
    horz_nombre = models.CharField(unique=True, max_length=100, primary_key=True)
    horz_created = models.DateTimeField("Registro", auto_now_add=True)
    horz_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return '{}'.format(self.horz_nombre)

    class Meta:
        managed = False
        db_table = 'suelo_horizonte'
        verbose_name = 'Horizonte'
        verbose_name_plural = 'Horizontes'


class SueloMuestra(models.Model):
    mues_id = models.CharField(primary_key=True, max_length=50)
    perf = models.ForeignKey(SueloPerfil, blank=True, null=True, db_column='perf_codigo')
    horz = models.ForeignKey(SueloHorizonte, blank=True, null=True, db_column='horz_nombre')
    mues_prof_inicio = models.FloatField()
    mues_prof_final = models.FloatField()
    mues_coordenadas = Geomodels.PointField(srid=4326)
    mues_descripcion = models.TextField(blank=True, null=True)
    mues_created = models.DateTimeField("Registro", auto_now_add=True)
    mues_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return self.mues_id

    @property
    def mues_lat(self):
        return float("{0:.3f}".format(self.mues_coordenadas.y))

    @property
    def mues_lng(self):
        return float("{0:.3f}".format(self.mues_coordenadas.x))

    class Meta:
        managed = False
        db_table = 'suelo_muestra'
        verbose_name = 'Muestra'
        verbose_name_plural = 'Muestras'


class SueloPropfisica(models.Model):
    pfis_id = models.BigAutoField(primary_key=True)
    mues = models.OneToOneField(SueloMuestra, unique=True, verbose_name="Muestra")
    pfis_arena = models.FloatField("Arena", blank=True, null=True)
    pfis_limo = models.FloatField("Limo", blank=True, null=True)
    pfis_arcilla = models.FloatField("Arcilla", blank=True, null=True)
    pfis_textura = models.CharField("Textura", max_length=50, blank=True, null=True)
    pfis_densidad_aparante = models.FloatField("Densidad aparente", blank=True, null=True)
    pfis_interp_daparente = models.CharField("Interpretación DA", max_length=50, blank=True, null=True)
    pfis_densidad_real = models.FloatField("Densidad real", blank=True, null=True)
    pfis_interp_dreal = models.CharField("Interpretación DR", max_length=50, blank=True, null=True)
    pfis_porosidad_total = models.FloatField("Porosidad total", blank=True, null=True)
    pfis_interp_pdad_total = models.CharField("Interpretación PT", max_length=50, blank=True, null=True)
    pfis_w_sat_g = models.FloatField("Saturación gravimetrica", blank=True, null=True)
    pfis_w_sat_v = models.FloatField("Saturación volumetrica", blank=True, null=True)
    pfis_d_4mm = models.FloatField("Agregados > 4", blank=True, null=True)
    pfis_d_2mm = models.FloatField("Agregados > 2", blank=True, null=True)
    pfis_d_1mm = models.FloatField("Agregados > 1", blank=True, null=True)
    pfis_d_05mm = models.FloatField("Agregados > 0.5", blank=True, null=True)
    pfis_d_may_025mm = models.FloatField("Agregados > 0.25", blank=True, null=True)
    pfis_d_men_025mm = models.FloatField("Agregados < 0.25", blank=True, null=True)
    pfis_dmp = models.FloatField("DMP", blank=True, null=True, help_text="Diametro medio ponderado")
    pfis_interp_dmp = models.CharField("Interpretación DMP", max_length=50, blank=True, null=True)
    pfis_w_01bar_cc = models.FloatField("Capacidad de campo", blank=True, null=True)
    pfis_w_1bar = models.FloatField("Ret. Hum. 1 Bar", blank=True, null=True, help_text="Retencion de humedad a 1 bar")
    pfis_w_15bar_pmp = models.FloatField("PMP", blank=True, null=True, help_text="Punto de marchites permanente")
    pfis_agua_aprovechable = models.FloatField("Agrua apro. v", blank=True, null=True, help_text="Agua aprovechable volumetrica")
    pfis_interp_aa = models.CharField("Interpretación AA", max_length=50, blank=True, null=True, help_text="Interpretación agua aprovechable")
    pfis_agua_aprovechable_gra = models.FloatField("Agua A. Gravimetrica",blank=True, null=True, help_text="Agua aprovechable gravimetrica")
    pfis_macroporos = models.FloatField("Macroporos", blank=True, null=True)
    pfis_interp_macroporos = models.CharField("Inter. Macroporos", max_length=50, blank=True, null=True, help_text="Interpretación macroporos")
    pfis_mesoporos = models.FloatField("Mesoporos", blank=True, null=True)
    pfis_interp_mesoporos = models.CharField("Interp. Mesoporos", max_length=50, blank=True, null=True, help_text="Interpretación mesoporos")
    pfis_microporos = models.FloatField("Microporos", blank=True, null=True)
    pfis_interp_microporos = models.CharField("Interp. Microporos", max_length=50, blank=True, null=True, help_text="Interpretación microporos")
    pfis_infil_basica = models.FloatField("Infiltración basica", blank=True, null=True)
    pfis_interp_infil_basica = models.CharField("Interp. Inf. Basica", max_length=50, blank=True, null=True, help_text="Interpretación infiltración basica")
    pfis_rmp = models.FloatField("RMP", blank=True, null=True, help_text="Resistencia mecanica a la penetración")
    pfis_interp_rmp = models.CharField("Interp. RMP", max_length=50, blank=True, null=True, help_text="Interpretación resistencia mecanica a la penetración")
    pfis_adt_mm = models.FloatField("Agua disponible lamina", blank=True, null=True, help_text="Agua disponible en lamina mm")
    pfis_ret_hmdd_10kpa = models.FloatField("Ret. humedad a 10 kpa", blank=True, null=True, help_text="Retención de humedad a 10 kpa")
    pfis_ret_hmdd_30kpa = models.FloatField("Ret. humedad a 30 kpa", blank=True, null=True, help_text="Retención de humedad a 30 kpa")
    pfis_ret_hmdd_100kpa = models.FloatField("Ret. humedad a 100 kpa", blank=True, null=True, help_text="Retención de humedad a 100 kpa")
    pfis_ret_hmdd_500kpa = models.FloatField("Ret. humedad a 500 kpa", blank=True, null=True, help_text="Retención de humedad a 500 kpa")
    pfis_ret_hmdd_1000kpa = models.FloatField("Ret. humedad a 1000 kpa", blank=True, null=True, help_text="Retención de humedad a 1000 kpa")
    pfis_ret_hmdd_1500kpa = models.FloatField("Ret. humedad a 1500 kpa", blank=True, null=True, help_text="Retención de humedad a 1500 kpa")
    pfis_created = models.DateTimeField("Registro", auto_now_add=True)
    pfis_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return self.mues

    class Meta:
        managed = False
        db_table = 'suelo_propfisica'
        verbose_name = 'Propiedad fisica'
        verbose_name_plural = 'Propiedades fisicas'


class SueloPropquimicaMayor(models.Model):
    pquim_id = models.BigAutoField(primary_key=True)
    mues = models.OneToOneField(SueloMuestra, models.DO_NOTHING, unique=True, verbose_name="Muestra")
    pquim_ph = models.FloatField("PH", blank=True, null=True)
    pquim_interp_ph = models.CharField("Interp. PH", max_length=50, blank=True, null=True, help_text="Interpretación PH")
    pquim_co = models.FloatField("Carbono organico", blank=True, null=True)
    pquim_interp_co = models.CharField("Interp. CO", max_length=50, blank=True, null=True, help_text="Interpretación Carbono Organico")
    pquim_mo = models.FloatField("Materia organica", blank=True, null=True)
    pquim_acidez = models.FloatField("AlH: Acidez", blank=True, null=True)
    pquim_interp_acidez = models.CharField("Interp. ALH", max_length=50, blank=True, null=True, help_text="Interpretación ALH: Acidez")
    pquim_aluminio_inter = models.FloatField("(Al) Aluminio inter.", blank=True, null=True, help_text="Aluminio intercambiable (cmol kg^-1)")
    pquim_interp_aluminio_inter = models.CharField("Interp. AL", max_length=50, blank=True, null=True, help_text="Interpretación AL")
    pquim_calcio_inter = models.FloatField("(Ca) Calcio inter.", blank=True, null=True, help_text="Calcio Intercambiable (cmol kg^-1)")
    pquim_interp_calcio_inter = models.CharField("Interp. Calcio", max_length=50, blank=True, null=True, help_text="Interpretación Calcio")
    pquim_magnesio_inter = models.FloatField("(Mg) Magnesio inter.", blank=True, null=True, help_text="Magnesio intercambiable")
    pquim_interp_magnesio_inter = models.CharField("Interp. Mg", max_length=50, blank=True, null=True, help_text="Interpretación Magnesio")
    pquim_potasio_inter = models.FloatField("(K) Potasio inter.", blank=True, null=True, help_text="Potasio intercambiable (cmol kg^-1)")
    pquim_interp_potasio_inter = models.CharField("Interp. Potasio", max_length=50, blank=True, null=True, help_text="Interpretación Potasio")
    pquim_sodio_inter = models.FloatField("(Na) Sodio inter.", blank=True, null=True, help_text="Sodio intercambiable")
    pquim_interp_sodio_inter = models.CharField("Interp. Sodio", max_length=50, blank=True, null=True, help_text="Interpretación Sodio")
    pquim_cice = models.FloatField("CICE", blank=True, null=True, help_text="Capacidad de intercambio catiónico efectiva")
    pquim_interp_cice = models.CharField("Interp. CICE", max_length=50, blank=True, null=True, help_text="Interpretación CICE")
    pquim_conduc_electrica = models.FloatField("(CE)Conduc. Eelc.", blank=True, null=True, help_text="Conductividad electrica (dS m^-1)")
    pquim_interp_conduc_electrica = models.CharField("Interp. Conduc. electrica", max_length=50, blank=True, null=True, help_text="Interpretación conductividad electrica")
    pquim_sat_cal = models.FloatField("Sat. Calcio", blank=True, null=True, help_text="Saturación de calcio (%)")
    pquim_interp_sat_cal = models.CharField("Interp. Sat. Calcio", max_length=50, blank=True, null=True, help_text="Interpretación saturación de calcio")
    pquim_sat_mag = models.FloatField("Sat. Magnesio", blank=True, null=True, help_text="Saturación magnesio (%)")
    pquim_interp_sat_mag = models.CharField("Interp. Sat. Mag.", max_length=50, blank=True, null=True, help_text="Interpretación saturación de magnesio")
    pquim_sat_sodio = models.FloatField("Sat. Sodio", blank=True, null=True, help_text="Saturación de sodio (%)")
    pquim_interp_sat_sodio = models.CharField("Interp. Sat. Sodio", max_length=50, blank=True, null=True, help_text="Interpretación saturación de sodio")
    pquim_sat_potasio = models.FloatField("Sat. Potasio", blank=True, null=True, help_text="Saturación de potasio (%)")
    pquim_interp_sat_pot = models.CharField("Interp. Sat. Pot.", max_length=50, blank=True, null=True, help_text="Interpretación saturación de potasio")
    pquim_sat_aluminio = models.FloatField("Sat. Aluminio", blank=True, null=True, help_text="Saturación de aluminio (%)")
    pquim_interp_sat_aluminio = models.CharField("Interp. Sat. Alum.", max_length=50, blank=True, null=True, help_text="Interpretación saturación de aluminio")
    pquim_sat_bases = models.FloatField("Sat. Bases", blank=True, null=True, help_text="Saturación de bases (%)")
    pquim_interp_sat_bases = models.CharField("Interp. Sat. Bases", max_length=50, blank=True, null=True, help_text="Interpretacion saturación de bases")
    pquim_calcio_magenesio = models.FloatField("Cal. - Mag.", blank=True, null=True, help_text="Relación Calcio - Magnesio")
    pquim_interp_calcio_magnesio = models.CharField("Interp. Cal - Mag", max_length=50, blank=True, null=True, help_text="Interpretacion relacion calcio - magnesio")
    pquim_magnesio_potasio = models.FloatField("Mag. - Pot.", blank=True, null=True, help_text="Relación Magnesio - Potasio")
    pquim_interp_mag_potasio = models.CharField("Interp. Mag. - Pot.", max_length=50, blank=True, null=True, help_text="Interpretación relacion magnesio - potasio")
    pquim_calcio_potasio = models.FloatField("Cal. - Pot.", blank=True, null=True, help_text="Relación Calcio - Potasio")
    pquim_interp_calcio_potasio = models.CharField("Interp. Cal. - Pot.", max_length=50, blank=True, null=True, help_text="Interpretación relacion calcio - potasio")
    pquim_calcio_magnesio_potasio = models.FloatField("Cal.- Mag. - Pot.", blank=True, null=True, help_text="Relación Calcio - Magnesio - Potasio")
    pquim_interp_cal_mag_pot = models.CharField("Interp. cal-mag-pot", max_length=50, blank=True, null=True, help_text="Interpretación relación calcio - magnesio - potasio")
    pquim_created = models.DateTimeField("Registro", auto_now_add=True)
    pquim_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return self.mues

    class Meta:
        managed = False
        db_table = 'suelo_propquimica_mayor'
        verbose_name = 'Propiedad quimica mayor'
        verbose_name_plural = 'Propiedades quimicas mayores'


class SueloPropquimicaMenor(models.Model):
    pqmen_id = models.BigAutoField(primary_key=True)
    mues = models.OneToOneField(SueloMuestra, models.DO_NOTHING, unique=True, verbose_name="Muestra")
    pqmen_fosforo_disp = models.FloatField("(P) Fosforo disponible", blank=True, null=True)
    pqmen_interp_fosforo_disp = models.CharField("Interp. Fosforo", max_length=50, blank=True, null=True, editable=False, help_text="Interpretación fosforo")
    pqmen_azufre_disp = models.FloatField("(S) Azufre disponible", blank=True, null=True)
    pqmen_interp_azufre_disp = models.CharField("Interp. Azufre", max_length=50, blank=True, null=True, help_text="Interpretación azufre")
    pqmen_hierro_disp = models.FloatField("(Fe) Hierro disponible", blank=True, null=True)
    pqmen_interp_hierro_disp = models.CharField("Interp. Hierro", max_length=50, blank=True, null=True, help_text="Interpretación hierro")
    pqmen_cobre_disp = models.FloatField("(Cu) Cobre disponible", blank=True, null=True)
    pqmen_interp_cobre_disp = models.CharField("Interp. Cobre", max_length=50, blank=True, null=True, help_text="Interpretación cobre")
    pqmen_magneso_disp = models.FloatField("(Mn) Magneso disponible", blank=True, null=True)
    pqmen_interp_magneso_disp = models.CharField("Interp. Magneso", max_length=50, blank=True, null=True, help_text="Interpretación magneso")
    pqmen_zinc_disp = models.FloatField("(Zn) Zinc disponible", blank=True, null=True)
    pqmen_interp_zinc_disp = models.CharField("Interp. Zinc", max_length=50, blank=True, null=True, help_text="Interpretación zinc")
    pqmen_boro_disp = models.FloatField("(B) Boro disponible", blank=True, null=True)
    pqmen_interp_boro_disp = models.CharField("Interp. Boro", max_length=50, blank=True, null=True, help_text="Interpretación boro")
    pqmen_created = models.DateTimeField("Registro", auto_now_add=True)
    pqmen_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return self.mues

    class Meta:
        managed = False
        db_table = 'suelo_propquimica_menor'
        verbose_name = 'Propiedad quimica menor'
        verbose_name_plural = 'Propiedades quimicas menores'


class SueloMetalesPesados(models.Model):
    smp_id = models.BigAutoField(primary_key=True)
    mues = models.OneToOneField(SueloMuestra, verbose_name="Muestra")
    smp_cromo_total = models.FloatField("(Cr) Cromo total", blank=True, null=True)
    smp_interp_cromo = models.CharField("Interp Cromo", max_length=50, blank=True, null=True, help_text="Interpretación Cromo")
    smp_arsenico_total = models.FloatField("(As) Arsenico total", blank=True, null=True)
    smp_interp_arsenico = models.CharField("Interp Arsenico", max_length=50, blank=True, null=True, help_text="Interpretación Arsenico")
    smp_plomo_total = models.FloatField("(Pb) Plomo total", blank=True, null=True)
    smp_interp_plomo = models.CharField("Interp Plomo", max_length=50, blank=True, null=True, help_text="Interpretación Plomo")
    smp_cadmio_total = models.FloatField("(Cd) Cadmio total", blank=True, null=True)
    smp_interp_cadmio = models.CharField("Interp Cadmio", max_length=50, blank=True, null=True, help_text="Interpretación Cadmio")
    smp_created = models.DateTimeField("Registro", auto_now_add=True)
    smp_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return self.mues

    class Meta:
        managed = False
        db_table = 'suelo_metales_pesados'
        verbose_name = 'Metales pesados'
        verbose_name_plural = 'Metales pesados'


class SueloPropbiologica(models.Model):
    pbio_id = models.BigAutoField(primary_key=True)
    mues = models.ForeignKey(SueloMuestra, models.DO_NOTHING)
    pbio_hfm = models.FloatField("HFM", blank=True, null=True, help_text="Hongos Formadores de Micorrizas: (esporas/g)")
    pbio_interp_hfm = models.CharField("Interpretación HFM", max_length=50, blank=True, null=True)
    pbio_created = models.DateTimeField("Registro", auto_now_add=True)
    pbio_updated = models.DateTimeField("Actualización", auto_now=True)

    def __unicode__(self):
        return self.mues

    class Meta:
        managed = False
        db_table = 'suelo_propbiologica'
        verbose_name = 'Propiedad biologica'
        verbose_name_plural = 'Propiedades biologicas'