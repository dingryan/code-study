"""
删除测试数据脚本

功能说明：
    该脚本用于删除运营中台的测试数据，包括：
    1. 九宫格运营栏目数据
    2. 九宫格图标数据
    3. 图标素材数据

使用方式：
    直接运行脚本：python delete_hundsun.py
    或导入模块后调用相应方法

注意事项：
    - 需要先配置test_data.yaml文件中的环境信息
    - 需要确保网络连接正常，能够访问运营中台API
    - 删除操作不可逆，请谨慎使用
"""

import yaml
import os
import requests
import sys
import jsonpath
from login_scyd import Login

# 获取当前脚本所在文件夹路径
curPath = os.path.dirname(os.path.realpath(__file__))
# 获取yaml文件路径
yamlPath = os.path.join(curPath, "test_data.yaml")

with open(yamlPath,"r",encoding='utf-8') as f:
    result = yaml.load(f.read(),Loader=yaml.FullLoader)

# 环境变量 qa or dev
envir = "qa"
access_token = Login(envir).center_login()



class DeleteTestDate(object):
    """
    删除测试数据类
    
    提供删除运营中台测试数据的方法，包括：
    - 九宫格运营栏目
    - 九宫格图标
    - 图标素材
    """

    def delete_column(self):

        # url = result['Center'][envir]['url'] + "/scyd/hundsun/icon/column/list"
        url = result['Center'][envir]['url'] + "/ydmanage/v1/icon/column/list"
        
        # 设置请求头，包含访问令牌用于身份验证
        headers = {"access_token": access_token}
        
        # 第一个查询参数：查询"行情栏目"相关的运营栏目
        params = {
            "colu_name": "行情栏目",  # 栏目名称关键字
            "start": "1",  # 分页起始位置
            "limit": "10000",  # 每页最大返回数量（设置较大值以获取所有数据）
            "publish_type": 0,  # 发布类型：0-全部
            "colu_type": "",  # 栏目类型（空表示不筛选）
            "status": "",  # 状态（空表示不筛选）
            "group_name": "",  # 分组名称（空表示不筛选）
            "icon_name": "",  # 图标名称（空表示不筛选）
            "colu_category": ""  # 栏目分类（空表示不筛选）
        }
        params2 = {
            "colu_name": "图标",  # 栏目名称关键字
            "start": "1",
            "limit": "10000",
            "publish_type": 0,
            "colu_type": "",
            "status": "",
            "group_name": "",
            "icon_name": "",
            "colu_category": ""
        }
        
        # 发送GET请求查询运营栏目列表
        res_data = requests.get(url, headers=headers, params=params).json()
        res_data2 = requests.get(url, headers=headers, params=params2).json()

        # 使用jsonpath提取所有栏目的序列号(serial_no)
        # jsonpath表达式 '$..list[*].serial_no' 表示：递归查找所有list数组中的serial_no字段
        colu_list = jsonpath.jsonpath(res_data, '$..list[*].serial_no')
        print(colu_list)
        colu_list2 = jsonpath.jsonpath(res_data2, '$..list[*].serial_no')
        print(colu_list2)

        # 如果需要合并两个查询结果，可以取消下面的注释
        # colu_list.extend(colu_list2)
        print(colu_list)

        try:
            # colu_list.extend(colu_list2)
            # for j in colu_list2:
            #     # 下架九宫格
            #     url = result['Center'][envir]['url'] + "/scyd/hundsun/operation/set"
            #     headers = {"access_token": access_token}
            #     json = {
            #         "serial_no": j,
            #         "operation_type": 3,
            #         "status": "0"
            #     }
            #     requests.post(url, headers=headers, json=json).json()
            #
            #     # 删除运营栏目
            #     url = result['Center'][envir]['url'] + "/scyd/hundsun/icon/column/delete"
            #     headers = {"access_token": access_token}
            #     json = {
            #         "serial_nos": j
            #     }
            #     requests.post(url, headers=headers, json=json).json()
            # print(colu_list)

            for i in colu_list:
                # ========== 第一步：下架运营栏目 ==========
                # 下架操作：将运营栏目的状态设置为0（下架状态）
                # 注意：删除前先下架，确保数据安全
                url = result['Center'][envir]['url'] + "/ydmanage/v1/operation/set"
                headers = {"access_token": access_token}
                json_data = {
                    "serial_no": i,  # 栏目序列号
                    "operation_type": 3,  # 操作类型：3-运营栏目操作
                    "status": "0",  # 状态：0-下架
                    "menuId": "58fc25cd-8dc1-4bc9-a3c9-88a6daa54b42"  # 菜单ID（固定值）
                }
                # 发送POST请求执行下架操作
                response = requests.post(url, headers=headers, json=json_data)
                print(f"栏目 {i} 下架结果: {response.status_code}")
                
                # ========== 第二步：删除运营栏目 ==========
                # 删除操作：永久删除运营栏目数据
                # 注意：删除操作不可逆，请谨慎使用
                url = result['Center'][envir]['url'] + "/ydmanage/v1/icon/column/delete"
                headers = {"access_token": access_token}
                json_data = {
                    "serial_nos": i,  # 栏目序列号（可以是单个值或数组）
                    "menuId": "58fc25cd-8dc1-4bc9-a3c9-88a6daa54b42"  # 菜单ID（固定值）
                }
                requests.post(url, headers=headers, json=json).json()



            print('九宫格运营已删除')
            # return res_data
        except Exception as e:
            print(e)

    # 删除九宫格图标
    def delete_icon(self):
        """
        删除九宫格图标
        
        功能说明：
            1. 查询符合条件的九宫格图标列表
            2. 提取图标序列号(serial_no)
            3. 批量删除所有查询到的图标
        
        查询条件：
            - icon_name: 图标名称关键字（"九宫格图标"）
        
        注意事项：
            - 删除操作不可逆
            - 如果查询结果为空，不会执行删除操作
        """
        # 构建查询图标列表的API地址
        url = result['Center'][envir]['url'] + "/ydmanage/v1/icon/list"
        
        # 设置请求头，包含访问令牌
        headers = {"access_token": access_token}
        
        # 查询参数：根据图标名称查询
        params = {
            "icon_name": "九宫格图标",  # 图标名称关键字
            "start": "1",  # 分页起始位置
            "limit": "10000",  # 每页最大返回数量
            "order_type": "",  # 排序类型（空表示不排序）
            "order_column": "",  # 排序字段（空表示不排序）
            "order_dir": ""  # 排序方向（空表示不排序）
        }
        res_data = requests.get(url, headers=headers, params=params).json()
        icon_list = jsonpath.jsonpath(res_data, '$..list..serial_no')
        try:
            for i in icon_list:
                # url = result['Center'][envir]['url'] + "/scyd/hundsun/icon/delete"
                url = result['Center'][envir]['url'] + "/ydmanage/v1/icon/delete"
                headers = {"access_token": access_token}
                json = {
                    "serial_nos": i,
                    "menuId": "58fc25cd-8dc1-4bc9-a3c9-88a6daa54b42"
                }
                requests.post(url, headers=headers, json=json).json()

            print('九宫格图标已删除')
            # return res_data

        except Exception as e:
            print(e)
        # print(res_data)

    # 删除图标素材
    def delete_material(self):

        # url = result['Center'][envir]['url'] + "/scyd/hundsun/operation/material/list"
        url = result['Center'][envir]['url'] + "/ydmanage/v1/operation/material/list"
        headers = {"access_token": access_token}
        params = {
            "material_origin_name": "素材图标",
            "start": "1",
            "limit": "10000",
            "material_type": "1",
            "order_column": "",
            "order_dir": "",
            "order_type": "0"
        }
        res_data = requests.get(url, headers=headers, params=params).json()
        material_list = jsonpath.jsonpath(res_data, '$..list..serial_no')
        try:
            for i in material_list:
                # url = result['Center'][envir]['url'] + "/scyd/hundsun/operation/material/delete"
                url = result['Center'][envir]['url'] + "/ydmanage/v1/operation/material/delete"
                headers = {"access_token": access_token}
                json = {
                    "serial_nos": i,
                    "menuId": "58fc25cd-8dc1-4bc9-a3c9-88a6daa54b42"
                }
                requests.post(url, headers=headers, json=json).json()

            print('图标素材已删除')
            # return res_data
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # pass
    del1 = DeleteTestDate().delete_column()
    del2 = DeleteTestDate().delete_icon()
    del3 = DeleteTestDate().delete_material()
