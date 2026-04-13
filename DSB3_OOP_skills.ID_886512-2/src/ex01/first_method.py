class Reasearch:
    def file_reader():
        with open("data.csv") as file:
            return file.read()

if __name__ == "__main__":
    print(Reasearch.file_reader())