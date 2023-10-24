# start all jobs wihtin the given directory as argument
#
# usage: python3 jobs.py <jobs directory>

import sys
import importlib
import os
import time
import multiprocessing

sys.path.insert(0, './jobs')


class JobProcess(multiprocessing.Process):

    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.job_queue = queue
        self.log = multiprocessing.SimpleQueue()

    def run(self):

        while not self.job_queue.empty():
            job_file = self.job_queue.get()
            job = importlib.import_module(job_file)
            
            start = time.time()

            try:
                result = str(job.run())
            except Exception as e:
                result = "Error: " + str(e)

            # end time
            end = time.time()

            file_name = job.__name__ + '.result'
            
            with open(file_name, 'w') as f:
                f.write(result)

            #add log to log queue
            self.log.put(f"{job.__name__} | result: {result} | start-time: {start} | end-time: {end} | delta: {end-start}\n")


            print(result)


def main(n = 100):

    # get all jobs
    jobs = [f[:-3] for f in os.listdir(sys.argv[1]) if f.endswith('.py')]
    
    # create a job queue for process
    job_queue = multiprocessing.Queue()
    
    for job in jobs:
        job_queue.put(job)
    
    #create n process
    processes = []
    for i in range(n):
        processes.append(JobProcess(job_queue))
    
    #start all process
    for process in processes:
        process.start()
    
    #join all process
    for process in processes:
        process.join()

    #create an empty log file
    with open('log.txt', 'w') as f:
        f.write('')

    #write log to file
    with open('log.txt', 'a') as f:
        for process in processes:
            while not process.log.empty():
                log = f"Process {processes.index(process)} | " + process.log.get()
                f.write(log)
        


if __name__ == '__main__':

    n=1000
    
    if len(sys.argv) <2:
        sys.argv.insert(1,'jobs')
        print(sys.argv)
        main(n)
    
    else:
        main(n)