import Image
import math
try: import numpypy
except ImportError: pass
import numpy

a = img = Image.open('church.png')
b = numpy.asarray(a)



def rgb2gray(rgb):
	r, g, b = numpy.rollaxis(rgb[...,:3], axis = -1)
	return 0.299 * r + 0.587 * g + 0.114 * b

def get_ring(img, rad):
	x,y = img.shape
	yscale = float(x)/y
	xx,yy = numpy.mgrid[:x,:y]
	rectangle = numpy.logical_or( abs(x/2-xx) > rad, abs(y/2-(yy))*yscale > rad)
	out = numpy.ma.masked_array(img, mask=rectangle, fill_value=0)
	return out.filled(0)


def save_close(img, fn):
	with open(fn, 'w') as f:
		img.save(f)
		f.flush()


d = rgb2gray(b)
save_close(Image.fromarray(d).convert('L'), 'church_g.png')

d_fft = numpy.fft.fft2(d)
d_r = d_fft.real
d_i = d_fft.imag
save_close(Image.fromarray(d_r).convert('L'), 'church_gr.png')
save_close(Image.fromarray(d_i).convert('L'), 'church_gi.png')

rad = 0
i_r = get_ring(d_r, rad)
count = 3
out_r = numpy.zeros(a.size[::-1])
out_i = numpy.zeros(a.size[::-1])
x,y = a.size


def normalize(arr):
	"""
	Linear normalization
	http://en.wikipedia.org/wiki/Normalization_%28image_processing%29
	"""
	arr = arr.astype('float')
	# Do not touch the alpha channel
	minval = arr.min()
	maxval = arr.max()
	if minval != maxval:
			arr -= minval
			arr *= (255.0/(maxval-minval))
	return arr


while rad < x/2:
	print count, rad
	i_r = get_ring(d_r, rad)
	print i_r.shape, out_r.shape
	i_i = get_ring(d_i, rad)
	print i_i.shape, out_i.shape
	rad += 1

	save_close(Image.fromarray(i_r).convert('L'), 'church_r%03d.png' %(rad))
	save_close(Image.fromarray(i_i).convert('L'), 'church_i%03d.png' %(rad))
	img = abs(numpy.fft.ifft2(i_r + i_i*1j))
	img = normalize(img)
	save_close(Image.fromarray(img).convert('L'), 'church_c%03d.png' %(rad))

