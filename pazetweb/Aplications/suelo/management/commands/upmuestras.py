# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from Aplications.suelo.models import *
import csv, codecs
import sys


reload(sys)
sys.setdefaultencoding('utf8')

class Command(BaseCommand):
    args = 'Arguments is not needed'
    help = 'Comando para cargar csv de muestras tomadas en azosulia'

    def handle(self, *args, **options):

        ruta = '/home/storres/Documentos/CORPOICA/Muestras_Asozulia.csv'

        reader = csv.DictReader(codecs.open(ruta, 'rU', encoding='ISO-8859-1'), delimiter=";")

        for line in reader:

            id = line.pop('ID').replace(" ", "")
            lng = line.pop('Longitud_W').replace(',', '.')
            lat = line.pop('Latitud_N').replace(',', '.')

            coordenada = 'SRID=4326;POINT(' + lng + ' ' + lat + ')'

            muestra = SueloMuestra.objects.create(mues_id=id, mues_coordenadas=coordenada, mues_prof_inicio=0, mues_prof_final=20);

            arena = line.pop('A').replace(',', '.') or None
            limo = line.pop('L').replace(',', '.') or None
            arcilla = line.pop('Ar').replace(',', '.') or None
            gravi = line.pop('W_sat_g').replace(',', '.') or None
            vol = line.pop('W_sat_v').replace(',', '.') or None
            da = line.pop('Da').replace(',', '.') or None
            dr = line.pop('Dr').replace(',', '.') or None

            d4mm = line.pop('D_4mm').replace(',', '.') or None
            d2mm = line.pop('D_2mm').replace(',', '.') or None
            d1mm = line.pop('D_1mm').replace(',', '.') or None
            d05mm = line.pop('D_0,5mm').replace(',', '.') or None
            d025mm = line.pop('D_0,25mm').replace(',', '.') or None
            dmin025mm = line.pop('D_menor_0,25').replace(',', '.') or None

            dmp = line.pop('DMP').replace(',', '.') or None
            bar01 = line.pop('W_0,1bar_CC').replace(',', '.') or None
            bar1 = line.pop('W_1bar').replace(',', '.') or None
            pmp = line.pop('W_15bar_PMP').replace(',', '.') or None
            ib = line.pop('ib').replace(',', '.') or None
            #rmp = line.pop('rmp').replace(',', '.') or None
            #print '{}'.format(arcilla)


            SueloPropfisica.objects.create(
                mues=muestra,
                pfis_arena=arena,
                pfis_limo=limo,
                pfis_arcilla=arcilla,
                pfis_w_sat_g=gravi,
                pfis_w_sat_v=vol,
                pfis_densidad_aparante=da,
                pfis_densidad_real=dr,
                pfis_d_4mm=d4mm,
                pfis_d_2mm=d2mm,
                pfis_d_1mm=d1mm,
                pfis_d_05mm=d05mm,
                pfis_d_may_025mm=d025mm,
                pfis_d_men_025mm=dmin025mm,
                pfis_dmp=dmp,
                pfis_w_01bar_cc=bar01,
                pfis_w_1bar=bar1,
                pfis_w_15bar_pmp=pmp,
                pfis_infil_basica=ib
            );

            ph = line.pop('ph').replace(',', '.') or None
            co = line.pop('CO').replace(',', '.') or None
            acidez = line.pop('AlH').replace(',', '.') or None
            al = line.pop('Al').replace(',', '.') or None
            cal = line.pop('Ca').replace(',', '.') or None
            mg = line.pop('Mg').replace(',', '.') or None
            pot = line.pop('K1').replace(',', '.') or None
            sod = line.pop('Na1').replace(',', '.') or None
            cice = line.pop('CICE').replace(',', '.') or None
            ce = line.pop('CE').replace(',', '.') or None

            SueloPropquimicaMayor.objects.create(
                mues=muestra,
                pquim_ph=ph,
                pquim_co=co,
                pquim_acidez=acidez,
                pquim_aluminio_inter=al,
                pquim_calcio_inter=cal,
                pquim_magnesio_inter=mg,
                pquim_potasio_inter=pot,
                pquim_sodio_inter=sod,
                pquim_cice=cice,
                pquim_conduc_electrica=ce
            );

            fosforo = line.pop('P').replace(',', '.') or None
            azufre = line.pop('S').replace(',', '.') or None
            hierro = line.pop('Fe').replace(',', '.') or None
            cobre = line.pop('Cu').replace(',', '.') or None
            magneso = line.pop('Mn').replace(',', '.') or None
            zinc = line.pop('Zn').replace(',', '.') or None
            boro = line.pop('B').replace(',', '.') or None

            SueloPropquimicaMenor.objects.create(
                mues=muestra,
                pqmen_fosforo_disp=fosforo,
                pqmen_azufre_disp=azufre,
                pqmen_hierro_disp=hierro,
                pqmen_cobre_disp=cobre,
                pqmen_magneso_disp=magneso,
                pqmen_zinc_disp=zinc,
                pqmen_boro_disp=boro
            );

            cromo = line.pop('Cr') or None
            arsenico = line.pop('As').replace(',', '.') or None
            plomo = line.pop('Pb').replace(',', '.') or None
            cadmio = line.pop('Cd').replace(',', '.') or None

            cadinterp, crinterp, arinterp, plinterp = None, None, None, None

            if cromo is not None and ('<' in cromo) :
                cromo = 0
                crinterp = 'No detectable'
            elif cromo is not None and not ('<' in cromo) :
                cromo = cromo.replace(',', '.')


            if arsenico is not None and ('<' in arsenico) :
                arsenico = 0
                arinterp = 'No detectable'
            elif arsenico is not None and not ('<' in arsenico) :
                arsenico = arsenico.replace(',', '.')


            if plomo is not None and ('<' in plomo) :
                plomo = 0
                plinterp = 'No detectable'
            elif plomo is not None and not ('<' in plomo) :
                plomo = plomo.replace(',', '.')

            if cadmio is not None and ('<' in cadmio) :
                cadmio = 0
                cadinterp = 'No detectable'
            elif cadmio is not None and not ('<' in cadmio) :
                cadmio = cadmio.replace(',', '.')



            SueloMetalesPesados.objects.create(
                mues=muestra,
                smp_cromo_total=cromo,
                smp_interp_cromo=crinterp,
                smp_arsenico_total=arsenico,
                smp_interp_arsenico=arinterp,
                smp_plomo_total=plomo,
                smp_interp_plomo=plinterp,
                smp_cadmio_total=cadmio,
                smp_interp_cadmio=cadinterp
            );

            hfm = line.pop('HFM').replace(',', '.') or None

            SueloPropbiologica.objects.create(
                mues=muestra,
                pbio_hfm=hfm
            )

            self.stdout.write(self.style.SUCCESS('Muestra: %s' % id))
