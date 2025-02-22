from flask import Flask, jsonify, request
import psycopg2
from psycopg2 import sql
import json
from flask_paginate import Pagination
app = Flask(__name__)
@app.route('/')
def first_app():
    return "Hi this is dhakshesh"

DB_HOST = 'localhost'
DB_NAME = 'user_management_db'
DB_USER = 'postgres'
DB_PASSWORD = 'Dhaksheshhpe7'

# The JSON FILE is uploaded to the Postgres SQL

@app.route('/api/users', methods=['POST'])
def upload_json():
    file = request.files['file']
    try:
        data=json.load(file)
        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        cursor = connection.cursor()
        for record in data:
            cursor.execute("""Insert into users (id,first_name, last_name, company_name, city, state, zip, email, web, age) 
                           values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning first_name, last_name, company_name, city, state, zip, email, web, age
                           """,(record['id'],record['first_name'],record['last_name'],record['company_name'],record['city'],
                                record['state'],record['zip'],record['email'],record['web'],record['age']))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"Message":"Data uploaded successfully"}),200
    except Exception as e:
        return jsonify({"error":str(e)}),500

#Returns all the data from the Database
@app.route('/api/users',methods=['GET'])
def page_limit_search_sort():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        page_num=int(request.args.get('page'))
        limit_data=int(request.args.get('limit'))
        search=request.args.get('search')
        sort=request.args.get('sort')
        cursor.execute("Select * from users order by id asc")        
        user_data=cursor.fetchall()
        
        user_list=[]
        for user in user_data:
            user_list.append({
                "id": user[0],
                "first_name": user[1],
                "last_name": user[2],
                "company_name":user[3],
                "city": user[4],
                "state": user[5],
                "zip": user[6],
                "email": user[7],
                "web": user[8],
                "age": user[9]
            })
        cursor.close()
        connection.close()
        start=(page_num-1)*limit_data
        end=start+limit_data
        paginate_output = user_list[start:end]

        if (search and sort) or search:
            search = search.lower()
            for index in range(start,end):
                if search in paginate_output[index]['first_name'].lower() or search in paginate_output[index]['last_name'].lower():
                    return jsonify({
                        "Searching found ": paginate_output[index] 
                    })
        if sort:
            if sort=="-age" or sort=="-id":
                paginate_output = sorted(paginate_output,key=lambda x:x[sort[1:]],reverse=True)
            else:
                paginate_output = sorted(paginate_output,key=lambda x:x[sort])
        return jsonify({
            "page":page_num,
            "Per_page":limit_data,
            "total":len(user_list),
            "Users":paginate_output
        }),200
    except Exception as e:
        return jsonify("error:",str(e)),500

#It gives the details of the specified ID
@app.route('/api/users/<int:id>',methods=['GET'])
def get_user_details(id):
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        cursor.execute("select * from users where id =%s",(id,))
        user=cursor.fetchone()
        if not user:
            return jsonify({"message": "No users found"}), 404
        user_list = []
        user_list.append({
            "id": user[0],
            "first_name": user[1],
            "last_name": user[2],
            "company_name":user[3],
            "city": user[4],
            "state": user[5],
            "zip": user[6],
            "email": user[7],
            "web": user[8],
            "age": user[9]
        })
        cursor.close()
        connection.close()
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({"error":str(e)}),500

#Updating the entire row with the specified ID
@app.route('/api/users/<int:id>', methods=['PUT'])
def get_user_from_id(id):
    user_data = request.get_json()
    first_name = user_data.get('first_name')
    last_name = user_data.get('last_name')
    company_name = user_data.get('company_name')
    city = user_data.get('city')
    state = user_data.get('state')
    zip = user_data.get('zip')
    email = user_data.get('email')
    web = user_data.get('web')
    age = user_data.get('age')
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()

        cursor.execute("""
                    UPDATE users set first_name = %s,last_name = %s,company_name = %s,city =%s,state = %s,zip= %s,email= %s,web = %s, 
                       age = %s where id = %s
                        returning first_name, last_name, company_name,city, state, zip, email,web, age,id;""", (
                            first_name, last_name, company_name,city, state, zip, email,web, age,id))
        connection.commit()
        user_data=cursor.fetchone()
        cursor.close()
        connection.close()
        return jsonify({
            "message": "User updated success",
        }), 201
    except Exception as e:
        return jsonify({"error":str(e)}),500

#Deleting the User with their ID
@app.route('/api/users/<int:id>',methods=['DELETE'])
def delete_user_details(id):
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE id =%s;",(id,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message":"User deleted successfully"}),200
    except Exception as e:
        return jsonify({"error":str(e)}),500

#Partially updating the data
@app.route('/api/users/<int:id>',methods=['PATCH'])
def update_user_partial(id):
    user_data=request.get_json()
    email = user_data.get('email')
    age = user_data.get('age')
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor=connection.cursor()
        cursor.execute("""
            UPDATE users set email =%s,age=%s where id =%s returning email,age;
                    """,(email,age,id))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message":"Updation success"})
    except Exception as e:
        return jsonify({"error":str(e)}),500

#It give the summary of Database
@app.route('/api/users/summary',methods=['GET'])
def user_summary():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor=connection.cursor()
        cursor.execute("SELECT count(*),avg(age) from users;")
        count_users,average_age=cursor.fetchone()
        cursor.execute("Select city, count(*) from users group by city;")
        users_city={
            city:count for city, count in cursor.fetchall()
        }
        connection.close()
        return jsonify({
            "total_users":count_users,
            "avaerge_age":round(average_age,2),
            "users_for_each_city":users_city
        }),200
    except Exception as e:
        return jsonify({"error":str(e)}),500

if __name__=="__main__":
    app.run(debug=True)