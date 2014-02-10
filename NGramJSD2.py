# -*-coding:Latin-1 -*
import math

class NGramJSD2(object):
	def __init__(self, text, n=3):
		self.length = None
		self.n = n
		self.table = {}
		self.parse_text(text)
		self.calculate_length()

	def parse_text(self, text):
		chars = ' ' * self.n # initial sequence of spaces with length n

		for letter in (" ".join(text.split()) + " "):
			chars = chars[1:] + letter # append letter to sequence of length n
			self.table[chars] = self.table.get(chars, 0) + 1 # increment count

	def calculate_length(self):
		""" Treat the N-Gram table as a vector and return its scalar magnitude
		to be used for performing a vector-based search.
		"""
		self.length = sum([x * x for x in self.table.values()]) ** 0.5
		return self.length

	def histo_diff(self, other):
		grams = list(set(self.table.keys()) & set(other.table.keys()))
		K = len(self.table.keys()) - len(grams)
		return K

	def __sub__(self, other):
		if not isinstance(other, NGramJSD2):
			raise TypeError("Can't compare NGram with non-NGram object.")

		if self.n != other.n:
			raise TypeError("Can't compare NGramJSD objects of different size.")

		JSD = 0
		grams = list(set(self.table.keys()) & set(other.table.keys()))

		for k in grams:
			P = float(self.table.get(k, 0.0000001))
			Q = float(other.table.get(k, 0.0000001))
			#print P, " - ", Q
			JSD += P * math.log(2 * Q / (P + Q))
			JSD += Q * math.log(2 * P / (P + Q))

		return -JSD

	def find_match(self, languages):
		return min(languages, lambda n: self - n)
