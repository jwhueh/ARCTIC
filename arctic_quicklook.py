#! /usr/bin/python

"""
arctic_quicklook.py
Take single and quad mode imaging and remove overscan

TODO:
create quick reduction options

Usage:
  single image reduce:	arctic_quicklook.py -d [dir] -i [image_name]
  continuous (buggy): arctic_quicklook.py -d [dir] -w

Options:
  -d, --dir	directory for continuous look, if no directory gived it will default to current working directory
  -i, --im	single image
  -w, --watch   run in continuous look mode
  -u, --usage	display the python help for this program
  -h, --help	diplay the python __doc__ usage information for this program

Output:
 [image_name]_comp.fits
 [image_name]_comp.jpg 
"""

__author__ = ["Joseph Huehnerhoff"]
__credits__ = ["Kolby Weisenburger"]
__license__ = "GPL"
__version__ = "0.3"
__maintainer__ = "Joseph Huehnerhof"
__email__ = "jwhueh@uw.edu"
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
import thread
import datetime

class ImageCombine(object):
	def __init__(self):
		pass

	def imSplit(self, dir = None, image = None):
		"""
		Break image into quadrants and subtract ovserscan
		Args:
			dir (string): directory of images
			image (string): name of image
		Returns:
			image (fits,jpg): fits and jpg saved image
		"""
		image = os.path.join(dir,image)
		hdulist = fits.open(image)
		#verify that it is a quad image
		amp = hdulist[0].header['READAMPS']
		if re.search("quad",amp.lower()):
			quad = ['SEC11', 'SEC21', 'SEC12', 'SEC22']
			#11:ll, 21:ul, 12:lr, 22:ur
			quad_pos={}
			print "%s   processing quad amplifier data" % datetime.datetime.now().strftime("%H:%M:%S.%f")

			for i,q in enumerate(quad):
				data_name = 'D'+quad[i]
				overscan_name = 'B'+quad[i]
				quad_pos[data_name] = self.headerParser(hdulist, data_name)
				quad_pos[overscan_name] = self.headerParser(hdulist, overscan_name)
			
			scidata = hdulist[0].data  #grab the image

			print "%s   breaking apart image into separate quadrants" % datetime.datetime.now().strftime("%H:%M:%S.%f")
			quad_data=[]
			for i,q in enumerate(quad):
				data_name = 'D'+quad[i]
                                overscan_name = 'B'+quad[i]
				
				quad_data.append(scidata[int(quad_pos[data_name][2]):int(quad_pos[data_name][3]),int(quad_pos[data_name][0]):int(quad_pos[data_name][1])] - np.mean(scidata[int(quad_pos[overscan_name][2]):int(quad_pos[overscan_name][3]),int(quad_pos[overscan_name][0]):int(quad_pos[overscan_name][1])]))

			"""sci_bot = np.concatenate((quad_data['DSEC12'], quad_data['DSEC22']), axis = 1)
                        sci_top = np.concatenate((quad_data['DSEC11'], quad_data['DSEC21']), axis = 1)"""

			sci_bot = np.concatenate((quad_data[2], quad_data[3]), axis = 1)
                        sci_top = np.concatenate((quad_data[0], quad_data[1]), axis = 1)
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
			print "%s   saving output images:"  % datetime.datetime.now().strftime("%H:%M:%S.%f")
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
		Args:
			im (string): astropy fitsio image format
			keyword (string): header keyword
		Returns:
			split (list) - list of ccd coordinates in IRAF coordinate system [x1, x2, y1, y2]
			
		"""
		split = re.split('[: ,]',im[0].header[keyword].rstrip(']').lstrip('['))
		return split
		


	def imCheck(self, path_to_watch = None):
		"""
		look in a given directory for new images and process
		Args:
			path_to_watch (string): directory to look for new images
		Returns:
			None

		ToDo:
			there should be some breakout sequence from the while loop
		"""
		before = dict ([(f, None) for f in os.listdir (path_to_watch)])
		while True:
			after = dict ([(f, None) for f in os.listdir (path_to_watch)])
	        	added = [f for f in after if not f in before]
        		removed = [f for f in before if not f in after]
			if added and re.search('.fits',added[0]) and not re.search('_comp.fits', added[0]):
				thread.start_new_thread(self.download,(path_to_watch,added[0]))
			before = after
			time.sleep(1)
		return

	def download(self, path = None, im = None):
		size = 0
                im_add = os.path.join(path, im)
                while size - os.path.getsize(im_add) !=0:
                	size = os.path.getsize(im_add)
                        print "downlading: %s mb" % (str(int(os.path.getsize(im_add))/(1024*1024)))
                        time.sleep(2)
                time.sleep(2)
                self.imSplit(path,im)
		return

	def usage(self):
		print __doc__
		print 'Author:',__author__
		print 'Credits:',__credits__
		print 'Maintainer:',__maintainer__
                print 'Maintainer Email:',__email__
		print 'License:',__license__
		print 'Version:',__version__
		print 'Status:',__status__

if __name__ == "__main__":
	i = ImageCombine()
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hud:i:w", ["help","usage", "dir", "image", "watch"])
	except getopt.GetoptError as err:
		print err
		i.usage()
		sys.exit()
	dict_opts={}
	dict_opts['d'] = os.getcwd()
	for o, a in opts:
		dict_opts[o.lstrip('-')] = a

	if 'h' in dict_opts or 'help' in dict_opts:	
		i.usage()
	elif 'u' in dict_opts:
		help(i)
	elif 'i' in dict_opts or 'image' in dict_opts:		
		i.imSplit(dict_opts['d'],dict_opts['i'])
	elif 'w' in dict_opts or 'watch' in dict_opts:
		i.imCheck(dict_opts['d'])
