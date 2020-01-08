#Autor: Keith Sasaki

import json
import requests
import re

#classe Post para armazenar os dados de cada post

class Post:

	def __init__(self, media, post_id, title, product_id, price, date, likes):
		self.media = media
		self.post_id = post_id
		self.title = title
		self.product_id = product_id 
		self.price = price
		self.date = date
		self.likes = likes
	
	def getMedia(self):
		return self.media	

	def getPost_id(self):
		return self.post_id

	def getTitle(self):
		return self.title

	def getProduct_id(self):
		return self.product_id

	def getPrice(self):
		return self.price

	def getDate(self):
		return self.date

	def getLikes(self):
		return self.likes

#funcao que armazena os dados obtidos pela requisicao get em um vetor de posts
def get_data(url): 
	r_get = requests.get(url)

	parsed_json = r_get.json();
	posts = parsed_json['posts']
	
	vet_posts = []
	
	for p in posts:
		media = p.get('media')
		post_id = p.get('post_id')
		title = p.get('title')
		product_id = p.get('product_id')
		price = p.get('price')
		date = p.get('date')
		likes = p.get('likes')
		new_post = Post(media, post_id, title, product_id, price, date, likes)
		vet_posts.append(new_post)

	return vet_posts


# exercicio a: funcao que retorna um vetor ordenado de acordo com as especificacoes, com os posts que contem a 
# palavra promocao no titulo 
def ex_A(vet_posts):
	vet_A = []

	for p in vet_posts:

		if re.search("promocao", p.getTitle()):

			for i in range (len(vet_A)):
				if(p.getPrice() < vet_A[i].getPrice()):
					vet_A.insert(i, p)
					break

				elif (p.getPrice() == vet_A[i].getPrice()):
					if(p.getProduct_id() != vet_A[i].getProduct_id()):
						j = i;

						while((p.getPrice() == vet_A[j].getPrice()) and 
							  (p.getProduct_id() > vet_A[j].getProduct_id())):
							j += 1

							if(j >= len(vet_A)):
								vet_A.append(p)
								break;

						vet_A.insert(j, p)
						break
					else:
						break
			else:
				vet_A.append(p)

	return vet_A

# exericio b: Funcao que retorna um vetor ordenado de acordo com as especificacoes com os posts da 
# midia instagram com o numero de likes acima de 700
def ex_B(vet_posts):
	vet_B = []

	for p in vet_posts:
		if ((p.getMedia() == "instagram_cpc") and (p.getLikes() > 700)):
			for i in range (len(vet_B)):
				if(p.getPrice() < vet_B[i].getPrice()):
					vet_B.insert(i, p)
					break
					
				elif (p.getPrice() == vet_B[i].getPrice()):
					if(p.getPost_id() != vet_B[i].getPost_id()):
						j = i;

						while((p.getPrice() == vet_B[j].getPrice()) and 
							  (p.getPost_id() > vet_B[j].getPost_id())):
							j += 1

							if(j >= len(vet_A)):
								vet_B.append(p)
								break;

						vet_B.insert(j, p)
						break
					else:
						break

			else:
				vet_B.append(p)
	return vet_B

#exercicio c: funcao que retorna o somatorio de likes no mes de maio de 2019 para todas as midias pagas
def ex_C(vet_posts):
	sum_likes = 0
	for p in vet_posts:
		if ((p.getMedia() == "google_cpc") or (p.getMedia() == "facebook_cpc") or (p.getMedia() == "instagram_cpc")):
			if(re.search("05/2019", p.getDate())):
				sum_likes += p.getLikes()

	return sum_likes


#exercicio d: funcao que retorna um vetor com os ids dos produtos que estao inconsistentes
def ex_D(url):
	r_get = requests.get(url)

	parsed_json_d = r_get.json();
	
	posts = parsed_json_d['posts']

	vet_posts_d = []
	vet_error = []
	
	for p in posts:

		product_id = p.get('product_id')
		price = p.get('price')
		new_post = Post("", "", "", product_id, price, "", 0)

		vet_posts_d.append(new_post)

		for i in range (len(vet_posts_d)):

			if((product_id == vet_posts_d[i].getProduct_id()) and 
			  (price != vet_posts_d[i].getPrice())):

				if(product_id not in vet_error):
					for j in range(len(vet_error)):
							if (product_id < vet_error[j]):
								vet_error.insert(j,product_id)
								break
					else:
						vet_error.append(product_id)

	return vet_error

#funcao que junta todos os valores necessarios para formar a string de resposta
def resposta(vet_A, vet_B, C, vet_D):

	str_A = ""
	i = 0
	for a in vet_A:
		i += 1
		if(i == len(vet_A)):
			str_A += '{"product_id": ' + '"' + a.getProduct_id() + '",' + '"price_field": ' + str(a.getPrice()) + '}'
		else:
			str_A += '{"product_id": ' + '"' + a.getProduct_id() + '",' + '"price_field": ' + str(a.getPrice()) + '},'

	str_B = ""
	i = 0
	for b in vet_B:
		i += 1
		if(i == len(vet_B)):
			str_B += '{"post_id": ' + '"' + b.getPost_id() + '",' + '"price_field": ' + str(b.getPrice()) + '}'
		else:
			str_B += '{"post_id": ' + '"' + b.getPost_id() + '",' + '"price_field": ' + str(b.getPrice()) + '},'

	str_D = ""
	i = 0
	for d in vet_D:
		i += 1
		if(i == len(vet_D)):
			str_D += '"' + d + '"'
		else:
			str_D += '"' + d + '",'



	aux_A = "{ \"full_name\": \"Keith Tsukada Sasaki\", \"email\": \"keith.sasaki5@gmail.com\", \"code_link\": \"https://github.com/keithsasaki/psel-racoonn\"," + "\"response_a\": [" + str_A + "],"
	aux_B = "\"response_b\": [" + str_B + "],"
	aux_C = "\"response_c\":" + str(C) + ","
	aux_D = "\"response_d\": ["+ str_D + "] }"


	json_string = aux_A + aux_B + aux_C + aux_D

	return json_string


#funcao principal
def main():
	url_get = 'https://us-central1-psel-clt-ti-junho-2019.cloudfunctions.net/psel_2019_get'
	url_get_d = 'https://us-central1-psel-clt-ti-junho-2019.cloudfunctions.net/psel_2019_get_error'
	url_post = 'https://us-central1-psel-clt-ti-junho-2019.cloudfunctions.net/psel_2019_post'

	vet_posts = get_data(url_get)
	vet_A = ex_A(vet_posts)
	vet_B = ex_B(vet_posts)
	C = ex_C(vet_posts)
	vet_D = ex_D(url_get_d)

	resp = resposta(vet_A, vet_B, C, vet_D)

	headers = {'content-type': 'application/json'}

	r = requests.post(url_post,  data = resp, headers = headers)

if __name__ == "__main__":
    main()