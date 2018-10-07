from django.db import models
import psycopg2

# Create your models here.


def connect(name, address, zipcode):
      con = psycopg2.connect("dbname=cms user=postgres password=Blr560016")
      cur = con.cursor()
      print(name)
      print(address)
      print(zipcode)
      query = "insert into customer(customer_id, customer_name, customer_address, customer_phone) values (DEFAULT, %s, %s, %s)"
      cur.execute(query, (name, address, zipcode))
      con.commit()
      con.close()


      
      