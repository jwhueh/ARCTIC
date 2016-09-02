#! /usr/bin/python

from astropy.io import fits
import os
import re

fi = os.listdir(os.getcwd())

for f in fi:
	if re.search('fits',f):
		try:
			new_imtyp = None
			print "Accessing file: ", f
			data, header = fits.getdata(f, header=True)
                	imtyp = header['IMAGETYP']
			header['TSEC11'] = header['DSEC11']
			header['TSEC12'] = header['DSEC12']     
			header['TSEC21'] = header['DSEC21']     
			header['TSEC22'] = header['DSEC22']     	
			header['CSEC11'] = header['DSEC11']
                        header['CSEC12'] = header['DSEC12']
                        header['CSEC21'] = header['DSEC21']
                        header['CSEC22'] = header['DSEC22']
			#header['ASEC11'] = '[3:1051,1:1024]'
			#header['ASEC12'] = '[3:1051,1027:2050]'
			#header['ASEC21'] = '[1052:2100,1:1024]'
			#header['ASEC22'] = '[1052:2100,1027:2050]'
			header['NAMPSYX'] = '2 2'
			if "Bias" in imtyp:
				new_imtyp = "zero"
			else:
				new_imtyp = imtyp.lower()
			header['IMAGETYP'] = new_imtyp
			print "Image Type Change from: ", imtyp,"==>", new_imtyp
			fits.writeto(f, data, header, clobber=True, output_verify='ignore')
		except IOError, VerifyError:
			print "failed to update file header"
