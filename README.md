# PMeter
`A light performance test tools`
```python
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
```
