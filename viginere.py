import itertools

alphabet = list('abcdefghijklmnopqrstuvwxyz')
table = {alphabet[x]:zip(alphabet, alphabet[x:]+alphabet[:x]) for x in range(len(alphabet))}
class ViginereTable:
	table = {key:(dict(table[key]),{v:k for k,v in table[key]}) for key in table}

	def __getitem__(self, key):
		if len(key) == 2:
			cipher, plain = key
			return self.table[cipher][plain]
		else:
			return self.table[key]

	def encode(self, key, plaintext):
		out = []
		for keychar, msgchar in zip(itertools.cycle(key), plaintext):
			enc, _ = self[keychar]
			out.append(enc[msgchar])
		return ''.join(out)

	def decode(self, key, ciphertext):
		out = []
		for keychar, cipherchar in zip(itertools.cycle(key), ciphertext):
			_, dec = self[keychar]
			out.append(dec[cipherchar])
		return ''.join(out)

class RandViginere(object):
	def __init__(self):
		self.table = ViginereTable()
		self.source = open('/dev/urandom')
	def __del__(self):
		self.source.close()

	def encode(self, text):
		text = [text[a*10:(a+1)*10] for a in range((len(text)/10)+1)]
		keys = []
		result = []
		for chunk in text:
			key = [alphabet[int((ord(k)/256.0)*26)] for k in self.source.read(len(chunk))]
			result.append(self.table.encode(key, chunk))
			keys.append(key)
		return ''.join(''.join(key) for key in keys), ''.join(result)

	def decode(self, key, text):
		return self.table.decode(key, text)

if __name__ == '__main__':
	import argparse
	import json
	import sys

	parser = argparse.ArgumentParser()
	parser.add_argument('--decode', '-d', default=False, action='store_true')
	options = parser.parse_args()

	a=RandViginere()

	for line in sys.stdin:
		if options.decode:
			encoded = json.loads(line)
			key, text = encoded['key'], encoded['encoded']
			print a.decode(key, text)
		else:
			key, text = a.encode(''.join(c.lower() for c in line if c.isalpha()))
			print json.dumps(dict(key=key, encoded=text))

