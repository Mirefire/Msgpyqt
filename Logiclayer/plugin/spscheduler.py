from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime,date
import time

from Logiclayer import  auto_message
""""
APScheduler有四大组件：
1、触发器 triggers ：
触发器包含调度逻辑。每个作业都有自己的触发器，用于确定下一个任务何时运行。除了初始配置之外，触发器是完全无状态的。
有三种内建的trigger:
（1）date: 特定的时间点触发
（2）interval: 固定时间间隔触发
（3）cron: 在特定时间周期性地触发
2、任务储存器 job stores：用于存放任务，把任务存放在内存（为默认MemoryJobStore）或数据库中。
  (1)MemoryJobStore
  (2)sqlalchemy
  (3)mongodb
  (4)redis
3、执行器 executors： 执行器是将任务提交到线程池或进程池中运行，当任务完成时，执行器通知调度器触发相应的事件。
4、调度器 schedulers： 把上方三个组件作为参数，通过创建调度器实例来运行
根据开发需求选择相应的组件，下面是不同的调度器组件：
BlockingScheduler 阻塞式调度器：适用于只跑调度器的程序。
BackgroundScheduler 后台调度器：适用于非阻塞的情况，调度器会在后台独立运行。
AsyncIOScheduler AsyncIO调度器，适用于应用使用AsnycIO的情况。
GeventScheduler Gevent调度器，适用于应用通过Gevent的情况。
TornadoScheduler Tornado调度器，适用于构建Tornado应用。
TwistedScheduler Twisted调度器，适用于构建Twisted应用。
QtScheduler Qt调度器，适用于构建Qt应用。



"""

class spsch_eduler():

    def __init__(self):
        super(spsch_eduler, self).__init__()
        self.scheduler = BlockingScheduler()  # 阻塞式调度器
        self.schedulerTo = BackgroundScheduler() #非阻塞式调度器

    def func(self):
        now = datetime.now()
        ts = now.strftime('%Y-%m-%d %H:%M:%S')
        print('do func time :', ts)
        # print(lk)
    def func2(self):
        # 耗时2S
        now = datetime.now()
        ts = now.strftime('%Y-%m-%d %H:%M:%S')
        print('do func2 time：', ts)
        # print(lk)
        time.sleep(2)

    """
    1、触发器date
    特定的时间点触发，只执行一次。参数如下：
    参数	说明
    run_date (datetime 或 str)	作业的运行日期或时间
    timezone (datetime.tzinfo 或 str)
    """
    def dateRun(self,t):
        self.schedulerTo.add_job(self.func, 'date', run_date=date(2019, 8, 30), args=['text1'])
        # 在 2019-8-30 01:00:00 运行一次 job 方法
        self.schedulerTo.add_job(self.func, 'date', run_date=datetime(2019, 8, 30, 1, 0, 0), args=['text2'])
        # 在 2019-8-30 01:00:01 运行一次 job 方法
        self.schedulerTo.add_job(self.func, 'date', run_date='2019-8-30 01:00:00', args=['text3'])
        self.schedulerTo.start()

    def intervalRun(self,drawPoniter,t,*args):
        """
        2、触发器interval
        固定时间间隔触发。参数如下：
        参数	说明
        weeks (int)	间隔几周
        days (int)	间隔几天
        hours (int)	间隔几小时
        minutes (int)	间隔几分钟
        seconds (int)	间隔多少秒
        start_date (datetime 或 str)	开始日期
        end_date (datetime 或 str)	结束日期
        timezone (datetime.tzinfo 或str)
        :return:
        """
        # 创建调度器：BlockingScheduler
        # 添加任务,时间间隔2S
        print("T：%s" % t)
        print("args：%s" % args)

            # self.schedulerTo.add_job(drawPoniter, 'interval', seconds=t, id='test_job1',args=[k[0]] )
        # self.schedulerTo.add_job(self.func, 'interval', seconds=t, id='test_job1')
        # # 添加任务,时间间隔5S
        # self.schedulerTo.add_job(self.func2, 'interval', seconds=t, id='test_job2')
        #     self.schedulerTo.start()

    def cronRun(self):
        # 在每天22点，每隔 1分钟 运行一次 job 方法
        self.schedulerTo.add_job(self.func2, 'cron', hour=22, minute='*/1', args=['job1'])
        # 在每天22和23点的25分，运行一次 job 方法
        self.schedulerTo.add_job(self.func2, 'cron', hour='22-23', minute='25', args=['job2'])
        self.schedulerTo.start()
    #结束定时器
    def stopRun(self):
        self.schedulerTo.shutdown()
        self.schedulerTo.remove_job('test_job1')
        self.scheduler.shutdown()