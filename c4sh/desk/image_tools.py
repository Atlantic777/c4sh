import math
import subprocess
import Image
import os
import tempfile

def __image_creation(image_path):
	try:
		image = Image.open(image_path)
	except IOError, e:
		return image_path + "  NO IMAGE FOUND!"

	image = image.convert("1")
	imagedata = image.load()
	(width, height) = image.size
	imagedata_list = list()

	esc = 0x1b

	realWidth = int(math.ceil(width/3.0) * 3)
	nH = realWidth >> 8
	nL = realWidth & 0xff

	print nL ,nH

	imagedata_list.extend([esc, ord('3'), 1]) # set line spacing to 24 dots

	for y1 in xrange(0, int(math.ceil(height/24.0))): # one "line" of image data is 24 px
		imagedata_list.extend([esc, ord('*'), 33]) # set mode to bitmap, 24 dots
		imagedata_list.extend([nL, nH])            # data count.
		for x1 in xrange(0, int(math.ceil(width/3.0))): # we write 3 x (3 x 8) pixels at once
			for x2 in xrange(0,3):
				for y2 in xrange(0,3):
					tmp = 0
					for y3 in xrange(0,8):
						x = x1 * 3 + x2
						y = y1 * 24 + y2 * 8 + y3
						px = 0
						if y < height and x < width:
							px = int(not bool(imagedata[x,y]))
						tmp += px * 2**(7-y3) # pixel value
					imagedata_list.append(int(tmp));
		imagedata_list.extend([ord('\n'),ord('\r')]) #newline

	imagedata_list.extend([ord('\n'),ord('\r')]) #newline
	imagedata_list.extend([esc, ord('3'), 30]) # set linespacing back to normal

	array = bytearray(imagedata_list)

	img_tempfile_path = get_tempfile_path(image_path)
	img_tempfile = open(img_tempfile_path, 'w')
	img_tempfile.write(array)

	return array

def get_tempfile_path(image_path):
	tmp = '/tmp'
	filename = tmp + '/' + os.path.split(image_path)[1] + '.c4shtmp'
	return filename

def get_imagedata(image_path):
	try:
		if os.path.exists(get_tempfile_path(image_path)):
			imagedata_file = open(get_tempfile_path(image_path), 'r')
			return imagedata_file.read()
		else:
			return __image_creation(image_path)

	except Exception, e:
		return "somethings going wrong"
