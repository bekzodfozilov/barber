from environs import Env
# import psycopg2
#
# con = psycopg2.connect(
#     database='postgres',
#     user='postgres',
#     password='XTgk4m66jmfdo15h53xzU8iaVJ'
# )
#
# cur = con.cursor()

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")

# async def insert_users(user_id):
#     try:
#         cur.execute(f"""
#     insert into users(id)
#     VALUES ('{user_id}')""")
#         con.commit()
#     except Exception as error:
#         print(error)
#
# def in_users():
#     try:
#         cur.execute(f"select id from users")
#         return cur.fetchall()
#     except Exception as error:
#         print(error)

# def in_users():
#     try:
#         cur.execute(f"select id from users")
#         users = []
#         for i in cur.fetchall():
#             for j in i:
#                 users.append(j)
#         return users
#     except Exception as error:
#         print(error)
        
# def count():
#     try:
#         cur.execute(f"select count(*) from users")
#         return cur.fetchone()
#     except Exception as error:
#         print(error)