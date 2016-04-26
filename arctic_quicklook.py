#! /usr/bin/python

"""
arctic_quicklook.py
Take single and quad mode imaging and remove overscan

TODO:
Make more robuse for slower internest connections
subtract overscan from image
divide by flats

Usage:
  single image reduce:	arctic_quicklook.py -d [dir] -i [image_name]
  continuous (buggy): arctic_quicklook.py -d [dir] -w

Options:
  -d, --dir	directory for continuous look, if no directory gived it will default to current working directory
  -i, --im	single image
  -w, --watch   run in continuous look mode

Output:
 [image_name]_comp.fits
 [image_name]_comp.jpg 
"""

__author__ = ["Joseph Huehnerhoff"]
__copyright__ = "NA"
__credits__ = [""]
__license__ = "GPL"
__version__ = "0.2"
__maintainer__ = "Joseph Huehnerhof"
__email__ = "NA"
__status__ = "Developement"

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
		"""
		Break image into quadrants and subtract ovserscan
		arguments:
			dir - directory of images
			image - name of image
		return:
			image - fits and jpg saved image
		"""
		image = os.path.join(dir,image)
		hdulist = fits.open(image)
		#verify that it is a quad image
		amp = hdulist[0].header['READAMPS']
		if amp == "Quad":
			print "%s   processing quad amplifier data" % time.strftime("%H:%M:%S")
			ll = self.headerParser(hdulist,'DSEC11')
			ll_os = self.headerParser(hdulist,'BSEC11')

                	ul = self.headerParser(hdulist,'DSEC21')
			ul_os = self.headerParser(hdulist,'BSEC21')

                	lr = self.headerParser(hdulist,'DSEC12')
			lr_os = self.headerParser(hdulist,'BSEC12')

                	ur = self.headerParser(hdulist,'DSEC22')
			ur_os = self.headerParser(hdulist,'BSEC22')
			
			scidata = hdulist[0].data  #grab the image

			print "%s   breaking apart image into separate quadrants" % time.strftime("%H:%M:%S")
			scidata_ll = scidata[int(ll[2]):int(ll[3]),int(ll[0]):int(ll[1])]
			osdata_ll = scidata[int(ll_os[2]):int(ll_os[3]),int(ll_os[0]):int(ll_os[1])]

                        scidata_lr = scidata[int(lr[2]):int(lr[3]),int(lr[0]):int(lr[1])]
			osdata_lr = scidata[int(lr_os[2]):int(lr_os[3]),int(lr_os[0]):int(lr_os[1])]

                        scidata_ul = scidata[int(ul[2]):int(ul[3]),int(ul[0]):int(ul[1])]
			osdata_ul = scidata[int(ul_os[2]):int(ul_os[3]),int(ul_os[0]):int(ul_os[1])]

                        scidata_ur = scidata[int(ur[2]):int(ur[3]),int(ur[0]):int(ur[1])]
			osdata_ur = scidata[int(ur_os[2]):int(ur_os[3]),int(ur_os[0]):int(ur_os[1])]

			print "%s   subtracting overscan" % time.strftime("%H:%M:%S")
			scidata_ll = scidata_ll - np.mean(osdata_ll)
			scidata_lr = scidata_lr - np.mean(osdata_lr)
			scidata_ul = scidata_ul - np.mean(osdata_ul)
			scidata_ur = scidata_ur - np.mean(osdata_ur)

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
			#print im_mean, np.std(sci)
			im_std = np.std(sci)
			im_min = im_mean - im_std
			im_max = im_mean + im_std
			if im_min <0:
				im_min = 0.0
			if im_max >=65000:
				im_max = 65000.0
			print "%s   saving output images:"  % time.strftime("%H:%M:%S")
			print out_name + '.jpg'
			print out_name +'.fits'
			hdu = fits.PrimaryHDU(sci)
			hdu.writeto(out_name +'.fits')
			sci = interpolation.rotate(sci,180 )
			sci = np.fliplr(sci)
			im = misc.toimage(sci, cmin = im_min, cmax = im_max).save(out_name + '.jpg')
		hdulist.close()

	def headerParser(self, im = None, keyword = None):
		"""
		Break apart header ccd coordinates into numpy array format
		arguments:
			im - astropy fitsio image format
			keyword - header keyword
		return:
			split - list of ccd coordinates in IRAF coordinate system [x1, x2, y1, y2]
			
		"""
		split = re.split('[: ,]',im[0].header[keyword].rstrip(']').lstrip('['))
		return split
		


	def imCheck(self, path_to_watch = None):
		"""
		look in a given directory for new images and process
		arguments:
			path_to_watch - directory to look for new images
		return:
			None
		"""
		before = dict ([(f, None) for f in os.listdir (path_to_watch)])
		while True:
			after = dict ([(f, None) for f in os.listdir (path_to_watch)])
	        	added = [f for f in after if not f in before]
        		removed = [f for f in before if not f in after]
			if added and re.search('.fits',added[0]) and not re.search('_comp.fits', added[0]):
				size = 0
				im_add = os.path.join(path_to_watch, added[0])
				while size - os.path.getsize(im_add) !=0:
					size = os.path.getsize(im_add)
					print "downlading: %s mb" % str(int(os.path.getsize(im_add))/(1024*1024))
					time.sleep(1)
				self.imSplit(path_to_watch, added[0])
			before = after
			time.sleep(1)

if __name__ == "__main__":
	i = ImageCombine()
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h:d:i:w", ["help", "dir", "im", "watch"])
	except getopt.GetoptError as err:
		print err
		help(i)
		sys.exit()
	im = None
        dir = os.getcwd()
	for o, a in opts:
		if o in ('-d','--dir'):
			dir = a
		if o in ('-i','--im'):		
			im = a	
			i.imSplit(dir,im)
		if o in ('-w','--watch'):
			i.imCheck(dir)
