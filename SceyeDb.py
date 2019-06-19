import pymysql
import os
import json

def main(arg1):
    #Putting argument with all the json files into a variable
    json_files = []
    json_files = arg1


    # connect to MySQL with the right SSL filepath
    con = pymysql.connect(host = '127.0.0.1',user = 'mellumsu',passwd = 'root',db = 'osintdb', ssl={'ssl' : {'ca': '/etc/mysql/certs/ca.pem'}})
    cursor = con.cursor()

    #A loop for all the json files
    for x in json_files:
        file = os.path.abspath(x)
        json_data=open(file).read().replace("null", "\"\"")
        json_obj = json.loads(json_data)

        # parse json data to SQL insert
        for i, item in enumerate(json_obj):
            print("date_time:", item["date_time"])
            print("uid:", item["uid"])
            print("land_code:", item["land_code"])
            print("company_registration_no", item["company_registration_no"])
            print("postal_code:", item["postal_code"])
            print("company_name:", item["company_name"])
            print("address:", item["address"])
            print("location:", item["location"])
            print("url:", item["url"])

            cursor.execute("INSERT INTO Company (UUIDCompany, Name, LandCode, ChamberOfCommerce, ScrapeDate, Source) VALUES (%s,%s,%s,%s,%s,%s)", (item["uid"], item["company_name"], item["land_code"], item["company_registration_no"], item["date_time"], item["url"]))
            
    con.commit()
    con.close()
    
    print("\nData has been stored into the database.")

if __name__ == "__main__":
    main(sys.argv[1])
