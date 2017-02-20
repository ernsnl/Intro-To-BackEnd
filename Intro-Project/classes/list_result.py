class ListResult(object):
    def __init__(self, data, total_count, page, page_size):
        self.data = []
        if len(data) > 0:
            self.data = list(data)
        self.total_count = total_count
        self.page = page
        self.page_size = page_size
