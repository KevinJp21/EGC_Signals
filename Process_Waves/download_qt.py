import os
import requests
from tqdm import tqdm

# URL base de PhysioNet
BASE_URL = "https://physionet.org/files/qtdb/1.0.0/"

# Lista de archivos a descargar
archivos = [
    "sel100.atr", "sel100.dat", "sel100.hea", "sel100.man", "sel100.pu", "sel100.pu0", "sel100.pu1", "sel100.q1c", "sel100.q2c", "sel100.qt1", "sel100.qt2", "sel100.xws",
    "sel102.atr", "sel102.dat", "sel102.hea", "sel102.man", "sel102.pu", "sel102.pu0", "sel102.pu1", "sel102.q1c", "sel102.q2c", "sel102.qt1", "sel102.qt2", "sel102.xws",
    "sel103.atr", "sel103.dat", "sel103.hea", "sel103.man", "sel103.pu", "sel103.pu0", "sel103.pu1", "sel103.q1c", "sel103.q2c", "sel103.qt1", "sel103.qt2", "sel103.xws",
    "sel104.atr", "sel104.dat", "sel104.hea", "sel104.man", "sel104.pu", "sel104.pu0", "sel104.pu1", "sel104.q1c", "sel104.qt1", "sel104.xws",
    "sel114.atr", "sel114.dat", "sel114.hea", "sel114.man", "sel114.pu", "sel114.pu0", "sel114.pu1", "sel114.q1c", "sel114.q2c", "sel114.qt1", "sel114.qt2", "sel114.xws",
    "sel116.atr", "sel116.dat", "sel116.hea", "sel116.man", "sel116.pu", "sel116.pu0", "sel116.pu1", "sel116.q1c", "sel116.q2c", "sel116.qt1", "sel116.qt2", "sel116.xws",
    "sel117.atr", "sel117.dat", "sel117.hea", "sel117.man", "sel117.pu", "sel117.pu0", "sel117.pu1", "sel117.q1c", "sel117.q2c", "sel117.qt1", "sel117.qt2", "sel117.xws",
    "sel123.atr", "sel123.dat", "sel123.hea", "sel123.man", "sel123.pu", "sel123.pu0", "sel123.pu1", "sel123.q1c", "sel123.q2c", "sel123.qt1", "sel123.qt2", "sel123.xws",
    "sel14046.atr", "sel14046.dat", "sel14046.hea", "sel14046.hea-", "sel14046.man", "sel14046.pu", "sel14046.pu0", "sel14046.pu1", "sel14046.q1c", "sel14046.qt1", "sel14046.xws",
    "sel14157.atr", "sel14157.dat", "sel14157.hea", "sel14157.hea-", "sel14157.man", "sel14157.pu", "sel14157.pu0", "sel14157.pu1", "sel14157.q1c", "sel14157.qt1", "sel14157.xws",
    "sel14172.atr", "sel14172.dat", "sel14172.hea", "sel14172.hea-", "sel14172.man", "sel14172.pu", "sel14172.pu0", "sel14172.pu1", "sel14172.q1c", "sel14172.qt1", "sel14172.xws",
    "sel15814.atr", "sel15814.dat", "sel15814.hea", "sel15814.hea-", "sel15814.man", "sel15814.pu", "sel15814.pu0", "sel15814.pu1", "sel15814.q1c", "sel15814.qt1", "sel15814.xws",
    "sel16265.atr", "sel16265.dat", "sel16265.hea", "sel16265.hea-", "sel16265.man", "sel16265.pu", "sel16265.pu0", "sel16265.pu1", "sel16265.q1c", "sel16265.qt1", "sel16265.xws",
    "sel16272.atr", "sel16272.dat", "sel16272.hea", "sel16272.hea-", "sel16272.man", "sel16272.pu", "sel16272.pu0", "sel16272.pu1", "sel16272.q1c", "sel16272.qt1", "sel16272.xws",
    "sel16273.atr", "sel16273.dat", "sel16273.hea", "sel16273.hea-", "sel16273.man", "sel16273.pu", "sel16273.pu0", "sel16273.pu1", "sel16273.q1c", "sel16273.qt1", "sel16273.xws",
    "sel16420.atr", "sel16420.dat", "sel16420.hea", "sel16420.hea-", "sel16420.man", "sel16420.pu", "sel16420.pu0", "sel16420.pu1", "sel16420.q1c", "sel16420.qt1", "sel16420.xws",
    "sel16483.atr", "sel16483.dat", "sel16483.hea", "sel16483.hea-", "sel16483.man", "sel16483.pu", "sel16483.pu0", "sel16483.pu1", "sel16483.q1c", "sel16483.qt1", "sel16483.xws",
    "sel16539.atr", "sel16539.dat", "sel16539.hea", "sel16539.hea-", "sel16539.man", "sel16539.pu", "sel16539.pu0", "sel16539.pu1", "sel16539.q1c", "sel16539.qt1", "sel16539.xws",
    "sel16773.atr", "sel16773.dat", "sel16773.hea", "sel16773.hea-", "sel16773.man", "sel16773.pu", "sel16773.pu0", "sel16773.pu1", "sel16773.q1c", "sel16773.qt1", "sel16773.xws",
    "sel16786.atr", "sel16786.dat", "sel16786.hea", "sel16786.hea-", "sel16786.man", "sel16786.pu", "sel16786.pu0", "sel16786.pu1", "sel16786.q1c", "sel16786.qt1", "sel16786.xws",
    "sel16795.atr", "sel16795.dat", "sel16795.hea", "sel16795.hea-", "sel16795.man", "sel16795.pu", "sel16795.pu0", "sel16795.pu1", "sel16795.q1c", "sel16795.qt1", "sel16795.xws",
    "sel17152.atr", "sel17152.dat", "sel17152.hea", "sel17152.hea-", "sel17152.man", "sel17152.pu", "sel17152.pu0", "sel17152.pu1", "sel17152.q1c", "sel17152.qt1", "sel17152.xws",
    "sel17453.atr", "sel17453.dat", "sel17453.hea", "sel17453.hea-", "sel17453.man", "sel17453.pu", "sel17453.pu0", "sel17453.pu1", "sel17453.q1c", "sel17453.qt1", "sel17453.xws",
    "sel213.atr", "sel213.dat", "sel213.hea", "sel213.man", "sel213.pu", "sel213.pu0", "sel213.pu1", "sel213.q1c", "sel213.q2c", "sel213.qt1", "sel213.qt2", "sel213.xws",
    "sel221.atr", "sel221.dat", "sel221.hea", "sel221.man", "sel221.pu", "sel221.pu0", "sel221.pu1", "sel221.q1c", "sel221.q2c", "sel221.qt1", "sel221.qt2", "sel221.xws",
    "sel223.atr", "sel223.dat", "sel223.hea", "sel223.man", "sel223.pu", "sel223.pu0", "sel223.pu1", "sel223.q1c", "sel223.q2c", "sel223.qt1", "sel223.qt2", "sel223.xws",
    "sel230.atr", "sel230.dat", "sel230.hea", "sel230.man", "sel230.pu", "sel230.pu0", "sel230.pu1", "sel230.q1c", "sel230.q2c", "sel230.qt1", "sel230.qt2", "sel230.xws",
    "sel231.atr", "sel231.dat", "sel231.hea", "sel231.man", "sel231.pu", "sel231.pu0", "sel231.pu1", "sel231.q1c", "sel231.qt1", "sel231.xws",
    "sel232.atr", "sel232.dat", "sel232.hea", "sel232.man", "sel232.pu", "sel232.pu0", "sel232.pu1", "sel232.q1c", "sel232.qt1", "sel232.xws",
    "sel233.atr", "sel233.dat", "sel233.hea", "sel233.man", "sel233.pu", "sel233.pu0", "sel233.pu1", "sel233.q1c", "sel233.qt1", "sel233.xws",
    "sel30.dat", "sel30.hea", "sel30.hea-", "sel30.man", "sel30.pu", "sel30.pu0", "sel30.pu1", "sel30.q1c", "sel30.qt1", "sel30.xws",
    "sel301.atr", "sel301.dat", "sel301.hea", "sel301.hea-", "sel301.man", "sel301.pu", "sel301.pu0", "sel301.pu1", "sel301.q1c", "sel301.qt1", "sel301.xws",
    "sel302.atr", "sel302.dat", "sel302.hea", "sel302.hea-", "sel302.man", "sel302.pu", "sel302.pu0", "sel302.pu1", "sel302.q1c", "sel302.qt1", "sel302.xws",
    "sel306.atr", "sel306.dat", "sel306.hea", "sel306.hea-", "sel306.man", "sel306.pu", "sel306.pu0", "sel306.pu1", "sel306.q1c", "sel306.qt1", "sel306.xws",
    "sel307.atr", "sel307.dat", "sel307.hea", "sel307.hea-", "sel307.man", "sel307.pu", "sel307.pu0", "sel307.pu1", "sel307.q1c", "sel307.qt1", "sel307.xws",
    "sel308.atr", "sel308.dat", "sel308.hea", "sel308.hea-", "sel308.man", "sel308.pu", "sel308.pu0", "sel308.pu1", "sel308.q1c", "sel308.qt1", "sel308.xws",
    "sel31.dat", "sel31.hea", "sel31.hea-", "sel31.man", "sel31.pu", "sel31.pu0", "sel31.pu1", "sel31.q1c", "sel31.qt1", "sel31.xws",
    "sel310.atr", "sel310.dat", "sel310.hea", "sel310.hea-", "sel310.man", "sel310.pu", "sel310.pu0", "sel310.pu1", "sel310.q1c", "sel310.qt1", "sel310.xws",
    "sel32.dat", "sel32.hea", "sel32.hea-", "sel32.man", "sel32.pu", "sel32.pu0", "sel32.pu1", "sel32.q1c", "sel32.qt1", "sel32.xws",
    "sel33.dat", "sel33.hea", "sel33.hea-", "sel33.man", "sel33.pu", "sel33.pu0", "sel33.pu1", "sel33.q1c", "sel33.qt1", "sel33.xws",
    "sel34.dat", "sel34.hea", "sel34.hea-", "sel34.man", "sel34.pu", "sel34.pu0", "sel34.pu1", "sel34.q1c", "sel34.qt1", "sel34.xws",
    "sel35.dat", "sel35.hea", "sel35.hea-", "sel35.man", "sel35.pu", "sel35.pu0", "sel35.pu1", "sel35.q1c", "sel35.qt1", "sel35.xws",
    "sel36.dat", "sel36.hea", "sel36.hea-", "sel36.man", "sel36.pu", "sel36.pu0", "sel36.pu1", "sel36.q1c", "sel36.qt1", "sel36.xws",
    "sel37.dat", "sel37.hea", "sel37.hea-", "sel37.man", "sel37.pu", "sel37.pu0", "sel37.pu1", "sel37.q1c", "sel37.qt1", "sel37.xws",
    "sel38.dat", "sel38.hea", "sel38.hea-", "sel38.man", "sel38.pu", "sel38.pu0", "sel38.pu1", "sel38.q1c", "sel38.qt1", "sel38.xws",
    "sel39.dat", "sel39.hea", "sel39.hea-", "sel39.man", "sel39.pu", "sel39.pu0", "sel39.pu1", "sel39.q1c", "sel39.qt1", "sel39.xws",
    "sel40.dat", "sel40.hea", "sel40.hea-", "sel40.man", "sel40.pu", "sel40.pu0", "sel40.pu1", "sel40.q1c", "sel40.qt1", "sel40.xws",
    "sel41.dat", "sel41.hea", "sel41.hea-", "sel41.man", "sel41.pu", "sel41.pu0", "sel41.pu1", "sel41.q1c", "sel41.qt1", "sel41.xws",
    "sel42.dat", "sel42.hea", "sel42.hea-", "sel42.man", "sel42.pu", "sel42.pu0", "sel42.pu1", "sel42.q1c", "sel42.qt1", "sel42.xws",
    "sel43.dat", "sel43.hea", "sel43.hea-", "sel43.man", "sel43.pu", "sel43.pu0", "sel43.pu1", "sel43.q1c", "sel43.qt1", "sel43.xws",
    "sel44.dat", "sel44.hea", "sel44.hea-", "sel44.man", "sel44.pu", "sel44.pu0", "sel44.pu1", "sel44.q1c", "sel44.qt1", "sel44.xws",
    "sel45.dat", "sel45.hea", "sel45.hea-", "sel45.man", "sel45.pu", "sel45.pu0", "sel45.pu1", "sel45.q1c", "sel45.qt1", "sel45.xws",
    "sel46.dat", "sel46.hea", "sel46.hea-", "sel46.man", "sel46.pu", "sel46.pu0", "sel46.pu1", "sel46.q1c", "sel46.qt1", "sel46.xws",
    "sel47.dat", "sel47.hea", "sel47.hea-", "sel47.man", "sel47.pu", "sel47.pu0", "sel47.pu1", "sel47.q1c", "sel47.qt1", "sel47.xws",
    "sel48.dat", "sel48.hea", "sel48.hea-", "sel48.man", "sel48.pu", "sel48.pu0", "sel48.pu1", "sel48.q1c", "sel48.qt1", "sel48.xws",
    "sel49.dat", "sel49.hea", "sel49.hea-", "sel49.man", "sel49.pu", "sel49.pu0", "sel49.pu1", "sel49.q1c", "sel49.qt1", "sel49.xws",
    "sel50.dat", "sel50.hea", "sel50.hea-", "sel50.man", "sel50.pu", "sel50.pu0", "sel50.pu1", "sel50.q1c", "sel50.qt1", "sel50.xws",
    "sel51.dat", "sel51.hea", "sel51.hea-", "sel51.man", "sel51.pu", "sel51.pu0", "sel51.pu1", "sel51.q1c", "sel51.qt1", "sel51.xws",
    "sel52.dat", "sel52.hea", "sel52.hea-", "sel52.man", "sel52.pu", "sel52.pu0", "sel52.pu1", "sel52.q1c", "sel52.qt1", "sel52.xws",
    "sel803.atr", "sel803.dat", "sel803.hea", "sel803.hea-", "sel803.man", "sel803.pu", "sel803.pu0", "sel803.pu1", "sel803.q1c", "sel803.qt1", "sel803.xws",
    "sel808.atr", "sel808.dat", "sel808.hea", "sel808.hea-", "sel808.man", "sel808.pu", "sel808.pu0", "sel808.pu1", "sel808.q1c", "sel808.qt1", "sel808.xws",
    "sel811.atr", "sel811.dat", "sel811.hea", "sel811.hea-", "sel811.man", "sel811.pu", "sel811.pu0", "sel811.pu1", "sel811.q1c", "sel811.qt1", "sel811.xws",
    "sel820.atr", "sel820.dat", "sel820.hea", "sel820.hea-", "sel820.man", "sel820.pu", "sel820.pu0", "sel820.pu1", "sel820.q1c", "sel820.qt1", "sel820.xws",
    "sel821.atr", "sel821.dat", "sel821.hea", "sel821.hea-", "sel821.man", "sel821.pu", "sel821.pu0", "sel821.pu1", "sel821.q1c", "sel821.qt1", "sel821.xws",
    "sel840.atr", "sel840.dat", "sel840.hea", "sel840.hea-", "sel840.man", "sel840.pu", "sel840.pu0", "sel840.pu1", "sel840.q1c", "sel840.qt1", "sel840.xws",
    "sel847.atr", "sel847.dat", "sel847.hea", "sel847.hea-", "sel847.man", "sel847.pu", "sel847.pu0", "sel847.pu1", "sel847.q1c", "sel847.qt1", "sel847.xws",
    "sel853.atr", "sel853.dat", "sel853.hea", "sel853.hea-", "sel853.man", "sel853.pu", "sel853.pu0", "sel853.pu1", "sel853.q1c", "sel853.qt1", "sel853.xws",
    "sel871.atr", "sel871.dat", "sel871.hea", "sel871.hea-", "sel871.man", "sel871.pu", "sel871.pu0", "sel871.pu1", "sel871.q1c", "sel871.qt1", "sel871.xws",
    "sel872.atr", "sel872.dat", "sel872.hea", "sel872.hea-", "sel872.man", "sel872.pu", "sel872.pu0", "sel872.pu1", "sel872.q1c", "sel872.qt1", "sel872.xws",
    "sel873.atr", "sel873.dat", "sel873.hea", "sel873.hea-", "sel873.man", "sel873.pu", "sel873.pu0", "sel873.pu1", "sel873.q1c", "sel873.qt1", "sel873.xws",
    "sel883.atr", "sel883.dat", "sel883.hea", "sel883.hea-", "sel883.man", "sel883.pu", "sel883.pu0", "sel883.pu1", "sel883.q1c", "sel883.qt1", "sel883.xws",
    "sel891.atr", "sel891.dat", "sel891.hea", "sel891.hea-", "sel891.man", "sel891.pu", "sel891.pu0", "sel891.pu1", "sel891.q1c", "sel891.qt1", "sel891.xws",
    "sele0104.atr", "sele0104.dat", "sele0104.hea", "sele0104.man", "sele0104.pu", "sele0104.pu0", "sele0104.pu1", "sele0104.q1c", "sele0104.qt1", "sele0104.xws",
    "sele0106.atr", "sele0106.dat", "sele0106.hea", "sele0106.man", "sele0106.pu", "sele0106.pu0", "sele0106.pu1", "sele0106.q1c", "sele0106.qt1", "sele0106.xws",
    "sele0107.atr", "sele0107.dat", "sele0107.hea", "sele0107.man", "sele0107.pu", "sele0107.pu0", "sele0107.pu1", "sele0107.q1c", "sele0107.qt1", "sele0107.xws",
    "sele0110.atr", "sele0110.dat", "sele0110.hea", "sele0110.man", "sele0110.pu", "sele0110.pu0", "sele0110.pu1", "sele0110.q1c", "sele0110.qt1", "sele0110.xws",
    "sele0111.atr", "sele0111.dat", "sele0111.hea", "sele0111.man", "sele0111.pu", "sele0111.pu0", "sele0111.pu1", "sele0111.q1c", "sele0111.qt1", "sele0111.xws",
    "sele0112.atr", "sele0112.dat", "sele0112.hea", "sele0112.man", "sele0112.pu", "sele0112.pu0", "sele0112.pu1", "sele0112.q1c", "sele0112.qt1", "sele0112.xws",
    "sele0114.atr", "sele0114.dat", "sele0114.hea", "sele0114.man", "sele0114.pu", "sele0114.pu0", "sele0114.pu1", "sele0114.q1c", "sele0114.qt1", "sele0114.xws",
    "sele0116.atr", "sele0116.dat", "sele0116.hea", "sele0116.man", "sele0116.pu", "sele0116.pu0", "sele0116.pu1", "sele0116.q1c", "sele0116.qt1", "sele0116.xws",
    "sele0121.atr", "sele0121.dat", "sele0121.hea", "sele0121.man", "sele0121.pu", "sele0121.pu0", "sele0121.pu1", "sele0121.q1c", "sele0121.qt1", "sele0121.xws",
    "sele0122.atr", "sele0122.dat", "sele0122.hea", "sele0122.man", "sele0122.pu", "sele0122.pu0", "sele0122.pu1", "sele0122.q1c", "sele0122.qt1", "sele0122.xws",
    "sele0124.atr", "sele0124.dat", "sele0124.hea", "sele0124.man", "sele0124.pu", "sele0124.pu0", "sele0124.pu1", "sele0124.q1c", "sele0124.qt1", "sele0124.xws",
    "sele0126.atr", "sele0126.dat", "sele0126.hea", "sele0126.man", "sele0126.pu", "sele0126.pu0", "sele0126.pu1", "sele0126.q1c", "sele0126.qt1", "sele0126.xws",
    "sele0129.atr", "sele0129.dat", "sele0129.hea", "sele0129.man", "sele0129.pu", "sele0129.pu0", "sele0129.pu1", "sele0129.q1c", "sele0129.qt1", "sele0129.xws",
    "sele0133.atr", "sele0133.dat", "sele0133.hea", "sele0133.man", "sele0133.pu", "sele0133.pu0", "sele0133.pu1", "sele0133.q1c", "sele0133.qt1", "sele0133.xws",
    "sele0136.atr", "sele0136.dat", "sele0136.hea", "sele0136.man", "sele0136.pu", "sele0136.pu0", "sele0136.pu1", "sele0136.q1c", "sele0136.qt1", "sele0136.xws",
    "sele0166.atr", "sele0166.dat", "sele0166.hea", "sele0166.man", "sele0166.pu", "sele0166.pu0", "sele0166.pu1", "sele0166.q1c", "sele0166.qt1", "sele0166.xws",
    "sele0170.atr", "sele0170.dat", "sele0170.hea", "sele0170.man", "sele0170.pu", "sele0170.pu0", "sele0170.pu1", "sele0170.q1c", "sele0170.qt1", "sele0170.xws",
    "sele0203.atr", "sele0203.dat", "sele0203.hea", "sele0203.man", "sele0203.pu", "sele0203.pu0", "sele0203.pu1", "sele0203.q1c", "sele0203.qt1", "sele0203.xws",
    "sele0210.atr", "sele0210.dat", "sele0210.hea", "sele0210.man", "sele0210.pu", "sele0210.pu0", "sele0210.pu1", "sele0210.q1c", "sele0210.qt1", "sele0210.xws",
    "sele0211.atr", "sele0211.dat", "sele0211.hea", "sele0211.man", "sele0211.pu", "sele0211.pu0", "sele0211.pu1", "sele0211.q1c", "sele0211.qt1", "sele0211.xws",
    "sele0303.atr", "sele0303.dat", "sele0303.hea", "sele0303.man", "sele0303.pu", "sele0303.pu0", "sele0303.pu1", "sele0303.q1c", "sele0303.qt1", "sele0303.xws",
    "sele0405.atr", "sele0405.dat", "sele0405.hea", "sele0405.man", "sele0405.pu", "sele0405.pu0", "sele0405.pu1", "sele0405.q1c", "sele0405.qt1", "sele0405.xws",
    "sele0406.atr", "sele0406.dat", "sele0406.hea", "sele0406.man", "sele0406.pu", "sele0406.pu0", "sele0406.pu1", "sele0406.q1c", "sele0406.qt1", "sele0406.xws",
    "sele0409.atr", "sele0409.dat", "sele0409.hea", "sele0409.man", "sele0409.pu", "sele0409.pu0", "sele0409.pu1", "sele0409.q1c", "sele0409.qt1", "sele0409.xws",
    "sele0411.atr", "sele0411.dat", "sele0411.hea", "sele0411.man", "sele0411.pu", "sele0411.pu0", "sele0411.pu1", "sele0411.q1c", "sele0411.qt1", "sele0411.xws",
    "sele0509.atr", "sele0509.dat", "sele0509.hea", "sele0509.man", "sele0509.pu", "sele0509.pu0", "sele0509.pu1", "sele0509.q1c", "sele0509.qt1", "sele0509.xws",
    "sele0603.atr", "sele0603.dat", "sele0603.hea", "sele0603.man", "sele0603.pu", "sele0603.pu0", "sele0603.pu1", "sele0603.q1c", "sele0603.qt1", "sele0603.xws",
    "sele0604.atr", "sele0604.dat", "sele0604.hea", "sele0604.man", "sele0604.pu", "sele0604.pu0", "sele0604.pu1", "sele0604.q1c", "sele0604.qt1", "sele0604.xws",
    "sele0606.atr", "sele0606.dat", "sele0606.hea", "sele0606.man", "sele0606.pu", "sele0606.pu0", "sele0606.pu1", "sele0606.q1c", "sele0606.qt1", "sele0606.xws",
    "sele0607.atr", "sele0607.dat", "sele0607.hea", "sele0607.man", "sele0607.pu", "sele0607.pu0", "sele0607.pu1", "sele0607.q1c", "sele0607.qt1", "sele0607.xws",
    "sele0609.atr", "sele0609.dat", "sele0609.hea", "sele0609.man", "sele0609.pu", "sele0609.pu0", "sele0609.pu1", "sele0609.q1c", "sele0609.qt1", "sele0609.xws",
    "sele0612.atr", "sele0612.dat", "sele0612.hea", "sele0612.man", "sele0612.pu", "sele0612.pu0", "sele0612.pu1", "sele0612.q1c", "sele0612.qt1", "sele0612.xws",
    "sele0704.atr", "sele0704.dat", "sele0704.hea", "sele0704.man", "sele0704.pu", "sele0704.pu0", "sele0704.pu1", "sele0704.q1c", "sele0704.qt1", "sele0704.xws"
]

# Crear directorio para los archivos si no existe
if not os.path.exists('QT_Database'):
    os.makedirs('QT_Database')

# Función para obtener el nombre base del archivo
def obtener_nombre_base(archivo):
    # Eliminar la extensión
    nombre_base = os.path.splitext(archivo)[0]
    # Si el archivo tiene múltiples puntos (como .hea-), tomar solo la primera parte
    nombre_base = nombre_base.split('.')[0]
    return nombre_base

# Función para descargar un archivo
def descargar_archivo(archivo):
    url = BASE_URL + archivo
    nombre_base = obtener_nombre_base(archivo)
    ruta_local = os.path.join('QT_Database', nombre_base, archivo)
    
    # Crear directorio para el archivo si no existe
    os.makedirs(os.path.dirname(ruta_local), exist_ok=True)
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Verificar si hay errores en la respuesta
        
        # Obtener el tamaño total del archivo
        total_size = int(response.headers.get('content-length', 0))
        
        # Descargar el archivo con barra de progreso
        with open(ruta_local, 'wb') as f, tqdm(
            desc=archivo,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as barra:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                barra.update(size)
        
        return True
    except Exception as e:
        print(f"Error al descargar {archivo}: {str(e)}")
        return False

# Descargar cada archivo
print("Iniciando descarga de archivos...")
archivos_exitosos = 0
archivos_fallidos = []

for archivo in archivos:
    if descargar_archivo(archivo):
        archivos_exitosos += 1
    else:
        archivos_fallidos.append(archivo)

# Mostrar resumen
print("\nResumen de la descarga:")
print(f"Total de archivos: {len(archivos)}")
print(f"Archivos descargados exitosamente: {archivos_exitosos}")
print(f"Archivos fallidos: {len(archivos_fallidos)}")

if archivos_fallidos:
    print("\nArchivos que fallaron:")
    for archivo in archivos_fallidos:
        print(f"- {archivo}") 