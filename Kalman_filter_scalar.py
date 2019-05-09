import numpy as num

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
		self.P = P
		self.Ppost = P
		self.x = x
		self.xpost = x

	def get_data(self, acc_data, gyro_data):

		'''

		Metoda będąca algorytmem wykonawczym filtru kalmana. 
		Jako argumenty przyjmuje "acc_data" - prędkość kątową z akacelrometru oraz "gyro_data" - prędkość kątową.
		Metoda zwraca wartość "x", któa jest kątem odchylenia po filtracji kalmana.
		Wartość atrybutów "x" i "P" jest w trakcie algorytmu nadpisywana i wykorzystywana w kolejnych iteracjach.

		Argumenty i zwracane wartości wyjaśnione są dla przypadku mierzenia kąta odchylenia.
		Filtr działa analogicznie dla innych wielkości po odpowiednim zaiinicjowaniu obiektu i przy podaniu odpowiednich wartości mierzonych do metody.


		'''
	

		#faza predykcji

		self.x=self.A*self.x + B*gyro_data
		self.P=self.A*self.P*self.A + self.Q
		#faza korekcji
		
		eps = acc_data - self.C*self.x
		S = self.C*self.P*self.C + self.W
		K = self.P*self.C/S
		self.x = self.x + K*eps
		self.P = self.P - K*S*K

		return self.x

	def test(self):
		pass

if __name__ == '__main__':

	#inicjalizacja modelu stanu procesu

	dt = 0.1
	A= 1
	B= dt
	C=1

	std_v = 1

	Q= std_v*std_v*dt
	W= std_v*std_v*dt

	x0=0
	P0=1

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
	#for nums in range(0,len(gyroz)):
	#	print(f"{gyroz[nums]}   {acc[nums]}")
	

	for nums in range(0, len(gyroz)):
		tmp = kalman.get_data(acc[nums], gyroz[nums])
		angle.append(tmp)

	for nums in range(0,len(angle)):
		print(f"{angle[nums]}     {acc[nums]}")

	
	


