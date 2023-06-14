from pyspark import SparkContext
from pyspark.mllib.recommendation import MatrixFactorizationModel
import redis
from pprint import pprint
pool=redis.ConnectionPool(host='192.168.10.10',port=6379)
redis_client= redis.Redis(connection_pool=pool)

# def redisOp():
#     redis_client.set(1,'bob')
#     print(redis_client.get(1))

def getRecommendByUseriID(userid,rec_num):
    sc=SparkContext(master="local[*]",appName='book_recommend')
    try:
        model = MatrixFactorizationModel.load(sc,"file:///root/bbb")
        result=model.recommendProducts(userid,rec_num)
        pprint(result)
        temp=''
        for r in result:
             temp +=str(r[0])+','+str(r[1])+','+str(r[2])+'|'
        # print(temp)
        print("load model success!!!")
    except Exception as e:
        print("load model failed"+str(e))
    sc.stop()
# if __name__ == '__main__':
#     getRecommendByUseriID(1,4)
