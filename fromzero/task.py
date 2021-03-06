import datetime
import peewee
from peewee import *

db_name = 'ecity0606'
# Connect to a MySQL database on network.
mysql_db = MySQLDatabase(db_name, user='ecitytest', password='ecitytest',
                         host='10.37.149.5', port=3306)
mysql_db.connect()

class Pro_propower_inspection_detail_feedback_file(Model):
    # 自增主键
    gid = IntegerField(column_name='gid', primary_key=True)
    # 反馈记录id
    feedbackid = IntegerField()
    # 检查内容id
    inspectdetailid = IntegerField()
    # 文件名
    fileName = CharField(column_name='filename')
    # 文件存储值
    fileUrl = CharField(column_name='fileurl')
    createTime = DateTimeField(column_name='createtime', default=datetime.datetime.now)
    # updatetime timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    # 文件服务器 URL 全路径
    fastdfsUrl = CharField(column_name='fastdfsurl')
    # 是否升级fastdfs，0=否，1=是
    fastdfs = IntegerField(null=False, default=0)

    class Meta:
        database = mysql_db
        table_name = 'pro_propower_inspection_detail_feedback_file'

    # def before_request_handler(self):
    #     self.database.connect()

if __name__ == '__main__':
    # get() 返回一条
    p = Pro_propower_inspection_detail_feedback_file
    query = p.select().where(p.fastdfs == 0).order_by(p.gid.desc()).limit(50)

    dict1 = [(q.gid, q.fileUrl) for q in query]
    print(dict1)
    # for q in query:
    #     print(q.gid)
    #     # 调用 MongoDD 接口
    inspectdetailid + "/" + PhotosFilePath.ProjectPrower + "/" + feedbackid + "/"
    {"proid":"146","type":"ProjectPrower","key":"306"}

    #     print(q.fileName)
    #     print(q.fileUrl)

