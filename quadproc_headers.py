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
		
			if "Bias" in imtyp:
				new_imtyp = "zero"
			else:
				new_imtyp = imtyp.lower()
			header['IMAGETYP'] = new_imtyp
			print "Image Type Change from: ", imtyp,"==>", new_imtyp
			fits.writeto(f, data, header, clobber=True)
		except:
			print "failed to update file header"
