import pymysql
import os
import json



# do validation and checks before insert
def validate_string(val):
   if val != None:
        if type(val) is int:
            #for x in val:
            #   print(x)
            return str(val).encode('utf-8')
        else:
            return val

def main(arg1):
    #Putting argument with all the json files into a variable
    json_files = []
    json_files = arg1


    # connect to MySQL with the right SSL filepath
    con = pymysql.connect(host = '127.0.0.1',user = 'mellumsu',passwd = 'root',db = 'NHTCU', ssl={'ssl' : {'ca': '/etc/mysql/certs/ca.pem'}})
    cursor = con.cursor()

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    cursor.execute("TRUNCATE `NHTCU` . `Company`")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    #A loop for all the json files
    for x in json_files:
        file = os.path.abspath(x)
        json_data=open(file).read().replace("null", "\"\"")
#        json_string=json.dumps(json_data).replace("null", " ")
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




            # cursor.execute("INSERT INTO CYR_testings (CYR_Address, CYR_Location, CYR_Company, CYR_PostalCode) VALUES (%s,%s,%s,%s)", (item["address"], item["location"], item["company_name"], item["postal_code"]))
            cursor.execute("INSERT INTO Company (ID, UUIDCompany, Name, LandCode, ChamberOfCommerce, FoundedIn) VALUES (%s,%s,%s,%s,%s,%s)", ("0", item["uid"], item["company_name"], item["land_code"], item["company_registration_no"], "2019-02-02"))
    con.commit()
    con.close()

if __name__ == "__main__":
    main(sys.argv[1])
