"""
module for encrypting and decrypting files


"""
import math
import hashlib
import rabimiller
import random
import shelve
import pickle
import hashlib
import os

BLOCK_SIZE=128
BYTE_SIZE=256

def addList(list):
	"""
	sum a list of integers and return the sum list
	argument is a list
	"""
	sum=0
	i=0
	while i < len(list):
		sum+=list[i]
		i +=1
	return sum
	
def gcd(a,b):
	"""
	find and return the greatest common divisor of two numbers a and a,b passed as args
	"""
	while a !=0:
		a,b=b%a,a
	return b


def  findModInverse(a,  m):
	""" 
	find and return the modinverse of two numbers a,m that are relative prime
	"""
	if  gcd(a,  m)  !=  1:
		 return  None  #  no  mod  inverse  exists  if  a  &  m  aren't  relatively  prime 
	u1,  u2,  u3  =  1,  0,  a 
	v1,  v2,  v3  =  0,  1,  m 
	while  v3  !=  0: 
		q  =  u3  //  v3  #  //  is  the  integer  division  operator 
		v1,  v2,  v3,  u1,  u2,  u3  =  (u1  -  q  *  v1),  (u2  -  q  *  v2),  (u3  -  q  *  v3), v1,  v2,  v3 
	return  u1  %  m 

def data_to_block(data,bytesize=256,blocksize=128):
	""" 
	Convert bytes of data to block by multiplying with the bytesize and mod of blocksize. Args list of data,bytesize and blocksize retun a dict of the blockdata and the length of the data list
	"""
	datalength=len(data)
	blockobj={}
	blockData=[ ]
	for blockstart in range(0,len(data),blocksize):
		blockInt=0
		for i in range(blockstart,min(blockstart+blocksize,len(data))):
			blockInt +=data[i]*(bytesize**(i%blocksize))
		blockData.append(blockInt)
	blockobj={'length':datalength,'data':blockData}
	return blockobj
	

def block_to_data(blockobj,bytesize=256,blocksize=128):
	""" 
	Convert block of data to list of data. Args  a dict of the blockdata and the length of the data list. Return a list of data
	"""
	lenD=blockobj["length"]
	datam=blockobj["block"]
	blockdata=[]
	for d in datam:
		data=[ ]
		for i in range(blocksize-1,-1,-1):
			if len(blockdata)+i  < lenD:
				byt=d//(bytesize**i)
				d=d%(bytesize**i)
				data.insert(0,byt)
		blockdata.extend(data)
	return blockdata
	
def generateKey(blocksize=1024):
	"""
	Generate keys for encryprion usig the RSA algorithim,args blocksize. Return a tuple of keys
	"""
	keyZ=blocksize
	p=rabimiller.generateLargePrime()
	q=rabimiller.generateLargePrime()
	n=p*q
	while True:
		e=random.randrange(2**(blocksize-1),2**(blocksize))
		if gcd(e,(p-1)*(q-1))==1:
			break
	d=findModInverse(e,(p-1)*(q-1))
	key=(e,d,n)
	return key
	
def encrypt(filepath,pwd):
	"""
	encrypt data using the RSA algorithim. Args bytes of data to be encrypted,filepath and password return a dictionary of encrypted data,keys,filetype
	"""
	try:
		file=open(filepath,"rb")
		data=file.read()
		pwd=hashlib.sha224(bytes(pwd,"utf-8")).hexdigest()
		dname=os.path.dirname(filepath)
		nf=os.path.basename(filepath).split(".")
		fnme=nf[0]
		ftype=nf[len(nf)-1]
		key= generateKey(blocksize=1024)
		e,d,n=key
		block=data_to_block(data)
		lent=block["length"]
		bloc=block["data"]
		encryptedblock=[]
		for b in bloc:
			encryptedblock.append(pow(b,e,n))
		dataobj={"pwd":pwd,"ftype":ftype,"length":lent,"data":encryptedblock,"d":d,"n":n}
		outfile=open(dname+"/"+nf[0]+".dat","wb")
		pickle.dump(dataobj,outfile)
		outfile.close()
		return " Encryption Successfull"
	except Exception as Exc:
		return Exc
	
	
	

def decrypt(filepath,pwd,blocksize=128):
		"""
		decrypt data args dictionary of encrypted data and keys. Return decrypted data
		"""
		pwdq=pwd
		pwd1=hashlib.sha224(bytes(pwdq,"utf-8")).hexdigest()
		
		try:
			infile=open(filepath,"rb")
			filedata=pickle.load(infile)
			if filedata["pwd"]==pwd1:
				decryptblock=[ ]
				ftype=filedata["ftype"]
				length=filedata["length"]
				blockdata=filedata["data"]
				d=filedata["d"]
				n=filedata["n"]
				for data in blockdata:
					decryptblock.append(pow(data,d,n))
				blockobj={"length":length,"block":decryptblock}
				data= block_to_data(blockobj)
				dname=os.path.dirname(filepath)
				fname=os.path.basename(filepath).split(".")
				file=open(dname+"/"+fname[0]+"."+ftype,"wb")
				file.write(bytes(data))
				return "Decryption Successfull"
			else:
				return "Invalid Password"
		except Exception as Exc:
			return Exc

		

			
		
	

	