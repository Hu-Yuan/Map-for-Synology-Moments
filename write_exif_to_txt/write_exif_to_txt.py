#coding=utf-8
import os
import sys
import exifread

reload(sys)
sys.setdefaultencoding('utf-8')

#Image DateTime: 拍摄时间,  2015-06-24 13:18:42
#GPS GPSLatitude: GPS纬度(N),   [39, 16, 2259/50]
#GPS GPSLongitude: GPS经度(E),   [99, 48, 897/25]

def covert_gps(n1, n2, n3):
    return float(n1) + (float(n2) / 60) + (float(n3) / 3600)
    # [39, 16, 2259/50]
    # [99, 48, 897/25]
    # 39 + 16/60 + (2259/50)/3600 = 39.279216667
    # 99 + 48/60 + (897/25)/3600 = 99.809966667

def read_exif(path):
    Image_DateTime=GPS_GPSLongitude=GPS_GPSLatitude=""

    f = open(path, 'rb')
    tags = exifread.process_file(f)
    for key, value in tags.items():
        key = key.strip()
        t_value = value

        if key == 'Image DateTime':
            if ' ' in str(t_value):
                t_value = '{date} {time}'.format(date=str(t_value).split(' ')[0].replace(':', '-'),
                                                 time=str(t_value).split(' ')[1])

        if key in ['GPS GPSLatitude', 'GPS GPSLongitude']:
            tmp_v = str(t_value).replace('[', '').replace(']', '').split(', ')
            for i in range(len(tmp_v)):
                 if '/' in tmp_v[i]:
                    tmp_v[i] = float(int(tmp_v[i].split('/')[0]) / int(tmp_v[i].split('/')[1]))
                 else:
                    tmp_v[i] = float(int(tmp_v[i]))
            t_value = round(covert_gps(tmp_v[0], tmp_v[1], tmp_v[2]),4)

        if key == 'Image DateTime':
            Image_DateTime = t_value
        elif key == 'GPS GPSLongitude':
            GPS_GPSLongitude = t_value
        elif key == 'GPS GPSLatitude':
            GPS_GPSLatitude = t_value
        else:
            pass

    if GPS_GPSLongitude != "" and GPS_GPSLatitude != 0.0:
        with open('exif.txt', 'a') as f:
            Web_Path=path.split('/')[-2] + "/" + path.split('/')[-1]
            f.write(Web_Path +','+ str(Image_DateTime) +','+ str(GPS_GPSLongitude) +','+ str(GPS_GPSLatitude) +"\n")

def walkFile(album):
    for lists in os.listdir(album):
        path = os.path.join(album, lists)
        if os.path.isdir(path):
            for photo in os.listdir(path):
                p = os.path.join(path, photo)
                if os.path.isfile(p):
                    p_format = p.split(".")[-1]
                    if p_format in ["png","PNG","jpeg","JPEG","jpg","JPG"]:
                        read_exif(p)

walkFile("/volume1/web/Moments/Mobile/itachi的 iPhone")