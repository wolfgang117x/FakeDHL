from django.db import models
import psycopg2
import psycopg2.extras
import bcrypt
import random

# Create your models here.


class dbconnection():
      def connect(self):
            try:
                  self.con = psycopg2.connect("host=bdzm3eywimkxj1x3y5qv-postgresql.services.clever-cloud.com dbname=bdzm3eywimkxj1x3y5qv user=uthpua3wbyl5tmqd43x5 password=xJuNZNcLsTFnKI97m77O")
                  self.cur = self.con.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
                  print("connected")
            except (Exception, psycopg2.DatabaseError) as error:
                  print(cur)
                  print(error)

      def close(self):
            if self.con is not None:
                  self.con.close()
                  print("closed")
      
      def reguser(self, phone, name, address, city, state, password):
            try:
                  query = "INSERT INTO customer(customer_phone, customer_name, customer_address, customer_city, customer_state) values (%s, %s, %s, %s, %s)"
                  self.cur.execute(query, (phone, name, address, city, state))
                  print(password)
                  salt = bcrypt.gensalt()
                  password_hashed = bcrypt.hashpw(password.encode('utf8'), salt)
                  print(password_hashed)
                  query2 = "INSERT INTO pass(customer_phone, password) values (%s, %s)"
                  self.cur.execute(query2, (phone, password_hashed.decode('utf-8')))
                  return 1
            except psycopg2.IntegrityError:
                  print("Caught")
                  return 0
            except Exception:
                  print("Others Caught")
                  return 2

      def auth(self, phone, password):
            query = "SELECT password from pass where customer_phone= %s"
            self.cur.execute(query, (phone, ))
            rowdata = self.cur.fetchone()
            try:
                  passhash = rowdata.password
            except Exception:
                  return 2
            print(passhash)
            print(password)
            if bcrypt.checkpw(password.encode('utf-8'), passhash.encode('utf-8')):
                  return 0
            else:
                  return 1

      def table(self, uid):
            query = "SELECT * from customer where customer_phone=%s"
            self.cur.execute(query, (uid, ))
            data = self.cur.fetchone()
            print(data)
            return data

      def updateaddress(self, address, city, state, uid):
            try:
                  query = "UPDATE customer set customer_address = %s, customer_city = %s, customer_state = %s where customer_phone = %s"
                  self.cur.execute(query, (address, city, state, uid, )) 
                  return 1
            except Exception:
                  print("Others Caught")
                  return 0

      def addship(self, uid,  name, phone, address, city, state, contents, weight, volume):
            
            try:
                  query = "INSERT INTO recepient(recepient_phone, recepient_name, address, city, state) values (%s, %s, %s, %s, %s)"
                  self.cur.execute(query, (phone, name, address, city, state))
                  print("ok0")
                  query = "INSERT INTO package(package_id, package_contents, package_volume, package_price, package_weight) values (%s, %s, %s, getprice(%s), %s)"
                  id = random.randint(000000000,999999999)
                  self.cur.execute(query, (id, contents, volume, weight, weight))
                  print("ok1")
                  query = "INSERT INTO package_sender(package_id, customer_phone) values (%s, %s)"
                  self.cur.execute(query, (id, uid))
                  print("ok2")
                  query = "SELECT max(recepient_id) from recepient where recepient_phone=%s"
                  self.cur.execute(query, (phone, ))
                  print("ok3")
                  data = self.cur.fetchone()
                  print(data)
                  query = "INSERT INTO package_receiver(package_id, recepient_id) values (%s, %s)"
                  self.cur.execute(query, (id, data.max))
                  print("ok4")
                  query = "INSERT INTO shipping (package_id, shipping_status) values (%s, %s)"
                  self.cur.execute(query, (id, "Order Placed"))
                  print("ok5")
                  return id
            except psycopg2.IntegrityError:
                  print("Caught")
                  return 1
            except Exception:
                  print("Others Caught")
                  return 2

      def orderstable(self, uid):
            query = " SELECT p.package_id, p.package_contents, r.recepient_phone, r.address, r.city, r.state from package p, recepient r, package_sender ps, package_receiver pr, shipping s where ps.customer_phone = %s and ps.package_id = pr.package_id and ps.package_id = p.package_id and pr.recepient_id = r.recepient_id and p.package_id=s.package_id order by s.route_no"
            self.cur.execute(query, (uid, ))
            data = self.cur.fetchall()
            print(data)
            datadict = {dat.package_id: dat for dat in data}
            print(datadict)
            return datadict

      def updatepass(self, uid, newpass):
            try:
                  query = "UPDATE pass set password=%s where customer_phone=%s"
                  print(newpass)
                  salt = bcrypt.gensalt()
                  password_hashed = bcrypt.hashpw(newpass.encode('utf8'), salt)
                  print(password_hashed)
                  self.cur.execute(query, (password_hashed.decode('utf-8'), uid))
                  return 1
            except psycopg2.IntegrityError:
                  print("Caught")
                  return 0
            except Exception:
                  print("Others Caught")
                  return 2

      def tracktable(self, trackid):
            query = "SELECT route_no,date, shipping_status from shipping where package_id=%s"
            self.cur.execute(query, (trackid, ))
            data = self.cur.fetchall()
            print(data)
            datadict = {dat.route_no: dat for dat in data}
            print(datadict)
            return datadict

      def recepient_info(self, trackid):
            query = "SELECT r.recepient_id, r.recepient_name, r.recepient_phone, r.address, r.city, r.state, p.package_price from recepient r, package_receiver pr, package p where pr.package_id=%s and pr.recepient_id = r.recepient_id and pr.package_id=p.package_id"
            self.cur.execute(query, (trackid, ))
            data = self.cur.fetchone()
            return data

      def delacc(self, uid):
            try:
                  query = "DELETE from customer where customer_phone = %s"
                  self.cur.execute(query, (uid, ))
                  return 1
            except Exception:
                  print("Caught While Deleting")
                  print(Exception)
                  return 2
            
            
      def vieworders(self):
            query = "select p.package_id, s.date, c.customer_phone, c.customer_name, p.package_contents from package p, customer c, shipping s, package_sender ps where ps.package_id = p.package_id and p.package_id = s.package_id and ps.customer_phone=c.customer_phone"
            self.cur.execute(query)
            data = self.cur.fetchall()
            print(data)
            datadict = {dat.package_id: dat for dat in data}
            print(datadict)
            return datadict
      
      def viewusers(self):
            query = "SELECT c.customer_phone,c.customer_name,c.customer_address, c.customer_city, c.customer_state, count(*) as orders from customer c  left join package_sender on (package_sender.customer_phone = c.customer_phone) group by c.customer_phone"
            self.cur.execute(query)
            data = self.cur.fetchall()
            print(data)
            datadict = {dat.customer_phone: dat for dat in data}
            print(datadict)
            return datadict

      def updatestatus(self, trackid, status):
            try:
                  query = "INSERT into shipping (package_id, shipping_status) values (%s, %s)"
                  self.cur.execute(query, (trackid, status )) 
                  return 1
            except Exception:
                  print("Others Caught")
                  return 0

      def getprice(self, trackid):
            try:
                  query = "SELECT package_price from package where package_id = %s"
                  self.cur.execute(query, (trackid, ))
                  price = self.cur.fetchone()
                  print(price.package_price)
                  return price.package_price

            except Exception:
                  print("Price Exception Caught")
                  print(Exception)
                  return 0
            


