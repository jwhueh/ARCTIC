#! /usr/bin/python

from astropy.io import fits
import re
import numpy as np
import os
from scipy import misc
from scipy.ndimage import interpolation
import time
import getopt
import sys

class ImageCombine(object):
	def __init__(self):
		pass

	def imSplit(self, dir = None, image = None):
		if dir == None:
			dir = os.getcwd()
		print dir, image
		image = os.path.join(dir,image)
		print image
		hdulist = fits.open(image)
		#verify that it is a quad image
		amp = hdulist[0].header['READAMPS']
		bn = int(hdulist[0].header['BINX'])
		ll = re.split('[: ,]',hdulist[0].header['DSEC11'].rstrip(']').lstrip('['))
		ul = re.split('[: ,]',hdulist[0].header['DSEC21'].rstrip(']').lstrip('['))
		lr = re.split('[: ,]',hdulist[0].header['DSEC12'].rstrip(']').lstrip('['))
		ur = re.split('[: ,]',hdulist[0].header['DSEC22'].rstrip(']').lstrip('['))
		print amp, ll, lr, ul, ur
		if amp == "Quad":
			scidata = hdulist[0].data  #grab the iamge
			#assign subregions without the bias
			scidata_ll = scidata[int(ll[2]):int(ll[3]),int(ll[0]):int(ll[1])]
                        scidata_lr = scidata[int(lr[2]):int(lr[3]),int(lr[0]):int(lr[1])]
                        scidata_ul = scidata[int(ul[2]):int(ul[3]),int(ul[0]):int(ul[1])]
                        scidata_ur = scidata[int(ur[2]):int(ur[3]),int(ur[0]):int(ur[1])]

			sci_bot = np.concatenate((scidata_lr, scidata_ur), axis = 1)
			sci_top = np.concatenate((scidata_ll, scidata_ul), axis = 1)
			sci = np.concatenate((sci_top, sci_bot), axis = 0)

			out_name = image.rstrip('.fits') + '_comp'
			try:
				if os.path.exists(out_name +'.fits'):
					os.remove(out_name+'.fits')
					os.remove(out_name+'.jpg')
			except:
				None
			im_mean = np.mean(sci)
			print im_mean, np.std(sci)
			im_std = np.std(sci)
			im_min = im_mean - im_std
			im_max = im_mean + im_std
			if im_min <0:
				im_min = 0.0
			if im_max >=65000:
				im_max = 65000.0
			hdu = fits.PrimaryHDU(sci)
			hdu.writeto(out_name +'.fits')
			sci = interpolation.rotate(sci,180 )
			sci = np.fliplr(sci)
			im = misc.toimage(sci, cmin = im_min, cmax = im_max).save(out_name + '.jpg')
		hdulist.close()


	def imCheck(self, path_to_watch):
		before = dict ([(f, None) for f in os.listdir (path_to_watch)])
		while True:
			after = dict ([(f, None) for f in os.listdir (path_to_watch)])
	        	added = [f for f in after if not f in before]
        		removed = [f for f in before if not f in after]
			if added and re.search('.fits',added[0]) and not re.search('_comp.fits', added[0]):
				print added
				im_add = os.path.join(path_to_watch, added[0])
				while os.path.getsize(im_add)/(1024*1024) < 8:
					time.sleep(1)
				self.imSplit(os.path.join(path_to_watch, added[0]))
			before = after
			time.sleep(1)
	def usage(self):
		print 'usage'	

if __name__ == "__main__":
	i = ImageCombine()
	try:
		opts, args = getopt.getopt(sys.argv[1:], "rh:d:i:", ["reduce","help", "dir", "im"])
	except getopt.GetoptError as err:
		print(err)
		i.usage()
		sys.exit()
	print opts,args
	im = None
        dir = None
	for o, a in opts:
		print o,a
		if o in ('-d','--dir'):
			dir = a
		if o in ('-i','--im'):		
			im = a	
		if o in ('-w','--watch'):
			i.imCheck(dir)
		if o in ('-r', '--reduce'):
			print dir, im
			i.imSplit(dir, im)
