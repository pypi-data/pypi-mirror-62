# -*- coding: utf-8 -*-
"""
**Download**

Before use this module, create ``accounts.yml`` file.
And edit account information in the file.

.. csv-table:: Product Detail
    :header: "id","product","account","protocol","version","parameter","resolution","variable","lat_s","lat_n","lat_r","lon_w","lon_e","lon_r","time_s","time_e"
    :widths: 10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10

    1,ALEXI,IHEWA,FTP,v1,evapotran~,daily,ETA,-60.0,70.0,0.05,-180.0,180.0,0.05,2005-01-01,2016-12-31
    2,ALEXI,IHEWA,FTP,v1,evapotran~,weekly,ETA,-60.0,90.0,0.05,-180.0,180.0,0.05,2003-01-01,2015-12-31
    3,ASCAT,Copernicus,HTTPS,v3.1.1,soil_wate~,daily,SWI_010,-90.0,90.0,0.1,-180.0,180.0,0.1,2007-01-01,None
    4,CFSR,None,HTTPS,v1,radiation,daily,dlwsfc,-89.91710~,89.917106~,0.3122121~,-0.156249~,359.84324~,0.3124995~,1979-01-01,2011-03-31
    5,CFSR,None,HTTPS,v1,radiation,daily,dswsfc,-89.91710~,89.917106~,0.3122121~,-0.156249~,359.84324~,0.3124995~,1979-01-01,2011-03-31
    6,CFSR,None,HTTPS,v1,radiation,daily,ulwsfc,-89.91710~,89.917106~,0.3122121~,-0.156249~,359.84324~,0.3124995~,1979-01-01,2011-03-31
    7,CFSR,None,HTTPS,v1,radiation,daily,uswsfc,-89.91710~,89.917106~,0.3122121~,-0.156249~,359.84324~,0.3124995~,1979-01-01,2011-03-31
    8,CFSR,None,HTTPS,v2,Radiation,daily,dlwsfc,-89.94621~,89.946211~,0.2044232~,-0.102272~,359.89727~,0.2045451~,2011-04-01,None
    9,CFSR,None,HTTPS,v2,Radiation,daily,dswsfc,-89.94621~,89.946211~,0.2044232~,-0.102272~,359.89727~,0.2045451~,2011-04-01,None
    10,CFSR,None,HTTPS,v2,Radiation,daily,ulwsfc,-89.94621~,89.946211~,0.2044232~,-0.102272~,359.89727~,0.2045451~,2011-04-01,None
    11,CFSR,None,HTTPS,v2,Radiation,daily,uswsfc,-89.94621~,89.946211~,0.2044232~,-0.102272~,359.89727~,0.2045451~,2011-04-01,None
    12,CHIRPS,None,FTP,v2.0,precipita~,daily,PCP,-50.0,50.0,0.05,-180.0,180.0,0.05,1981-01-01,None
    13,CHIRPS,None,FTP,v2.0,precipita~,monthly,PCP,-50.0,50.0,0.05,-180.0,180.0,0.05,1981-01-01,None
    14,CMRSET,IHEWA,FTP,v1,evapotran~,monthly,ETA,-90.0,90.0,0.05,-180.0,180.0,0.05,2000-01-01,2012-12-31
    15,DEM,None,HTTPS,v1,DEM,3s,af,-35.0,38.0,0.0008333~,-19.0,55.0,0.0008333~,None,None
    16,DEM,None,HTTPS,v1,DEM,3s,as,-12.0,61.0,0.0008333~,57.0,180.0,0.0008333~,None,None
    17,DEM,None,HTTPS,v1,DEM,3s,au,-56.0,-10.0,0.0008333~,112.0,180.0,0.0008333~,None,None
    18,DEM,None,HTTPS,v1,DEM,3s,ca,5.0,39.0,0.0008333~,-119.0,-60.0,0.0008333~,None,None
    19,DEM,None,HTTPS,v1,DEM,3s,eu,12.0,62.0,0.0008333~,-14.0,70.0,0.0008333~,None,None
    20,DEM,None,HTTPS,v1,DEM,3s,na,24.0,60.0,0.0008333~,-138.0,-52.0,0.0008333~,None,None
    21,DEM,None,HTTPS,v1,DEM,3s,sa,-56.0,15.0,0.0008333~,-93.0,-32.0,0.0008333~,None,None
    22,DEM,None,HTTPS,v1,DEM,15s,af,-35.0,38.0,0.0041666~,-19.0,55.0,0.0041666~,None,None
    23,DEM,None,HTTPS,v1,DEM,15s,as,-12.0,61.0,0.0041666~,57.0,180.0,0.0041666~,None,None
    24,DEM,None,HTTPS,v1,DEM,15s,au,-56.0,-10.0,0.0041666~,112.0,180.0,0.0041666~,None,None
    25,DEM,None,HTTPS,v1,DEM,15s,ca,5.0,39.0,0.0041666~,-119.0,-60.0,0.0041666~,None,None
    26,DEM,None,HTTPS,v1,DEM,15s,eu,12.0,62.0,0.0041666~,-14.0,70.0,0.0041666~,None,None
    27,DEM,None,HTTPS,v1,DEM,15s,na,24.0,60.0,0.0041666~,-138.0,-52.0,0.0041666~,None,None
    28,DEM,None,HTTPS,v1,DEM,15s,sa,-56.0,15.0,0.0041666~,-93.0,-32.0,0.0041666~,None,None
    29,DEM,None,HTTPS,v1,DEM,30s,af,-35.0,38.0,0.0083333~,-19.0,55.0,0.0083333~,None,None
    30,DEM,None,HTTPS,v1,DEM,30s,as,-12.0,61.0,0.0083333~,57.0,180.0,0.0083333~,None,None
    31,DEM,None,HTTPS,v1,DEM,30s,au,-56.0,-10.0,0.0083333~,112.0,180.0,0.0083333~,None,None
    32,DEM,None,HTTPS,v1,DEM,30s,ca,5.0,39.0,0.0083333~,-119.0,-60.0,0.0083333~,None,None
    33,DEM,None,HTTPS,v1,DEM,30s,eu,12.0,62.0,0.0083333~,-14.0,70.0,0.0083333~,None,None
    34,DEM,None,HTTPS,v1,DEM,30s,na,24.0,60.0,0.0083333~,-138.0,-52.0,0.0083333~,None,None
    35,DEM,None,HTTPS,v1,DEM,30s,sa,-56.0,15.0,0.0083333~,-93.0,-32.0,0.0083333~,None,None
    36,DEM,None,HTTPS,v1,DIR,3s,af,-35.0,38.0,0.0008333~,-19.0,55.0,0.0008333~,None,None
    37,DEM,None,HTTPS,v1,DIR,3s,as,-12.0,61.0,0.0008333~,57.0,180.0,0.0008333~,None,None
    38,DEM,None,HTTPS,v1,DIR,3s,au,-56.0,-10.0,0.0008333~,112.0,180.0,0.0008333~,None,None
    39,DEM,None,HTTPS,v1,DIR,3s,ca,5.0,39.0,0.0008333~,-119.0,-60.0,0.0008333~,None,None
    40,DEM,None,HTTPS,v1,DIR,3s,eu,12.0,62.0,0.0008333~,-14.0,70.0,0.0008333~,None,None
    41,DEM,None,HTTPS,v1,DIR,3s,na,24.0,60.0,0.0008333~,-138.0,-52.0,0.0008333~,None,None
    42,DEM,None,HTTPS,v1,DIR,3s,sa,-56.0,15.0,0.0008333~,-93.0,-32.0,0.0008333~,None,None
    43,DEM,None,HTTPS,v1,DIR,15s,af,-35.0,38.0,0.0041666~,-19.0,55.0,0.0041666~,None,None
    44,DEM,None,HTTPS,v1,DIR,15s,as,-12.0,61.0,0.0041666~,57.0,180.0,0.0041666~,None,None
    45,DEM,None,HTTPS,v1,DIR,15s,au,-56.0,-10.0,0.0041666~,112.0,180.0,0.0041666~,None,None
    46,DEM,None,HTTPS,v1,DIR,15s,ca,5.0,39.0,0.0041666~,-119.0,-60.0,0.0041666~,None,None
    47,DEM,None,HTTPS,v1,DIR,15s,eu,12.0,62.0,0.0041666~,-14.0,70.0,0.0041666~,None,None
    48,DEM,None,HTTPS,v1,DIR,15s,na,24.0,60.0,0.0041666~,-138.0,-52.0,0.0041666~,None,None
    49,DEM,None,HTTPS,v1,DIR,15s,sa,-56.0,15.0,0.0041666~,-93.0,-32.0,0.0041666~,None,None
    50,DEM,None,HTTPS,v1,DIR,30s,af,-35.0,38.0,0.0083333~,-19.0,55.0,0.0083333~,None,None
    51,DEM,None,HTTPS,v1,DIR,30s,as,-12.0,61.0,0.0083333~,57.0,180.0,0.0083333~,None,None
    52,DEM,None,HTTPS,v1,DIR,30s,au,-56.0,-10.0,0.0083333~,112.0,180.0,0.0083333~,None,None
    53,DEM,None,HTTPS,v1,DIR,30s,ca,5.0,39.0,0.0083333~,-119.0,-60.0,0.0083333~,None,None
    54,DEM,None,HTTPS,v1,DIR,30s,eu,12.0,62.0,0.0083333~,-14.0,70.0,0.0083333~,None,None
    55,DEM,None,HTTPS,v1,DIR,30s,na,24.0,60.0,0.0083333~,-138.0,-52.0,0.0083333~,None,None
    56,DEM,None,HTTPS,v1,DIR,30s,sa,-56.0,15.0,0.0083333~,-93.0,-32.0,0.0083333~,None,None
    57,ETmonitor,IHEWA,FTP,v1,evapotran~,monthly,ETA,-6671700.0,10007550.0,926.625,-12231450~,16679250.0,926.625,2008-01-01,2013-12-31
    58,ETmonitor,IHEWA,FTP,v1,evapotran~,monthly,ETP,-6671700.0,10007550.0,926.625,-12231450~,16679250.0,926.625,2008-01-01,2013-12-31
    59,ETmonitor,IHEWA,FTP,v1,evapotran~,monthly,EW,-6671700.0,10007550.0,926.625,-12231450~,16679250.0,926.625,2008-01-01,2013-12-31
    60,ETmonitor,IHEWA,FTP,v1,evapotran~,monthly,ES,-6671700.0,10007550.0,926.625,-12231450~,16679250.0,926.625,2008-01-01,2013-12-31
    61,ETmonitor,IHEWA,FTP,v1,evapotran~,monthly,EI,-6671700.0,10007550.0,926.625,-12231450~,16679250.0,926.625,2008-01-01,2013-12-31
    62,ETmonitor,IHEWA,FTP,v1,evapotran~,monthly,T,-6671700.0,10007550.0,926.625,-12231450~,16679250.0,926.625,2008-01-01,2013-12-31
    63,FEWS,None,HTTPS,v4,evapotran~,daily,ETP,-90.5,90.5,1.0,-180.5,179.5,1.0,2001-01-01,None
    64,GLDAS,NASA,HTTPS,v2.1,evapotran~,three_hou~,ETA,-60.0,90.0,0.25,-180.0,180.0,0.25,2000-01-01,None
    65,GLDAS,NASA,HTTPS,v2.1,evapotran~,monthly,ETA,-60.0,90.0,0.25,-180.0,180.0,0.25,2000-01-01,None
    66,GLEAM,GLEAM,SFTP,v3.3a,evapotran~,daily,ETA,-89.875,89.875,0.25,-179.875,179.875,0.25,1980-01-01,2018-12-31
    67,GLEAM,GLEAM,SFTP,v3.3a,evapotran~,monthly,ETA,-89.875,89.875,0.25,-179.875,179.875,0.25,1980-01-01,2018-12-31
    68,GLEAM,GLEAM,SFTP,v3.3b,evapotran~,daily,ETA,-89.875,89.875,0.25,-179.875,179.875,0.25,2003-01-01,2018-12-31
    69,GLEAM,GLEAM,SFTP,v3.3b,evapotran~,monthly,ETA,-89.875,89.875,0.25,-179.875,179.875,0.25,2003-01-01,2018-12-31
    70,GPM,NASA,HTTPS,v6,precipita~,daily,PCP,-90.0,90.0,0.1,-180.0,180.0,0.1,2000-06-01,2019-09-30
    71,GPM,NASA,HTTPS,v6,precipita~,monthly,PCP,-90.0,90.0,0.1,-180.0,180.0,0.1,2000-06-01,2019-09-30
    72,HiHydroSo~,IHEWA,FTP,v1,soil,30s,wcsat_top~,-90.0,90.0,0.0083333~,-180.0,180.0,0.0083333~,None,None
    73,JRC,None,HTTPS,v1,water,1s,occurrence,-60.0,80.0,0.00025,-180.0,180.0,0.00025,None,None
    74,MCD12Q1,NASA,HTTPS,v6,land,yearly,LC,-10007554~,10007554.~,463.31271~,-20015109~,20015109.~,463.31271~,2001-01-01,2018-12-31
    75,MCD12Q1,NASA,HTTPS,v6,land,yearly,LU,-10007554~,10007554.~,463.31271~,-20015109~,20015109.~,463.31271~,2001-01-01,2018-12-31
    76,MCD43A3,NASA,HTTPS,v6,land,daily,AlbedoWSA,-10007554~,10007554.~,463.31271~,-20015109~,20015109.~,463.31271~,2000-02-24,None
    77,MCD43A3,NASA,HTTPS,v6,land,daily,AlbedoBSA,-10007554~,10007554.~,463.31271~,-20015109~,20015109.~,463.31271~,2000-02-24,None
    78,MOD09GQ,NASA,HTTPS,v6,land,daily,REFb01,-10007554~,10007554.~,231.65635~,-20015109~,20015109.~,231.65635~,2000-02-24,None
    79,MOD09GQ,NASA,HTTPS,v6,land,daily,REFb02,-10007554~,10007554.~,231.65635~,-20015109~,20015109.~,231.65635~,2000-02-24,None
    80,MOD10A2,NASA,HTTPS,v6,land,eight_dai~,SnowFrac,-10007554~,10007554.~,463.31271~,-20015109~,20015109.~,463.31271~,2000-02-18,None
    81,MOD10A2,NASA,HTTPS,v6,land,eight_dai~,SnowExt,-10007554~,10007554.~,463.31271~,-20015109~,20015109.~,463.31271~,2000-02-18,None
    82,MOD11A2,NASA,HTTPS,v6,land,eight_dai~,LSTday,-10007554~,10007554.~,926.62543~,-20015109~,20015109.~,926.62543~,2000-02-18,None
    83,MOD11A2,NASA,HTTPS,v6,land,eight_dai~,LSTnight,-10007554~,10007554.~,926.62543~,-20015109~,20015109.~,926.62543~,2000-02-18,None
    84,MOD13Q1,NASA,HTTPS,v6,land,sixteen_d~,NDVI,-10007554~,10007554.~,231.65635~,-20015109~,20015109.~,231.65635~,2000-02-24,None
    85,MOD15A2H,NASA,HTTPS,v6,land,eight_dai~,Fpar,-10007554~,10007554.~,463.31271~,-20015109~,20015109.~,463.31271~,2000-02-18,None
    86,MOD15A2H,NASA,HTTPS,v6,land,eight_dai~,Lai,-10007554~,10007554.~,463.31271~,-20015109~,20015109.~,463.31271~,2000-02-18,None
    87,MOD16A2,NASA,HTTPS,v6,evapotran~,eight_dai~,ET,-10007554~,10007554.~,463.31271~,-20015109~,20015109.~,463.31271~,2001-01-01,None
    88,MOD16A2,NASA,HTTPS,v6,evapotran~,eight_dai~,ETP,-10007554~,10007554.~,463.31271~,-20015109~,20015109.~,463.31271~,2001-01-01,None
    89,MOD17A2H,NASA,HTTPS,v6,land,eight_dai~,GPP,-10007554~,10007554.~,463.31271~,-20015109~,20015109.~,463.31271~,2000-02-18,None
    90,MOD17A3H,NASA,HTTPS,v6,land,eight_dai~,NPP,-10007554~,10007554.~,463.31271~,-20015109~,20015109.~,463.31271~,2000-02-18,None
    91,MSWEP,MSWEP,HTTPS,v2.1,precipita~,daily,PCP,-90.0,90.0,0.1,-180.0,180.0,0.1,1979-01-01,2017-10-31
    92,MYD13,NASA,HTTPS,v6,land,sixteen_d~,NDVI,-10007554~,10007554.~,231.65635~,-20015109~,20015109.~,231.65635~,2000-02-24,None
    93,PROBAV,VITO,HTTPS,v1.01,land,daily,NDVI,-64.99950~,75.000496~,0.0009920~,-180.0004~,179.99950~,0.0009920~,2014-03-12,None
    94,RFE,None,FTP,v2,precipita~,daily,PCP,-40.05,40.05,0.1,-20.05,55.05,0.1,2001-01-01,None
    95,SEBS,IHEWA,FTP,v1,energy,monthly,ETM,-90.0,90.0,0.05,-180.0,180.0,0.05,2000-04-01,2017-06-30
    96,SoilGrids,None,HTTPS,v1,soil,9s,BDRICM,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    97,SoilGrids,None,HTTPS,v1,soil,9s,BDRLOG,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    98,SoilGrids,None,HTTPS,v1,soil,9s,BDTICM,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    99,SoilGrids,None,HTTPS,v1,soil,9s,BLDFIE1,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    100,SoilGrids,None,HTTPS,v1,soil,9s,BLDFIE2,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    101,SoilGrids,None,HTTPS,v1,soil,9s,BLDFIE3,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    102,SoilGrids,None,HTTPS,v1,soil,9s,BLDFIE4,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    103,SoilGrids,None,HTTPS,v1,soil,9s,BLDFIE5,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    104,SoilGrids,None,HTTPS,v1,soil,9s,BLDFIE6,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    105,SoilGrids,None,HTTPS,v1,soil,9s,BLDFIE7,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    106,SoilGrids,None,HTTPS,v1,soil,9s,CLYPPT1,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    107,SoilGrids,None,HTTPS,v1,soil,9s,CLYPPT2,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    108,SoilGrids,None,HTTPS,v1,soil,9s,CLYPPT3,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    109,SoilGrids,None,HTTPS,v1,soil,9s,CLYPPT4,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    110,SoilGrids,None,HTTPS,v1,soil,9s,CLYPPT5,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    111,SoilGrids,None,HTTPS,v1,soil,9s,CLYPPT6,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    112,SoilGrids,None,HTTPS,v1,soil,9s,CLYPPT7,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    113,SoilGrids,None,HTTPS,v1,soil,9s,CRFVOL1,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    114,SoilGrids,None,HTTPS,v1,soil,9s,CRFVOL2,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    115,SoilGrids,None,HTTPS,v1,soil,9s,CRFVOL3,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    116,SoilGrids,None,HTTPS,v1,soil,9s,CRFVOL4,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    117,SoilGrids,None,HTTPS,v1,soil,9s,CRFVOL5,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    118,SoilGrids,None,HTTPS,v1,soil,9s,CRFVOL6,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    119,SoilGrids,None,HTTPS,v1,soil,9s,CRFVOL7,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    120,SoilGrids,None,HTTPS,v1,soil,9s,OCSTHA1,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    121,SoilGrids,None,HTTPS,v1,soil,9s,OCSTHA2,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    122,SoilGrids,None,HTTPS,v1,soil,9s,OCSTHA3,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    123,SoilGrids,None,HTTPS,v1,soil,9s,OCSTHA4,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    124,SoilGrids,None,HTTPS,v1,soil,9s,OCSTHA5,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    125,SoilGrids,None,HTTPS,v1,soil,9s,OCSTHA6,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    126,SoilGrids,None,HTTPS,v1,soil,9s,ORCDRC1,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    127,SoilGrids,None,HTTPS,v1,soil,9s,ORCDRC2,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    128,SoilGrids,None,HTTPS,v1,soil,9s,ORCDRC3,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    129,SoilGrids,None,HTTPS,v1,soil,9s,ORCDRC4,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    130,SoilGrids,None,HTTPS,v1,soil,9s,ORCDRC5,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    131,SoilGrids,None,HTTPS,v1,soil,9s,ORCDRC6,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    132,SoilGrids,None,HTTPS,v1,soil,9s,ORCDRC7,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    133,SoilGrids,None,HTTPS,v1,soil,9s,SLTPPT1,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    134,SoilGrids,None,HTTPS,v1,soil,9s,SLTPPT2,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    135,SoilGrids,None,HTTPS,v1,soil,9s,SLTPPT3,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    136,SoilGrids,None,HTTPS,v1,soil,9s,SLTPPT4,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    137,SoilGrids,None,HTTPS,v1,soil,9s,SLTPPT5,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    138,SoilGrids,None,HTTPS,v1,soil,9s,SLTPPT6,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    139,SoilGrids,None,HTTPS,v1,soil,9s,SLTPPT7,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    140,SoilGrids,None,HTTPS,v1,soil,9s,SNDPPT1,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    141,SoilGrids,None,HTTPS,v1,soil,9s,SNDPPT2,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    142,SoilGrids,None,HTTPS,v1,soil,9s,SNDPPT3,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    143,SoilGrids,None,HTTPS,v1,soil,9s,SNDPPT4,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    144,SoilGrids,None,HTTPS,v1,soil,9s,SNDPPT5,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    145,SoilGrids,None,HTTPS,v1,soil,9s,SNDPPT6,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    146,SoilGrids,None,HTTPS,v1,soil,9s,SNDPPT7,-56.0,84.0,0.0020833~,-180.0,180.0,0.0020833~,None,None
    147,TRMM,NASA,HTTPS,v7,precipita~,monthly,PCP,-50.0,50.0,0.25,-180.0,180.0,0.25,1980-01-01,2019-09-30
    148,TRMM,NASA,HTTPS,v7a,precipita~,monthly,PCP,-50.0,50.0,0.25,-180.0,180.0,0.25,2000-01-01,2010-09-30
    149,TWC,IHEWA,FTP,v1,water,5m,WPL,-55.99499~,83.671666~,0.0833333~,-180.0,180.0,0.0833333~,None,None
"""
# import shutil
import datetime
import importlib
import inspect
import os
import sys

try:
    from .base.exception import IHEClassInitError,\
        IHEStringError, IHETypeError, IHEKeyError, IHEFileError
except ImportError:
    from IHEWAcollect.base.exception import IHEClassInitError,\
        IHEStringError, IHETypeError, IHEKeyError, IHEFileError

try:
    from .base.user import User
except ImportError:
    from IHEWAcollect.base.user import User


class Download(User):
    """Download class

    After initialise the class, data downloading will automatically start.

    Args:
        workspace (str): Directory to accounts.yml.
        product (str): Product name.
        version (str): Version name.
        parameter (str): Parameter name.
        resolution (str): Resolution name.
        variable (str): Variable name.
        bbox (dict): Spatial range, {'w':, 's':, 'e':, 'n':}.
        period (dict): Time range, {'s':, 'e':}.
        nodata (int): -9999.
        is_status (bool): Is to print status message.
        kwargs (dict): Other arguments.
    """
    status = 'Global status.'

    __status = {
        'messages': {
            0: 'S: WA.Download {f:>20} : status {c}, {m}',
            1: 'E: WA.Download {f:>20} : status {c}: {m}',
            2: 'W: WA.Download {f:>20} : status {c}: {m}',
        },
        'code': 0,
        'message': '',
        'is_print': True
    }

    __conf = {
        'path': '',
        'time': {
            'start': None,
            'now': None,
            'end': None
        },
        'account': {
            'name': '',
            'data': {}
        },
        'product': {
            'name': '',
            'version': '',
            'parameter': '',
            'resolution': '',
            'variable': '',
            'bbox': {},
            'period': {},
            'nodata': -9999,
            'template': '',
            'url': '',
            'protocol': '',
            'method': '',
            'freq': '',
            'data': {}
        },
        'folder': {
            'r': '',
            't': '',
            'l': ''
        },
        'log': {
            'name': 'log.{var}.{res}.{prod}.txt',
            'file': '{path}/log-.txt',
            'fp': None,
            'status': -1,  # -1: not found, 0: closed, 1: opened
        }
    }
    __tmp = {
        'name': '',
        'module': None,
        'data': {}
    }

    def __init__(self, workspace='',
                 product='', version='', parameter='', resolution='', variable='',
                 bbox={}, period={}, nodata=-9999,
                 is_status=True, **kwargs):
        """Class instantiation
        """
        tmp_product_conf = {
            'version': version,
            'parameter': parameter,
            'resolution': resolution,
            'variable': variable
        }

        # Class self.__status['is_print']
        vname, rtype, vdata = 'is_status', bool, is_status
        if self.check_input(vname, rtype, vdata):
            self.__status['is_print'] = vdata
        else:
            self.__status['code'] = 1

        # Class self.__conf['path']
        vname, rtype, vdata = 'workspace', str, workspace
        if self.check_input(vname, rtype, vdata):
            path = os.path.join(vdata, 'IHEWAcollect')
            if not os.path.exists(path):
                os.makedirs(path)
            self.__conf['path'] = path
        else:
            self.__status['code'] = 1

        rtype = str
        for vname, vdata in tmp_product_conf.items():
            if self.check_input(vname, rtype, vdata):
                self.__conf['product'][vname] = vdata
            else:
                self.__status['code'] = 1

        self.__conf['product']['bbox'] = bbox
        self.__conf['product']['period'] = period
        self.__conf['product']['nodata'] = nodata

        # super(Download, self).__init__(**kwargs)
        if self.__status['code'] == 0:
            User.__init__(self, workspace, product, is_status, **kwargs)
        else:
            raise IHEClassInitError('Download') from None

        # Class Download
        if self.__status['code'] == 0:
            self._download_init()

            self._download_prepare()
            self._download_start()
            self._download_finish()

            self.__status['message'] = ''
        else:
            raise IHEClassInitError('Download') from None

    def _set_status(self, fun='', prt=False, ext=''):
        """Set status

        Args:
            fun (str): Function name.
            prt (bool): Is to print on screen?
            ext (str): Extra message.
        """
        self.status = self._status(self.__status['messages'],
                                   self.__status['code'],
                                   fun, prt, ext)

    def _download_init(self) -> int:
        """

        Returns:
            int: Status.
        """
        status = -1
        self._time()
        self._account()
        self._product()
        return status

    def _download_prepare(self) -> int:
        """

        Returns:
            int: Status.
        """
        status = -1
        self._folder()
        self._log()
        self._template()
        # _folder_clean
        return status

    def _download_start(self) -> int:
        """

        Returns:
            int: Status.
        """
        status = -1
        self.__tmp['module'].DownloadData(self.__status, self.__conf)
        # self.__tmp['module'].download()
        # self.__tmp['module'].convert()
        # self.__tmp['module'].saveas()
        return status

    def _download_finish(self) -> int:
        """

        Returns:
            int: Status.
        """
        status = -1
        self._log_close()
        # _folder_clean
        return status

    def _time(self) -> dict:
        """

        Returns:
            int: Status.
        """
        # Class self.__conf['time']
        time = self.__conf['time']

        if self.__status['code'] == 0:
            now = datetime.datetime.now()

            self.__conf['time']['start'] = now
            self.__conf['time']['now'] = now
            self.__conf['time']['end'] = now
        return time

    def _account(self) -> dict:
        """

        Returns:
            dict: account.
        """
        # Class self.__conf['account'] <- User.account
        account = self.__conf['account']

        if self.__status['code'] == 0:
            account['name'] = self._User__conf['account']['name']
            account['data'] = self._User__conf['account']['data']

            self.__conf['account']['name'] = account['name']
            self.__conf['account']['data'] = account['data']
        return account

    def _product(self) -> dict:
        """

        Returns:
            dict: product.
        """
        # Class self.__conf['product'] <- Base.product
        product = self.__conf['product']
        version = product['version']
        parameter = product['parameter']
        resolution = product['resolution']
        variable = product['variable']

        if self.__status['code'] == 0:
            product['name'] = \
                self._Base__conf['product']['name']
            product['data'] = \
                self._Base__conf['product']['data']
            product['template'] = \
                self._Base__conf['product']['data'][
                    'template']
            product['url'] = \
                self._Base__conf['product']['data'][
                    version][parameter][resolution]['url']
            product['protocol'] = \
                self._Base__conf['product']['data'][
                    version][parameter][resolution]['protocol']
            product['method'] = \
                self._Base__conf['product']['data'][
                    version][parameter][resolution]['method']
            product['freq'] = \
                self._Base__conf['product']['data'][
                    version][parameter][resolution]['freq']

            keys = product['data'].keys()
            if version not in keys:
                self.__status['code'] = 1
                raise IHEKeyError(version, keys) from None

            keys = product['data'][
                version].keys()
            if parameter not in keys:
                self.__status['code'] = 1
                raise IHEKeyError(parameter, keys) from None

            keys = product['data'][
                version][parameter].keys()
            if resolution not in keys:
                self.__status['code'] = 1
                raise IHEKeyError(resolution, keys) from None

            keys = product['data'][
                version][parameter][resolution]['variables'].keys()
            if variable not in keys:
                self.__status['code'] = 1
                raise IHEKeyError(variable, keys) from None

            self.__conf['product']['name'] = product['name']
            self.__conf['product']['data'] = product['data'][
                version][parameter][resolution]['variables'][variable]
        return product

    def _folder(self) -> dict:
        folder = self.__conf['folder']

        # Define folder
        if self.__status['code'] == 0:
            workspace = self.__conf['path']

            variable = self.__conf['product']['variable']

            #  _parameter_ / _resolution_ / _variable_ / _product_ \_ _version_
            path = os.path.join(workspace, variable)
            folder = {
                'r': os.path.join(path, 'remote'),
                't': os.path.join(path, 'temporary'),
                'l': os.path.join(path, 'download')
            }

            for key, value in folder.items():
                if not os.path.exists(value):
                    os.makedirs(value)

            self.__conf['folder'] = folder
        return folder

    def _folder_clean(self, name):
        statue = 1

        # shutil

        # re = glob.glob(os.path.join(folder['r'], '*'))
        # for f in re:
        #     os.remove(os.path.join(folder['r'], f))
        return statue

    def _log(self) -> dict:
        """

        Returns:
            dict: log.
        """
        # Class self.__conf['log']
        status = -1
        log = self.__conf['log']
        product = self.__conf['product']['name']
        resolution = self.__conf['product']['resolution']
        variable = self.__conf['product']['variable']

        if self.__status['code'] == 0:
            path = self.__conf['path']
            time = self.__conf['time']['start']
            time_str = time.strftime('%Y-%m-%d %H:%M:%S.%f')

            fname = log['name'].format(prod=product, var=variable, res=resolution)
            file = os.path.join(path, fname)

            # -1: not found, 0: closed, 1: opened
            fp = self._log_create(file)

            self.__conf['log']['fname'] = fname
            self.__conf['log']['file'] = file
            self.__conf['log']['fp'] = fp
            self.__conf['log']['status'] = status
        return log

    def _log_create(self, file):
        time = datetime.datetime.now()
        time_str = time.strftime('%Y-%m-%d %H:%M:%S.%f')
        self.__conf['time']['now'] = time

        print('Create log file "{f}"'.format(f=file))
        txt = '{t}: IHEWAcollect'.format(t=time_str)

        fp = open(file, 'w+')
        fp.write('{}\n'.format(txt))
        for key, value in self.__conf['product'].items():
            if key != 'data':
                fp.write('{:>26s}: {}\n'.format(key, str(value)))

        return fp

    def _log_close(self):
        time = datetime.datetime.now()
        time_str = time.strftime('%Y-%m-%d %H:%M:%S.%f')
        self.__conf['time']['now'] = time

        file = self.__conf['log']['file']
        fp = self.__conf['log']['fp']

        print('Close log file "{f}"'.format(f=file))
        txt = '{t}: IHEWAcollect finished.'.format(t=time_str)
        fp.write('{}\n'.format(txt))
        fp.close()
        self.__conf['log']['fp'] = None

    def _template(self) -> dict:
        """

        Returns:
            dict: template.
        """
        # Class self.__tmp <- Base.product
        template = self.__tmp

        if self.__status['code'] == 0:
            product = self.__conf['product']
            module_name_base = '{tmp}.{prod}'.format(
                tmp=self._Base__conf['product']['data']['template'],
                prod=product['name'])

            # Load module
            # module_obj = None
            module_name = template['name']
            module_obj = template['module']
            if module_obj is None:
                is_reload_module = False
            else:
                if module_name == module_name_base:
                    is_reload_module = True
                else:
                    is_reload_module = False
            template['name'] = module_name_base

            if is_reload_module:
                try:
                    module_obj = importlib.reload(module_obj)
                except ImportError:
                    raise IHEClassInitError('Templates') from None
                else:
                    template['module'] = module_obj
                    print('Reloaded module'
                          '.{p}.{m}'.format(p=product['template'],
                                            m=product['name']))
            else:
                try:
                    # def template_load(self) -> dict:
                    module_obj = \
                        importlib.import_module('IHEWAcollect.templates'
                                                '.{p}.{m}'.format(p=product['template'],
                                                                  m=product['name']))
                    print('Loaded module from IHEWAcollect.templates'
                          '.{p}.{m}'.format(p=product['template'],
                                            m=product['name']))
                except ImportError:
                    module_obj = \
                        importlib.import_module('IHEWAcollect.templates'
                                                '.{p}.{m}'.format(p=product['template'],
                                                                  m=product['name']))
                    print('Loaded module from IHEWAcollect.templates'
                          '.{p}.{m}'.format(p=product['template'],
                                            m=product['name']))
                finally:
                    # def template_init(self) -> dict:
                    if module_obj is not None:
                        template['module'] = module_obj
                    else:
                        raise IHEClassInitError('Templates') from None

            self.__tmp['name'] = template['name']
            self.__tmp['module'] = template['module']
        return template

    def get_products(self) -> dict:
        """Get details of all products

        Returns:
            dict: Products data.
        """
        products = self._Base__conf['data']['products']

        # import pandas as pd
        # df_products = pd.DataFrame.from_dict(products)
        # print(df_products)

        str_col = ['id',
                   'product',
                   'account',
                   'protocol',
                   'version',
                   'parameter',
                   'resolution',
                   'variable',
                   'lat_s', 'lat_n', 'lat_r',
                   'lon_w', 'lon_e', 'lon_r',
                   'time_s', 'time_e']

        str_size = 10
        print('')

        # str_fmt = ''
        # str_fmt_cel = '{col[%d]:>' + str(str_size) + '}%s'
        # for icol in range(len(str_col)):
        #     str_fmt += str_fmt_cel % (icol, ', ')
        # str_fmt += ''
        # print(str_fmt.format(col=str_col))

        # ================= #
        # ReStructured Text #
        # ================= #
        # str_tmp = ''
        # for icol in range(len(str_col)):
        #     str_tmp += '+{sep:->' + str(str_size + 2) + 's}'
        # str_tmp += '+'
        # print(str_tmp.format(sep=''))

        # str_tmp = ''
        # str_tmp_cel = '| {col[%d]:>' + str(str_size) + '}%s'
        # for icol in range(len(str_col)):
        #     str_tmp += str_tmp_cel % (icol, ' ')
        # str_tmp += '|'
        # print(str_tmp.format(col=str_col))

        # str_tmp = ''
        # for icol in range(len(str_col)):
        #     str_tmp += '+{sep:=>' + str(str_size + 2) + 's}'
        # str_tmp += '+'
        # print(str_tmp.format(sep=''))

        # ============================= #
        # .. csv-table:: Product Detail #
        # ============================= #
        str_tmp = '.. csv-table:: Product Detail'
        print(str_tmp)

        str_tmp = '    :header: '
        str_tmp_cel = '"{col[%d]}"%s'
        for icol in range(len(str_col) - 1):
            str_tmp += str_tmp_cel % (icol, ',')
        str_tmp += str_tmp_cel % (len(str_col) - 1, '')
        print(str_tmp.format(col=str_col))

        str_tmp = '    :widths: '
        str_tmp_cel = '%d%s'
        for icol in range(len(str_col) - 1):
            str_tmp += str_tmp_cel % (str_size, ',')
        str_tmp += str_tmp_cel % (str_size, '\n')
        print(str_tmp)


        i = 0
        for pd_n, pd_d in products.items():
            pd_a = pd_d['account']

            for pd_ver_n, pd_ver_d in pd_d.items():
                if pd_ver_n not in ['account', 'template', 'meta']:

                    for pd_par_n, pd_par_d in pd_ver_d.items():

                        for pd_res_n, pd_res_d in pd_par_d.items():
                            pd_res_d_pro = pd_res_d['protocol']

                            for pd_var_n, pd_var_d in pd_res_d['variables'].items():
                                i += 1

                                # pd_var_d_nam = pd_var_d['name']
                                pd_var_d_lat_s = pd_var_d['lat']['s']
                                pd_var_d_lat_n = pd_var_d['lat']['n']
                                pd_var_d_lat_r = pd_var_d['lat']['r']
                                pd_var_d_lon_w = pd_var_d['lon']['w']
                                pd_var_d_lon_e = pd_var_d['lon']['e']
                                pd_var_d_lon_r = pd_var_d['lon']['r']
                                pd_var_d_tim_s = pd_var_d['time']['s']
                                pd_var_d_tim_e = pd_var_d['time']['e']

                                str_col = [i,
                                           pd_n,
                                           pd_a,
                                           pd_res_d_pro,
                                           pd_ver_n,
                                           pd_par_n,
                                           pd_res_n,
                                           pd_var_n,
                                           pd_var_d_lat_s,
                                           pd_var_d_lat_n,
                                           pd_var_d_lat_r,
                                           pd_var_d_lon_w,
                                           pd_var_d_lon_e,
                                           pd_var_d_lon_r,
                                           pd_var_d_tim_s,
                                           pd_var_d_tim_e]

                                for j in range(len(str_col)):
                                    if isinstance(str_col[j], datetime.datetime):
                                        str_col[j] = str_col[j].strftime('%Y-%m-%d')

                                    if str_col[j] is None:
                                        str_col[j] = 'None'

                                    str_col[j] = str(str_col[j])

                                    if len(str_col[j]) > str_size:
                                        str_col[j] = str_col[j][0:str_size - 1] + '~'

                                # print(str_fmt.format(col=str_col))

                                # ================= #
                                # ReStructured Text
                                # ================= #
                                # str_tmp = ''
                                # for icol in range(len(str_col)):
                                #     str_tmp += '+{sep:->' + str(str_size + 2) + 's}'
                                # str_tmp += '+'
                                # print(str_tmp.format(sep=''))

                                # ============================= #
                                # .. csv-table:: Product Detail #
                                # ============================= #
                                str_tmp = '    '
                                str_tmp_cel = '{col[%d]}%s'
                                for icol in range(len(str_col) - 1):
                                    str_tmp += str_tmp_cel % (icol, ',')
                                str_tmp += str_tmp_cel % (len(str_col) - 1, '')
                                print(str_tmp.format(col=str_col))

        return products


if __name__ == "__main__":
    print('\nDownload\n=====')
    path = os.path.join(
        os.getcwd(),
        os.path.dirname(
            inspect.getfile(
                inspect.currentframe())),
        '../', '../', 'tests'
    )

    test_args = {
        '1a': {
            'product': 'ALEXI',
            'version': 'v1',
            'parameter': 'evapotranspiration',
            'resolution': 'daily',
            'variable': 'ETA',
            'bbox': {
                'w': -19.0,
                'n': 38.0,
                'e': 55.0,
                's': -35.0
            },
            'period': {
                's': '2005-01-01',
                'e': '2005-01-02'
            },
            'nodata': -9999
        }
    }

    # Download __init__
    for key, value in test_args.items():
        print('\n{:>4s}'
              '{:>20s}{:>6s}{:>20s}{:>20s}{:>20s}\n'
              '{:->90s}'.format(key,
                                value['product'],
                                value['version'],
                                value['parameter'],
                                value['resolution'],
                                value['variable'],
                                '-'))

        download = Download(workspace=path,
                            product=value['product'],
                            version=value['version'],
                            parameter=value['parameter'],
                            resolution=value['resolution'],
                            variable=value['variable'],
                            bbox=value['bbox'],
                            period=value['period'],
                            nodata=value['nodata'],
                            is_status=False)

        download.get_products()
