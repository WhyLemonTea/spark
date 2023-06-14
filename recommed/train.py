from pyspark.mllib.recommendation import ALS
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pprint import pprint
if __name__ == '__main__':
    spark=SparkSession.builder.getOrCreate()
    sc=spark.sparkContext

    rdd1=sc.textFile("hdfs:///book/movie.txt")
    ratingRDD=rdd1.map(lambda x:x.split('\t'))
    print(ratingRDD.take(3))

    user_row=ratingRDD.map(lambda x:Row(userid=int(x[0]),bookid=int(x[1]),hitnum=int(x[2])))

    user_df=spark.createDataFrame(user_row)
    user_df.printSchema()
    user_df.show()

    user_df.createOrReplaceTempView('test')
    datatable=spark.sql("""
    select userid,bookid, sum(hitnum) as hitnum from test group by userid , bookid
    """)
    datatable.show()

    bookrdd=datatable.rdd.map(lambda x:(x.userid,x.bookid,x.hitnum))
    print(bookrdd.take(3))

    #训练数据，特征集数量，迭代次数，正则因子
    model=ALS.trainImplicit(bookrdd,10,10,0.01)
    print(model)

    #测试
    # pprint(model.recommendProducts(169, 5))

    #保存
    #删除存在的目录
    import shutil
    import os

    if os.path.exists('/root/bbb'):
        shutil.rmtree('/root/bbb')
    model.save(sc,'file:///root/bbb')