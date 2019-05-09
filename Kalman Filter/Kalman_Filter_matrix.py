import numpy as num
import matplotlib.pyplot as plt

class KalmanFilter():

	'''

	Obiekt tworzony jako instancja tej klasy jest filtrem kalmana dla dowolnej wielkości nieliniowej.


	'''

	def __init__(self, A, B, C, Q, W, P, x):

		'''
		Inicjalizacja macierzy stanu procesu
		A-macierz przejścia
		B-macierz wejścia
		C-macierz wyjścia
		Q-macierz kowariancji szumu procesu
		W-macierz kowariancji szumu pomiaru
		P-macierz stanu szumu procesu
		x-macierz stanu układu

		'''
		self.A = A
		self.B = B
		self.C = C
		self.Q = Q
		self.W = W
		self.Ppri = P
		self.Ppost = P
		self.xpri = x
		self.xpost = x
		self.index = 0

	def get_data(self, acc_data, gyro_data):

		'''

		Metoda będąca algorytmem wykonawczym filtru kalmana. 
		Jako argumenty przyjmuje "acc_data" - prędkość kątową z akacelrometru oraz "gyro_data" - prędkość kątową.
		Metoda zwraca wartość "x", któa jest kątem odchylenia po filtracji kalmana.
		Wartość atrybutów "x" i "P" jest w trakcie algorytmu nadpisywana i wykorzystywana w kolejnych iteracjach.

		Argumenty i zwracane wartości wyjaśnione są dla przypadku mierzenia kąta odchylenia.
		Filtr działa analogicznie dla innych wielkości po odpowiednim zaiinicjowaniu obiektu i przy podaniu odpowiednich wartości mierzonych do metody.


		'''
		w=num.array([[gyro_data]])
		#print(w)
		Y=num.array([[acc_data]])
		if self.index == 0:
			self.xpost = num.array([[acc_data],[0]])
			self.xpri = self.xpost
			self.index=self.index+1
		else:

			#faza predykcji
			Ax= num.matmul(self.A, self.xpost)
			Bw = self.B*gyro_data
			self.xpri= Ax + Bw
			#print(self.xpri)

			AP= num.matmul(self.A, self.Ppost)
			AT=self.A.transpose()
			APAT=num.matmul(AP, AT)
			self.Ppri = APAT + self.Q
			#print(self.Ppri)

			#faza korekcji
			# eps i S to macierze pomocnicze
			# K to macierz wzmocnienia kalmana

			Cx = num.matmul(self.C, self.xpri)
			eps = Y-Cx
			#print(eps)

			CP= num.matmul(self.C, self.Ppri)
			CT= self.C.transpose()
			CPCT = num.matmul(CP,CT)
			S = CPCT + self.W
			#print(S)

			PCT=num.matmul(self.Ppri, CT)
			K=PCT/S
			#print(K)

			Keps = num.matmul(K,eps)
			self.xpost = self.xpri + Keps
			#print(self.xpost)

			KT=K.transpose()
			KSKT = num.matmul(K*S, KT)
			self.Ppost = self.Ppri - KSKT
			#print(self.Ppost)
			#print("\n")
		return self.xpri

	def test(self):
		pass

if __name__ == '__main__':

	#inicjalizacja modelu stanu procesu

	dt = 0.1
	A= num.array([[1, -dt], [0,1]])
	B= num.array([[dt],[0]])
	C=num.array([[1,0]])

	std_v = 1
	std_w = 2

	Q=num.array([[std_v*std_v*dt, 0],[0, std_v*std_v*dt]])
	W=num.array([std_w*std_w])

	x0=num.array([[0],[0]])
	P0=num.array([[1,0],[0,1]])

	kalman = KalmanFilter(A,B,C,Q,W,P0,x0)

	gyroz = []
	acc = []

	with open("data.txt", "r") as f:
		data = f.readlines()
		for index,line in enumerate(data):
			if index==0:
				continue
			words=line.split()
			gyroz.append(float(words[2])*250/32768)
			x=float(words[3])*4/65535
			y=float(words[4])*4/65535
			acc.append(num.arctan(x/y)*180/num.pi)
	angle = []
	for nums in range(0, len(gyroz)):
		tmp = kalman.get_data(acc[nums], gyroz[nums])
		angle.append(tmp[0][0])

	for nums in range(0,len(angle)):
		print(f"{angle[nums]}     {acc[nums]}")

