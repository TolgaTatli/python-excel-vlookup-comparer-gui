import pandas as pd
import json


firstFile = input("Birinci dosya yolunu giriniz: ")
secondFile = input("İkinci dosya yolunu giriniz: ")

dataframe1 = pd.read_excel(firstFile)
dataframe2 = pd.read_excel(secondFile)

column1 = input("Birinci dosyadaki hangi sütunu kıyaslayacağınızı seçiniz: ")
column2 = input("İkinci dosyadaki hangi sütunu kıyaslayacağınızı seçiniz: ")


data1 = json.loads(dataframe1.to_json(orient='records'))
data2 = json.loads(dataframe2.to_json(orient='records'))

list1 = [str(record.get(column1, '')).strip() for record in data1] 
list2 = [str(record.get(column1, '')).strip() for record in data2]

set1, set2 = set(list1), set(list2)

unique_in_file1,unique_in_file2 = sorted(set1 - set2), sorted(set2 - set1)


def writeFiles(uniquefile1, uniquefile2):
    print("Birinci dosyada olup ikinci dosyada olmayanları nereye yazdırmak istersin:")
    writeLocation1 = input()

    print("İkinci dosyada olup birinci dosyada olmayanları nereye yazdırmak istersin:")
    writeLocation2 = input()

    try:
        with open(writeLocation1, "w") as writeFile1:
            for value in unique_in_file1:
                writeFile1.write(value + "\n")

        with open(writeLocation2, "w") as writeFile2:
            for value in unique_in_file2:
                writeFile2.write(value + "\n")

    except FileExistsError:
        print("Dosya yolunu doğru girdiğinize emin misiniz?")

    finally:
        print("İşlem tamamlandı")


if __name__ == "__main__":
    writeFiles(unique_in_file1,unique_in_file2)


# print("\nBirinci dosya'da olup İkinci dosyada olmayanlar:")

# for value in unique_in_file1:
#     print(value)

# print("\nIkıncı dosyada olup birinci dosyada olmayanlar:")

# for value in unique_in_file2:
#     print(value)


