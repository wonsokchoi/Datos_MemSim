from abc import ABC, abstractmethod
import settings as st
import circularLinkedList

lpnlist = []


class CacheStat:
    def __init__(self, slots, refs, hits):
        self.slots = slots
        self.refs = refs
        self.hits = hits
    
    def __str__(self):
        stat = f"cache_size = {self.slots} \ntotal_refs = {self.refs}\n\
hits = {self.hits}\nhit_ratio = {self.hits/self.refs}"
        
        stat = f"cache_size = {self.slots} total_refs = {self.refs} \
hits = {self.hits} hit_ratio = {self.hits/self.refs}"
        return stat
    

class Cache:
    def __init__(self, capacity: int, unit):
        self.slots = capacity
        self.unit = unit # 캐쉬 내 데이터 관리 단위
        self.hits = 0
        self.refs = 0

    @abstractmethod
    def access(self, line):
        pass

    def do_sim(self, _conf):
        conf = st.Settings(_conf)
        for f in conf.files:
            for trc in conf.trcs:
                filename = conf.dir + f + "_" + str(conf.line_size) + "." + trc
                self.reset()
                with open(filename, "r") as file:

                    for line in file:
                        newline = int(line.strip())
                        lpn = newline // self.unit
                        self.future_accesses.append(lpn)
                        
                with open(filename, 'r') as df:
                    addr = df.readline()
                    while addr:
                        self.access(addr)
                        addr = df.readline()

            print(f, end=' ')
            print(self.stats())

class LRUCache(Cache):
    def __init__(self, capacity: int, unit):
        super().__init__(capacity, unit)

        self.dlist = []


    def reset(self):
        self.hits = 0
        self.refs = 0
        self.dlist.clear()


    def access(self, line):
        self.refs += 1 
        line = int(line)

        lpn = line // self.unit


        if lpn in self.dlist:
            # self.ranks.append(self.stack.index(lpn)+1)
            self.dlist.remove(lpn)
            self.dlist.insert(0, lpn) # MRU position: head
            self.hits +=1
        else:
            if len(self.dlist) == self.slots:
                # oldest = self.stack.pop(0)
                self.dlist.pop(-1)
            self.dlist.insert(0, lpn)

    def stats(self):
        cache_stat = CacheStat(self.slots,
                              self.refs, self.hits)
        return cache_stat


class OPTCache(Cache):
    def __init__(self, capacity: int, unit):
        super().__init__(capacity, unit)
        self.dlist = []
        self.future_accesses = []        

    def reset(self):
        self.hits = 0
        self.refs = 0
        self.dlist.clear()
        self.future_accesses.clear()        
            
    def __find_farest(self, futureaccesses):
        farthest_index = -1
        farthest_lpn = None

        for lpn in self.dlist:
            if lpn not in futureaccesses:
                return lpn

            index = futureaccesses.index(lpn)
            if index > farthest_index:
                farthest_index = index
                farthest_lpn = lpn
        return farthest_lpn

    def access(self, line) -> None:
        self.refs += 1
        line = int(line)
        self.future_accesses.pop(0)
        futureaccesses = self.future_accesses

        lpn = line // self.unit

        if lpn in self.dlist:
            self.dlist.remove(lpn)
            self.dlist.insert(0, lpn)
            self.hits += 1
        else:
            if len(self.dlist) == self.slots:
                evicted_lpn = self.__find_farest(futureaccesses)
                self.dlist.remove(evicted_lpn)
            self.dlist.insert(0, lpn)

    def stats(self):
        cache_stat = CacheStat(self.slots,
                              self.refs, self.hits)
        return cache_stat

# class LFUCache(Cache):
#     def __init__(self, capacity: int, unit):
#         super().__init__(capacity, unit)
#         self.dlist = []

    



