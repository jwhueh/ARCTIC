#! /usr/bin/python

"""
arctic_quicklook.py
Take single and self.quad mode imaging and remove overscan

TODO:
create quick reduction options

Usage:
  single image reduce:	arctic_quicklook.py -d [dir] -i [image_name]
  continuous (buggy): arctic_quicklook.py -d [dir] -w

Options:
  -d, --dir	directory for continuous look, if no directory gived it will default to current working directory
  -i, --im	single image
  -f, --flat	flat image to use for quick reduction
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
__version__ = "0.4"
__maintainer__ = "Joseph Huehnerhof"
__email__ = "jwhueh@uw.edu"
__status__ = "Developement"

from astropy.io import fits
import re
import numpy as np
import os
from scipy import stats
from scipy import misc
from scipy.ndimage import interpolation
import time
import getopt
import sys
import thread
import datetime

class ImageCombine(object):
	def __init__(self):
		self.quad = ['SEC11', 'SEC21', 'SEC12', 'SEC22']  #11:ll, 21:ul, 12:lr, 22:ur


	def imSplit(self, dir = None, image = None, flat = None, finder = False):
		"""
		Break image into quadrants and subtract ovserscan
		Args:
			dir (string): directory of images
			image (string): name of image
		Returns:
			image (fits,jpg): fits and jpg saved image
		"""
		data_im = os.path.join(dir,image)
		hdulist = fits.open(data_im)
		#verify that it is a quad image
		amp = hdulist[0].header['READAMPS']
		if re.search("quad",amp.lower()):
			quad_pos = self.secParser(hdulist)
			print "%s   processing quad amplifier data" % datetime.datetime.now().strftime("%H:%M:%S.%f")

			scidata = hdulist[0].data  #grab the image

			print "%s   breaking apart image into separate quadrants" % datetime.datetime.now().strftime("%H:%M:%S.%f")
			quad_dict = self.imageParser(scidata, quad_pos)
			print quad_dict
			flat_dict = {}
			try:
				if flat != None:
					flat_im = os.path.join(dir,flat)
                			flat_hdu = fits.open(flat_im)
					flatdata = flat_hdu[0].data
					if np.mean(flatdata) > 50000:
						raise ValueError
					flat_dict = self.imageParser(flatdata,quad_pos, True, quad_dict)
					flat_hdu.close()		
			except ValueError:
				print ('Not a good flat based on mean counts > 50K\n ',
					'skipping flat reduction')
				
			#stitch the image back together	
			sci_bot = np.concatenate((quad_dict['DSEC12'], quad_dict['DSEC22']), axis = 1)
                        sci_top = np.concatenate((quad_dict['DSEC11'], quad_dict['DSEC21']), axis = 1)
			sci = np.concatenate((sci_top, sci_bot), axis = 0)

			out_name = image.rstrip('.fits') + '_comp'
			try:
				if os.path.exists(out_name +'.fits'):
					os.remove(out_name+'.fits')
					os.remove(out_name+'.jpg')
			except:
				None
			im_mean = np.mean(sci)
			im_std = np.std(sci)
			im_min = im_mean - im_std
			im_max = im_mean + im_std
			if im_min < 0:
				im_min = 0.0
			if im_max >= 65000:
				im_max = 65000.0
			hdu = fits.PrimaryHDU(sci)
			hdu.writeto(out_name +'.fits')
			if finder:
				 #needs to be place before the rotation otherwise the plotting is rotated.
				finder_name = self.finderChart(image.rstrip('.fits'), hdulist, dir, sci, im_min, im_max)
			sci = interpolation.rotate(sci,180 )
			sci = np.fliplr(sci)
			im = misc.toimage(sci, cmin = im_min, cmax = im_max).save(out_name + '.jpg')
		hdulist.close()
		print "%s   saving output images:"  % datetime.datetime.now().strftime("%H:%M:%S.%f")
                print out_name + '.jpg'
                print out_name +'.fits'
		#print finder_name
	
	def finderChart(self, image_name = None, hdulist = None, dir = None, im_array = None, min = 0,max = 65000):
		"""
		Overlay a finder chart on the image
		Args:
			image_name (str): output image name
			hudlist (fits): opened fits file
			dir (str):  working directory
			im_array (array):  array for reduced data
			min (int):  minimum stretch threshold
			max (int): maximum stretch threshold

		Returns:
			plot (jpg): image of overlayed finder chart on acquired data 
		"""
		from astroplan.plots.finder import plot_finder_image
		from astroquery.skyview import SkyView
		from astropy.coordinates import SkyCoord
		import wcsaxes
		import matplotlib.pyplot as plt
		import astropy.units as u

		print "%s  Overlaying finding chart" % datetime.datetime.now().strftime("%H:%M:%S.%f")
		ra = hdulist[0].header['RA']
		dec = hdulist[0].header['DEC']
		coord = SkyCoord(ra+' ' +dec, unit=(u.hourangle,u.deg)) 
		position = coord
    		coordinates = hdulist[0].header['RADECSYS']
		
		ax, hdu = plot_finder_image(position,fov_radius=.133*u.degree)
		plt.imshow(im_array, clim=(min,max), alpha=.5, interpolation = 'nearest', origin = 'center',extent=[0,293,0,293])
		image_name = image_name + '_finder.jpg'
		plt.savefig(image_name)
		plt.close()
		return image_name

	def imageParser(self, im = None, quad_pos = None, flat = False, im_dict = None):
		"""Break the image into dictionaries and flat field if provided the data
		Args:
			im (fits): numpy array of fits image
			quad_pos (list):  quadrant boundaries in IRAF format (x1,x2, y1,y2)
			flat (bool): is there a flat field included
			im_dict (dict):  dictionary of image in numpy format

		Returns:
			dict (dict):  dictionary of image in numpy format
		"""
		dict = {}
		for i,q in enumerate(self.quad):
			try:
	                	data_name = 'D'+self.quad[i]
				overscan_name = 'B'+self.quad[i]
	                        overscan = np.mean(im[int(quad_pos[overscan_name][2]):int(quad_pos[overscan_name][3]),int(quad_pos[overscan_name][0]):int(quad_pos[overscan_name][1])])
        	                data = im[int(quad_pos[data_name][2]):int(quad_pos[data_name][3]),int(quad_pos[data_name][0]):int(quad_pos[data_name][1])]
                	        if flat:
                        	        dict[overscan_name] = overscan
                               		data  = (data - overscan) / np.median(data)
                                	dict[data_name] = data
                                	im_dict[data_name] = im_dict[data_name] / dict[data_name]
                        	else:
                                	dict[overscan_name] = overscan
                                	dict[data_name] = data

			except:
				data_name = 'A'+self.quad[i]
				print quad_pos
				#print data_name, quad_pos[data_name.replace('A','D')][2], quad_pos[data_name][3],quad_pos[data_name][0],quad_pos[data_name][1]
				data = im[int(quad_pos[data_name.replace('A','D')][2]):int(quad_pos[data_name.replace('A','D')][3]),int(quad_pos[data_name.replace('A','D')][0]):int(quad_pos[data_name.replace('A','D')][1])]
				print data
				dict[data_name.replace('A','D')] = data

		return dict

	def secParser(self, im = None):
		"""
		Break apart header ccd coordinates into numpy array format
		Args:
			im (string): astropy fitsio image format
			keyword (string): header keyword
		Returns:
			split (list) - list of ccd coordinates in IRAF coordinate system [x1, x2, y1, y2]
			
		"""
		dict = {}
		for i,q in enumerate(self.quad):
				try:
                                	data_sec = 'D'+self.quad[i]
                                	overscan_sec = 'B'+self.quad[i]
                                	dict[data_sec] = re.split('[: ,]',im[0].header[data_sec].rstrip(']').lstrip('['))
                                	dict[overscan_sec] = re.split('[: ,]',im[0].header[overscan_sec].rstrip(']').lstrip('['))
				except:
					data_sec = 'A'+self.quad[i]
					dict[data_sec.replace('A','D')] = re.split('[: ,]',im[0].header[data_sec].rstrip(']').lstrip('['))
		print dict
		return dict
		


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
		opts, args = getopt.getopt(sys.argv[1:], "hud:i:wf:s:r", ["help","usage", "dir", "image", "watch", "flat", "sky", "reduce"])
	except getopt.GetoptError as err:
		print err
		i.usage()
		sys.exit()
	dict_opts={}
	dict_opts['d'] = os.getcwd()
	dict_opts['f'] = None
	dict_opts['s'] = False
	for o, a in opts:
		dict_opts[o.lstrip('-')] = a

	if 'h' in dict_opts or 'help' in dict_opts:	
		i.usage()
	elif 'u' in dict_opts:
		help(i)
	elif 'r' in dict_opts or 'image' in dict_opts:		
		i.imSplit(dict_opts['d'],dict_opts['i'], dict_opts['f'], dict_opts['s'])
	elif 'w' in dict_opts or 'watch' in dict_opts:
		i.imCheck(dict_opts['d'])
	
