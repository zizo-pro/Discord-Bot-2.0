def read_token():
		with open("token.txt","r") as f:
				token = f.readline()
				return token