"""
PMeter     --  ThreadGroup - -Collection1 -- -Api1
                                             -Api2
                                             -Api3
                           - -Collection1

           --  ThreadGroup - -Collection2
                             -Collection2

PMeter 主要负责启动串行启动Tasks，所有的Tasks执行完毕，分析数据。展示数据。
ThreadGroup 用于多线程并发测试Collection。可以配置thread_number和loop_count控制collection的并发场景。对应jmeter的线程组
HttpCollection 用于添加被测接口。可以添加多个api。使用requests.Session复用，减少网络开销。

测试场景1，10线程，循环20次，测试1个场景3api
thread_group = ThreadGroup()
thread_group.create_task(thread_number=10, loop_count=2, HttpCollection())
thread_group.run()

测试场景2，1线程，持续时间60秒，测试2个场景
thread_group = ThreadGroup()
thread_group.create_task(thread_number=2, duration=60, HttpCollection(1))
thread_group.create_task(thread_number=2, duration=10, HttpCollection(2))
thread_group.run()
"""
import json
import os
import uuid
import threading
from typing import Optional

from loguru import logger
import argparse
import requests
from queue import Queue
from datetime import datetime, timedelta


class HttpCollection:
    """
    1，要实现支持多个api，循环执行，提供统一调度入口__call__()
    2，通过json文件读取
    3，
    """

    def __init__(self, file: str, name: str = None):
        self.id: str = str(uuid.uuid4())
        self.name: str = name if name else f'TaskName'
        self.http_session = requests.Session()
        self.base_dir: str = os.getcwd()
        self.cases: list[dict] = self.read_json(file)

    def read_json(self, file: str) -> list[dict]:
        file_path = os.path.join(self.base_dir, file)
        # with open(file_path, mode='r', encoding='utf-8') as f:
        #     return json.load(f)
        return [{
            "url": "http://127.0.0.1:5000/index",
            "method": "GET",
            "headers": {
                "content-type": "application/x-www-form-urlencoded"
            },
            "data": {},
            "response": {
                "status_code": 200,
                "data": {}
            },
            "response_time": 120
        }]

    def validate(self, response: requests.Response, case: dict):
        error_msg = f'{self.id} {response.status_code} != {case.get("status_code")}'
        assert response.status_code != case.get('status_code'), error_msg

        assert response.json() != case.get('response').get('data'), error_msg

    def execute(self, case, q, stop=None, i=None):
        r: requests.Response = self.http_session.request(case.get('method'), case.get('url'))
        logger.debug(f'thread_id={threading.current_thread().name}, response_time={r.elapsed.total_seconds()}')
        # print(
        #     f'thread_id={threading.current_thread().name}, remaining={(stop - datetime.now().timestamp()):.4f}, response_time={r.elapsed.total_seconds()}')
        self.validate(r, case)
        data: dict = {
            'response_time': r.elapsed.total_seconds(),
            'data': r.json(),
            'thread_id': threading.current_thread().name
        }
        q.put(data)

    def __call__(self, q: Queue, loop_count: Optional[int], duration: Optional[float]):
        """
        有持续时间，通过持续时间执行。循环次数失效
        否则执行循环次数
        """

        if duration:
            start: float = datetime.now().timestamp()
            stop: float = (datetime.now() + timedelta(seconds=duration)).timestamp()

            while start <= stop:
                for case in self.cases:
                    try:
                        self.execute(case, q, stop=stop)
                    except Exception as e:
                        logger.error(f'{self.name}, {case} fail, e={e}')
                    start = datetime.now().timestamp()

        else:
            for i in range(loop_count):

                for case in self.cases:
                    try:
                        self.execute(case, q, i=i)
                    except Exception as e:
                        logger.error(f'{self.name}, {case} fail, e={e}')


class ThreadGroup:
    def __init__(self, thread_number: int, loop_count: Optional[int], duration: Optional[float], q: Queue):
        self.thread_number: int = thread_number
        self.loop_count: Optional[int] = loop_count
        self.duration: Optional[float] = duration
        self.group: list[threading.Thread] = []
        self.q: Queue = q

    def create(self, collection: HttpCollection):
        for _ in range(self.thread_number):
            self.group.append(
                threading.Thread(target=collection, args=(self.q, self.loop_count, self.duration)))
        return self

    def __call__(self, *args, **kwargs):
        logger.debug(f'{threading.current_thread().name} start')
        for _task in self.group:
            _task.start()
        for _task in self.group:
            _task.join()
        logger.debug(f'{threading.current_thread().name} done!!!')


def args_parser():
    parser = argparse.ArgumentParser(prog='PMeter', epilog='小测试', description='%(prog)s帮助文档',
                                     add_help=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--file', dest='file', help='指定用例文件', nargs=1, type=str, required=False)
    parser.add_argument('-h', '--help', help="这是一个帮助信息", action='store_true', default=False)
    sub = parser.add_subparsers(title='run', description='runrunrun', prog='frrun', dest='bvdsca', help='help')
    sub.add_parser('gogogo')
    sub.add_parser('gogogo1')
    return parser


class PMeter:
    """
    做线程管理，模拟jmeter多个ThreadGroup
    阻塞主线程。统计数据
    """

    def __init__(self):
        self.task_group: list[threading.Thread] = []
        self.q_map: dict[HttpCollection, Queue] = {}

    def create_task_args(self, args_parser):
        ...

    def create_task(self, collection: HttpCollection, thread_group: str = None,
                    thread_number: int = 1, loop_count: Optional[int] = 1,
                    duration: Optional[float] = None) -> 'PMeter':
        q = Queue()
        target = ThreadGroup(thread_number=thread_number, q=q,
                             loop_count=loop_count, duration=duration).create(collection)
        self.task_group.append(threading.Thread(target=target, name=thread_group))
        self.q_map[collection] = q
        return self

    def run(self):
        for task_group_thread in self.task_group:
            task_group_thread.start()
            task_group_thread.join()

    def analysis(self):
        logger.debug(f'*********** Start analysis ************')
        for collection, q in self.q_map.items():
            for _ in range(q.qsize()):
                logger.debug(f'{collection.name} , {q.get()}')
            logger.debug(f'{"-" * 20} analysis {collection.name} end!!! {"-" * 20}')


if __name__ == '__main__':
    parser = args_parser()
    args = parser.parse_args()
    parser.print_help()

    # pmeter = PMeter()
    # pmeter.create_task(collection=HttpCollection(name='api1', file=args.f), thread_number=2, loop_count=5,
    #                    thread_group='测试')
    # pmeter.run()
    # print('done!')
    # pmeter.analysis()
