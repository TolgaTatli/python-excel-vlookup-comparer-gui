import sys
import pandas as pd
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QCheckBox, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Excel Kıyaslama Arayüzü'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 400, 500)

        layout = QVBoxLayout()

        self.sameFileCheckBox = QCheckBox('Aynı dosyada farklı sayfaları karşılaştır', self)
        layout.addWidget(self.sameFileCheckBox)
        self.sameFileCheckBox.stateChanged.connect(self.toggleSameFileOption)

        self.label1 = QLabel('Birinci dosya yolunu seçiniz:')
        layout.addWidget(self.label1)
        self.filePath1 = QLineEdit(self)
        layout.addWidget(self.filePath1)
        self.browseButton1 = QPushButton('Gözat', self)
        self.browseButton1.clicked.connect(self.browseFile1)
        layout.addWidget(self.browseButton1)

        self.label2 = QLabel('İkinci dosya yolunu seçiniz:')
        layout.addWidget(self.label2)
        self.filePath2 = QLineEdit(self)
        layout.addWidget(self.filePath2)
        self.browseButton2 = QPushButton('Gözat', self)
        self.browseButton2.clicked.connect(self.browseFile2)
        layout.addWidget(self.browseButton2)

        self.label3 = QLabel('Birinci dosyadaki sayfa adı:')
        layout.addWidget(self.label3)
        self.sheet1 = QLineEdit(self)
        layout.addWidget(self.sheet1)
        self.label3.setVisible(False)
        self.sheet1.setVisible(False)

        self.label4 = QLabel('Birinci dosyadaki sütun:')
        layout.addWidget(self.label4)
        self.column1 = QLineEdit(self)
        layout.addWidget(self.column1)

        self.label5 = QLabel('İkinci dosyadaki sayfa adı:')
        layout.addWidget(self.label5)
        self.sheet2 = QLineEdit(self)
        layout.addWidget(self.sheet2)
        self.label5.setVisible(False)
        self.sheet2.setVisible(False)

        self.label6 = QLabel('İkinci dosyadaki sütun:')
        layout.addWidget(self.label6)
        self.column2 = QLineEdit(self)
        layout.addWidget(self.column2)

        self.excelCheckBox = QCheckBox('Sonuçları Excel formatında kaydet', self)
        layout.addWidget(self.excelCheckBox)

        self.compareButton = QPushButton('Karşılaştır', self)
        self.compareButton.clicked.connect(self.compare)
        layout.addWidget(self.compareButton)

        # Imza QLabel'i ekleme
        signatureLabel = QLabel('T.T.', self)
        signatureLabel.setStyleSheet("font-size: 10px; color: gray;")
        signatureLabel.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        # Daha az boşluk bırakan bir QSpacerItem ekleme
        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Layout için bir QVBoxLayout ekleyerek imza QLabel'ini sağ alt köşeye yerleştirme
        bottomLayout = QVBoxLayout()
        bottomLayout.addSpacerItem(spacer)
        bottomLayout.addWidget(signatureLabel)

        # Ana layout'u güncelleme
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(layout)
        mainLayout.addLayout(bottomLayout)

        self.setLayout(mainLayout)

    def toggleSameFileOption(self, state):
        if state == 2:
            # Aynı dosyada kıyaslama yapılacaksa
            self.label2.setVisible(False)
            self.filePath2.setVisible(False)
            self.browseButton2.setVisible(False)
            self.label3.setVisible(True)
            self.sheet1.setVisible(True)
            self.label5.setVisible(True)
            self.sheet2.setVisible(True)
        else:
            # Farklı dosyalar kıyaslanacaksa
            self.label2.setVisible(True)
            self.filePath2.setVisible(True)
            self.browseButton2.setVisible(True)
            self.label3.setVisible(False)
            self.sheet1.setVisible(False)
            self.label5.setVisible(False)
            self.sheet2.setVisible(False)

    def browseFile1(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Birinci dosya yolunu seçiniz", "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options)
        if filePath:
            self.filePath1.setText(filePath)

    def browseFile2(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "İkinci dosya yolunu seçiniz", "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options)
        if filePath:
            self.filePath2.setText(filePath)

    def compare(self):
        firstFile = self.filePath1.text()
        secondFile = self.filePath2.text()
        column1 = self.column1.text()
        column2 = self.column2.text()
        sameFile = self.sameFileCheckBox.isChecked()
        sheet1 = self.sheet1.text() if sameFile else None
        sheet2 = self.sheet2.text() if sameFile else None

        if not firstFile or (not secondFile and not sameFile) or not column1 or not column2:
            QMessageBox.warning(self, 'Hata', 'Tüm alanları doldurunuz.')
            return

        try:
            if sameFile:
                dataframe1 = pd.read_excel(firstFile, sheet_name=sheet1)
                dataframe2 = pd.read_excel(firstFile, sheet_name=sheet2)
            else:
                dataframe1 = pd.read_excel(firstFile)
                dataframe2 = pd.read_excel(secondFile)
        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Dosyaları okurken hata oluştu: {str(e)}')
            return

        matched_column1 = self.getMatchedColumnName(column1, dataframe1.columns)
        matched_column2 = self.getMatchedColumnName(column2, dataframe2.columns)

        if not matched_column1:
            QMessageBox.warning(self, 'Hata', f'Birinci dosyada "{column1}" adlı bir sütun bulunamadı.')
            return
        
        if not matched_column2:
            QMessageBox.warning(self, 'Hata', f'İkinci dosyada "{column2}" adlı bir sütun bulunamadı.')
            return

        data1 = json.loads(dataframe1.to_json(orient='records'))
        data2 = json.loads(dataframe2.to_json(orient='records'))

        list1 = [str(record.get(matched_column1, '')).strip() for record in data1] 
        list2 = [str(record.get(matched_column2, '')).strip() for record in data2]

        set1, set2 = set(list1), set(list2)

        unique_in_file1, unique_in_file2 = sorted(set1 - set2), sorted(set2 - set1)

        self.writeFiles(unique_in_file1, unique_in_file2)

    def getMatchedColumnName(self, column_name, columns):
        for col in columns:
            if col.lower() == column_name.lower():
                return col
        return None

    def writeFiles(self, unique_in_file1, unique_in_file2):
        writeLocation1, _ = QFileDialog.getSaveFileName(self, "Birinci dosyada olup ikinci dosyada olmayanları kaydet", "", "Text Files (*.txt);;All Files (*)")
        writeLocation2, _ = QFileDialog.getSaveFileName(self, "İkinci dosyada olup birinci dosyada olmayanları kaydet", "", "Text Files (*.txt);;All Files (*)")

        if not writeLocation1 or not writeLocation2:
            return

        try:
            with open(writeLocation1, "w") as writeFile1:
                for value in unique_in_file1:
                    writeFile1.write(value + "\n")

            with open(writeLocation2, "w") as writeFile2:
                for value in unique_in_file2:
                    writeFile2.write(value + "\n")

            QMessageBox.information(self, 'Başarılı', 'İşlem tamamlandı')

            if self.excelCheckBox.isChecked():
                self.convertToExcel(writeLocation1, unique_in_file1)
                self.convertToExcel(writeLocation2, unique_in_file2)

            self.clearFields()

        except Exception as e:
            QMessageBox.critical(self, 'Hata', f'Dosyaları yazarken hata oluştu: {str(e)}')

    def convertToExcel(self, txtFilePath, data):
        excelFilePath = txtFilePath.replace('.txt', '.xlsx')
        df = pd.DataFrame(data, columns=["Değerler"])
        df.to_excel(excelFilePath, index=False)
        QMessageBox.information(self, 'Başarılı', f'{excelFilePath} olarak kaydedildi')

    def clearFields(self):
        self.filePath1.clear()
        self.filePath2.clear()
        self.column1.clear()
        self.column2.clear()
        self.sheet1.clear()
        self.sheet2.clear()
        self.excelCheckBox.setChecked(False)
        self.sameFileCheckBox.setChecked(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
