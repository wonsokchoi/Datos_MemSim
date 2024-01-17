class Settings:
    def __init__(self, obj=None):

        if obj is None:
            self.dir = "./traces/"
            self.odir = "./figures/"
            self.files = ["bert", "tpcc", "ycsb"]
            # self.files = ["tpcc"]
            # self.files = ["tmp"]
            # self.files = ["page_rank"]
            self.trcs = ["paddr"]
            # caches = ["lru_stack", "lfu_stack", "distance"]
            self.page_size = (1 << 13) # Page size (8KB)
            self.line_size = (1 << 6) # Line size
        else:
            self.dir = obj.dir
            self.odir = obj.odir
            self.files = obj.files
            self.trcs = obj.trcs
            # caches = ["lru_stack", "lfu_stack", "distance"]
            self.page_size = obj.page_size
            self.line_size = obj.line_size
    
    # def __init__(self, obj):
    #     self.obj = obj