from fastapi import FastAPI,Response
from pydantic import BaseModel


from Scraping import scraping
import os

from pymongo import MongoClient
from mongoengine import connect, Document, fields
from PIL import Image
import io

app=FastAPI()



class UpdateItem(BaseModel):
    name:str
# cet inventaire a été réalisé pour la verification des données qu'on doit passer 
# dans get(/informations)
# vu qu'on a une seule personne a scrappé
inventory={"nadal":"https://www.facebook.com/Nadal/"}

@app.get("/")
def home():
    return{"dans le post on doit passer le nom ":"nadal"}

# On affiche les informations de la personne si le nom est verifié ('nadal')
@app.get("/name")
def get_informations(name:str):
    if name=='nadal':
        client=MongoClient("mongodb://ramzi:ramzi@mongo:27017/Elyadata")
        db=client.Elyadata
        document=db.test_webscraping
        information=document.find_one()
        return{'nom':information['name']}
    return{'Error':"le facebook de cette personne n'a pas été scrappé"}

# On affiche l'image du site web qu'on scrapper selon le nombre de l'index de l'image qu'on veut pas
# On a limité le choix au 10 premieres images malgres qu'on a scrappé une quarantaine d'images
@app.get("/image")
def get_item(number:int):
    if number in range(10) :
        client=MongoClient("mongodb://ramzi:ramzi@mongo:27017/Elyadata")
        db=client.Elyadata
        customers=db.test_webscraping
        image=customers.find_one()
        index=str(number)
        return Response(content=image['photos'][index], media_type='image/jpeg')
    return {"Erreur":"Le nombre doit etre entre 0 et 9"}

# Ajouter un document qui contient les données de la page de la personne qu'on va scraper
# on realise une verification sur le nom de la personne qui est 'nadal'
@app.post("/create-item")
def create_item(name:str):
    all={}
    album={}
    if name not in inventory:
        return{"Error":"ce n'est pas la personne de notre exemple"}
    else:
        scraper=scraping()
        scraper.execute()
        client=MongoClient("mongodb://ramzi:ramzi@mongo:27017/Elyadata")
        db = client['Elyadata']
        my_col=db['test_webscraping']
        path = os.getcwd()
        path = os.path.join(path, "FB_SCRAPED")
        for i in range(0,10):
            adresse=os.path.join(path, str(i) + '.jpg')
            image1=Image.open(adresse)
            image_bytes = io.BytesIO()
            image1.save(image_bytes, format='JPEG')
            key=str(i)
            album[key]=image_bytes.getvalue()
            all['name']=scraper.name
            all['photos']=album
            
        
        x=my_col.insert_one(all).inserted_id

#Effacer toute le Document selon son nom pour notre cas on a une seule qui est celle de rafael nadal
@app.delete('/delete/name')
def delete_item(names:str):
    client=MongoClient("mongodb://ramzi:ramzi@mongo:27017/Elyadata")
    db=client.Elyadata
    customers=db.test_webscraping
    document=customers.find_one()
    if names == document['name']:
        db.test_webscraping.delete_one( {'name': names } )
        return{'Success':'le document a été effacer avec succès'}
    else:
        return{'Error':"le facebook de cette personne n'a pas été scrappé"}

# Update de le Document selon le nom et sur le nom de la personne
@app.put('/update-item/name')
def update_item(name:str,item:UpdateItem):
    client=MongoClient("mongodb://ramzi:ramzi@mongo:27017/Elyadata")
    db=client.Elyadata
    customers=db.test_webscraping
    document=customers.find_one()
    if name == document['name']:
        client.Elyadata.test_webscraping.update_one({ 'name':document['name']}, { '$set': {'name': item.name }})
        return{'Success':'Update fait avec succès'}
    else:
        return{'Error':'Un champ est vide ou faux nom'}

    