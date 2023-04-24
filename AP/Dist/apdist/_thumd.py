from pdf2image import convert_from_path
import os
try:
	os.mkdir('Thumbs')
except Exception:
	pass

files=os.listdir(os.getcwd())
for i in files:
	if (i[-3:]=='pdf'):
		img=i[:-4]
		pages = convert_from_path(i,20,first_page=1,last_page=1)
		for page in pages:
		    page.save('Thumbs/'+img+'-01_001'+'.jpg', 'JPEG')
		    print(img+'.jpg is saved')