import numpy as np
import cv2,datetime,glob
from PIL import Image, ImageGrab
from osgeo import gdal

import cv2 as cv

class Tif():
    def __init__(self):
        super(Tif, self).__init__()
        self.dataset2 = None
    def read_img(self,filepath):
        try:
            print(filepath)
            dataset1 = gdal.Open(filepath[0])
            im_width = dataset1.RasterXSize  # 栅格矩阵的列数
            im_height = dataset1.RasterYSize  # 栅格矩阵的行数
            im_geotrans = dataset1.GetGeoTransform()  # 仿射矩阵
            im_proj = dataset1.GetProjection()  # 地图投影信息
            im_data = dataset1.ReadAsArray(0, 0, im_width, im_height)  # 将数据写成数组，对应栅格矩阵

            del dataset1  # 关闭对象，文件dataset
            return im_proj, im_geotrans, im_data, im_width, im_height
            print(im_geotrans)
            print(im_proj)
            print(im_data)
        except Exception as e:
            print(e)
            pass

    def write_img(self,filename,im_proj,im_geotrans,im_data):
        # 判断栅格数据的数据类型
        if 'int8' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
        else:
            datatype = gdal.GDT_Float32

            # 判读数组维数
        if len(im_data.shape) == 3:
            im_bands, im_height, im_width = im_data.shape
        else:
            im_bands, (im_height, im_width) = 1, im_data.shape
            # 创建文件
            driver = gdal.GetDriverByName("GTiff")  # 数据类型必须有，因为要计算需要多大内存空间
            self.dataset2 = driver.Create(filename, im_width, im_height, im_bands, datatype)

            self.dataset2.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
            self.dataset2.SetProjection(im_proj)  # 写入投影

        if im_bands == 1:
            self.dataset2.GetRasterBand(1).WriteArray(im_data)  # 写入数组数据
        else:
            for i in range(im_bands):
                self.dataset2.GetRasterBand(i + 1).WriteArray(im_data[i])

        del self.dataset2

    def getIMgs(self,filename):
        try:
            proj, geotrans, data1, row1, column1 = self.read_img(filename)  # 读数据,获取tif图像的信息
            dataIMg = cv2.imread(filename[0],-1)
            timestr = str(datetime.datetime.now()).replace(':', '_')
            fn = "D:\\Pictures\\Camera Roll\\" + timestr + ".tif"
            datades = np.array((dataIMg),dtype=data1.dtype)
            self.write_img(fn,proj,geotrans,datades)
        except Exception as e:
            print(e)
            pass

    def tiffs(self,filename):
        try:
            timestr = str(datetime.datetime.now()).replace(':', '_')
            fn = "D:\\Pictures\\Camera Roll\\" + timestr + ".tif"
            for i in glob.glob(r'%s'%filename[0]):
                im = Image.open(i, "r")
                print(i.split(".")[0])
                im.save("{}_new.tif".format(i.split(".")[0]), quality=95)
        except Exception as e:
            pass

    def getWord(self):
        filename = 'filename.png'
        img = cv.imread(cv.samples.findFile(filename))
        cImage = np.copy(img)  # image to draw linescv.imshow("image", img) #name the window as "image"
        cv.waitKey(0)
        cv.destroyWindow("image")  # close the window