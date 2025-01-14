import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 获取 Neo4j 连接信息
neo4j_uri = os.getenv('NEO4J_URI')
neo4j_user = os.getenv('NEO4J_USERNAME')
neo4j_password = os.getenv('NEO4J_PASSWORD')

# 建立连接
driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

# 执行 Cypher 查询
def execute_query(query, parameters=None):
    with driver.session() as session:
        result = session.run(query, parameters)
        return [record for record in result]

