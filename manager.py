# coding:utf-8
from app import create_app
from flask_script import Manager
import platform
node_name = platform.node()
appn = create_app(node_name or 'default')
manager = Manager(appn)



@manager.command
def tests():
    """
    this is a tests command which is run ./tests 
    """
    import unittest
    from tests import test_weeks
    all_tests = unittest.TestLoader().loadTestsFromModule(test_weeks)
    unittest.TextTestRunner(verbosity=2).run(all_tests)



# python manager.py run_realtime_five_minutes
@manager.command
def run_realtime_five_minutes():
    "实时数据生成脚本"
    from tools.count_realtime_section_datas import Count_realtime_five_minutes
    Count_realtime_five_minutes()




if __name__ == '__main__':
    manager.run()
