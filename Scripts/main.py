#Ассистент Маргарита
from funcitions import *
# from window import *
text="""Здравствуйте! Я ваш голосовой ассистент Маргарита. В мой функционал входит:
                    Определение погоды в любом городе планеты
                    Определение текущего времени
                    Запись задачи в список дел
                    Предоставление рейтинга лучших игр 
                    Перевод текста с русского на английский
                    Поиск запроса в Wikipedia
                    Предоставление новейших новостей 
                    """
def main():
     ToSpeak(text)
     counter=0
     while (True):
         counter+=1
         if counter == 1:
            ToSpeak("Произнесите команду после сигнала 'Производится распознавание'")
         else:
            ToSpeak("Ожидается следующая команда")
         string = Listening()
         if (string == "стоп"):
             exit(0)
         key=get_key(string)
         if key!="":
            globals()[key]()
            break

if  __name__=="__main__":
    main()