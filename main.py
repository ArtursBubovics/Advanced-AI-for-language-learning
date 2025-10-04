from DB.cromadb import handle_user_request

user_id = "user_123"

print("\033[32mСистема запущена. Начните общение с ИИ.\033[0m")
print("---")

while True: 
    entered_text = input('Enter your text: ')

    # Шаг 1: Пользовательский ввод
    print(f"Пользователь: '{entered_text}'")

    response = handle_user_request(user_id, entered_text) #!!!!!!!!!!!!!обрабатывать ошибки, которые могут вернуться

    # Шаг 5: Получение ответа и завершение цикла
    print(f"Ответ ИИ: {response}")
    print("\n------------\n\n")