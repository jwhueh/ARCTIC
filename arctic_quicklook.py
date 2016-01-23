#! /usr/bin/python

from astropy.io import fits
import re
import numpy as np
import os
from scipy import misc
import time

class ImageCombine(object):
	def __init__(self):
		pass

	def imSplit(self, image = None):
		hdulist = fits.open(image)
		#verify that it is a quad image
		amp = hdulist[0].header['READAMPS']
		bn = int(hdulist[0].header['BINX'])
		ll = re.split('[: ,]',hdulist[0].header['CSEC11'].rstrip(']').lstrip('['))
		ul = re.split('[: ,]',hdulist[0].header['CSEC21'].rstrip(']').lstrip('['))
		lr = re.split('[: ,]',hdulist[0].header['CSEC12'].rstrip(']').lstrip('['))
		ur = re.split('[: ,]',hdulist[0].header['CSEC22'].rstrip(']').lstrip('['))
		#print amp, ll, lr, ul, ur
		if amp == "Quad":
			scidata = hdulist[0].data  #grab the iamge
			#assign subregions without the bias
			#print int(lr[0])/bn,int(lr[1])/bn,int(lr[2])/bn,int(lr[3])/bn
			scidata_ll = scidata[int(ll[0])/bn:int(ll[1])/bn,int(ll[2])/bn:int(ll[3])/bn]
			scidata_lr = scidata[int(lr[0])/bn:int(lr[1])/bn,int(lr[2])/bn+100:int(lr[3])/bn + 100]
			scidata_ul = scidata[int(ul[0])/bn:int(ul[1])/bn,int(ul[2])/bn:int(ul[3])/bn]
			scidata_ur = scidata[int(ur[0])/bn:int(ur[1])/bn,int(ur[2])/bn + 100:int(ur[3])/bn + 100]

			sci_bot = np.concatenate((scidata_ll, scidata_lr), axis = 1)
			sci_top = np.concatenate((scidata_ul, scidata_ur), axis = 1)
			sci = np.concatenate((sci_bot, sci_top), axis = 0)

			out_name = image.rstrip('.fits') + '_comp'
			if os.path.exists(out_name +'.fits'):
				os.remove(out_name+'.fits')
				os.remove(out_name+'.jpg')
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
			im = misc.toimage(sci, cmin = im_min, cmax = im_max).save(out_name + '.jpg')
		hdulist.close()


	def imCheck(self, path_to_watch):
		before = dict ([(f, None) for f in os.listdir (path_to_watch)])
		while True:
			after = dict ([(f, None) for f in os.listdir (path_to_watch)])
	        	added = [f for f in after if not f in before]
        		removed = [f for f in before if not f in after]
			print added
			if added and re.search('.fits',added[0]) and not re.search('_comp.fits', added[0]):
				im_add = os.path.join(path_to_watch, added[0])
				while os.path.getsize(im_add)/(1024*1024) < 8:
					time.sleep(1)
				self.imSplit(os.path.join(path_to_watch, added[0]))
			before = after
			time.sleep(1)
			

if __name__ == "__main__":
	i = ImageCombine()
	#i.imSplit('bias_med.0092.fits')
	i.imCheck('/Users/jwhueh/TUI_Images/Q1APO/UT160123/arctic_linearity_2/')
