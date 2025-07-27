# 改写为类
class fun_test1:
    def load_data(self):
        print("in test1")


fun_test2 = fun_test1


dict1 = {".mp3":fun_test2}

file_extractor = dict1[".mp3"](file_name_path)

file_extractor.load_data()

