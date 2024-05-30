from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllCountry():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct(gr.Country) from go_retailers gr """
        cursor.execute(query)
        for row in cursor:
            result.append((row["Country"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRetailers(country):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select * from go_retailers gr 
                    where gr.Country = %s"""
        cursor.execute(query,(country,))
        for row in cursor:
            result.append((Retailer(**row)))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPesi(c1,c2,year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select count(DISTINCT gds.Product_number) as c from go_daily_sales gds, go_daily_sales gds2 
                    where gds2.Retailer_code = %s and gds.Retailer_code =%s
                    and gds2.Product_number = gds.Product_number
                    and YEAR(gds2.`Date`) = %s and YEAR(gds.`Date`) = %s
                    """
        cursor.execute(query, (c2,c1,year,year))
        for row in cursor:
            result.append(row["c"])
        cursor.close()
        conn.close()
        return result
