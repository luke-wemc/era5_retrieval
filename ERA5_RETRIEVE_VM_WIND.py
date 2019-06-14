
# Script to retrieve C3S ERA5 data
# Author: Luke Sanger
# Date: May 2019

def getData():

    import os.path
    import cdsapi
    # import c3s filename utilites

    c = cdsapi.Client()

    # define paths for nc files on VM
    p_10u = '/data/private/wemc/10WS/10WS_nc/10U'
    p_10v = '/data/private/wemc/10WS/10WS_nc/10V'
    p_100u = '/data/private/wemc/100WS/100WS_nc/100U'
    p_100v = '/data/private/wemc/100WS/100WS_nc/100V'

    # set years & months
    years = ['1979','1980','1981','1982','1983','1984',
              '1985','1986','1987','1988','1989','1990',
              '1991','1992','1993','1994','1995','1996',
              '1997','1998','1999','2000','2001','2002',
              '2003','2004','2005','2006','2007','2008',
              '2009','2010','2011','2012','2013','2014',
              '2015','2016','2017','2018','2019']

    years1 = ['2019']

    months = ['01','02','03','04','05','06','07','08','09','10','11','12']

    variables = [165,166,246,247]

    for VAR in variables:
        try:
            if VAR == 165 :
                codname = 'U--'
                dirname = '10U'
                varname = '10m_u_component_of_wind'
                height = '0010'
                meas = 'INS'
                MPATH = p_10u
            elif VAR == 166 :
                codname = 'V--'
                dirname = '10V'
                varname = '10m_v_component_of_wind'
                height = '0010'
                meas = 'INS'
                MPATH = p_10v
            elif VAR == 246 :
                codname = 'U--'
                dirname = '100U'
                varname = '100m_u_component_of_wind'
                height = '0100'
                meas = 'INS'
                MPATH = p_100u
            elif VAR == 247 :
                codname = 'V--'
                dirname = '100V'
                varname = '100m_v_component_of_wind'
                height = '0100'
                meas = 'INS'
                MPATH = p_100v

            for YYYY in years1:
                for MMMM in months:
                    if MMMM in ['04','06','09','11']:
                        day = '30'
                    else: 
                        day = '31'
                    print("Retrieving variable " + varname + " year " + YYYY + " month " + MMMM)
                    FNAME = 'H_ERA5_ECMW_T639_' + codname + '_' + height + 'm_Euro_025d_S' + YYYY + MMMM + '010000_' + 'E' + YYYY + MMMM + day +'2300_' + meas + '_MAP_01h_NA-_noc_org_NA_NA---_NA---_NA---.nc'
                    PATH_FNAME = MPATH + '/' + FNAME 

                    print("File: " + PATH_FNAME )

                    check = os.path.isfile(PATH_FNAME)

                    #fsize(FNAME)

                    if(check):
                        print("File: " + FNAME + " already retrieved")    
                    else:
                        print("Retrieving variable " + varname + " year " + YYYY + " month " + MMMM)

                    r = c.retrieve(
                        'reanalysis-era5-single-levels',
                        {
                        'variable': varname,
                        'product_type':'reanalysis',
                        'year': YYYY,
                        'month': MMMM,
                        'day':[
                            '01','02','03',
                            '04','05','06',
                            '07','08','09',
                            '10','11','12',
                            '13','14','15',
                            '16','17','18',
                            '19','20','21',
                            '22','23','24',
                            '25','26','27',
                            '28','29','30',
                            '31'
                        ],
                        'time':[
                            '00:00','01:00','02:00',
                            '03:00','04:00','05:00',
                            '06:00','07:00','08:00',
                            '09:00','10:00','11:00',
                            '12:00','13:00','14:00',
                            '15:00','16:00','17:00',
                            '18:00','19:00','20:00',
                            '21:00','22:00','23:00'
                        ],
                        #'grid': [1.0, 1.0],
                        'area': '72.5/-22/26.5/45.5',
                        'format':'netcdf'
                        })
                    r.download(MPATH + '/' + FNAME)
        except:
            pass
        else:
            break                

# run it
getData()

# then run the WS + nuts calulations
import sys
sys.path.append(os.path.abspath("/data/private/resources"))
from RUN_WS_VM.py import RUN_WS_VM
runWS()
