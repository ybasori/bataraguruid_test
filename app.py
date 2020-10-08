from flask import Flask, request
import pymongo
import time

client=pymongo.MongoClient()
mydb=client["mydb"]

app = Flask(__name__)

@app.route("/")
def home():
    if request.headers.get("x-api-key") is None:
        return "API KEY is required."

    else:
        if request.headers.get("x-api-key")!="123":
            return "Access Denied"

        else:
            mycol=mydb["log"]
            x=mycol.find_one({"apiKey":request.headers.get("x-api-key")})

            if x is None:
                data={"apiKey":request.headers.get("x-api-key"), "createdAt": time.time(), "requestTotal": 1}
                mycol.insert_one(data)

                return "Hello World"

            else:
                if time.time()-x["createdAt"] < 60 and x["requestTotal"] < 5:
                    myquery = { "apiKey": request.headers.get("x-api-key") }
                    newvalues = { "$set": { "createdAt": time.time(), "requestTotal": x["requestTotal"]+1 } }
                    mycol.update_one(myquery, newvalues)

                    return "Hello World"

                elif time.time()-x["createdAt"] >= 60:
                    myquery = { "apiKey": request.headers.get("x-api-key") }
                    newvalues = { "$set": { "createdAt": time.time(), "requestTotal": 1 } }
                    mycol.update_one(myquery, newvalues)

                    return "Hello World"
                
                else:
                    return "Limited request"

app.run(debug=True)
