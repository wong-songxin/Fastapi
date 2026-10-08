"""
#  作者      :   Liu Qingzheng
#  微信      :   306334678
#  项目名    :   Kong_OA_Backend
#  文件名    :   main.py
#  创建时间  :   2025/1/16/016 20:48
"""

from src import create_app
from src.settings import setting
app=create_app()
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host=setting.APP_HOST,port=setting.APP_PORT)

