import requests
import json

def appeal_to_ai(prompt):
    # Ollama ожидает POST-запрос именно по этому адресу.
    print("\n--- Отправка запроса в Ollama ---")
    api_url = "http://localhost:11434/api/generate"

    data = {
        "model": "qwen3:14b", 
        #Объясни грамматическую тему 'Present Perfect Continuous' в английском языке. Сделай объяснение максимально простым и понятным, как для начинающего. Используй простые примеры. Обязательно объясни главное отличие этого времени от 'Present Perfect' и 'Present Continuous', чтобы пользователь не запутался. В конце, дай краткое правило-шпаргалку: 'Когда использовать Present Perfect Continuous?'
        #Объясни грамматическое время 'Present Perfect Continuous' так, чтобы его мог понять любой человек. Используй очень простые жизненные примеры и аналогии. Не используй грамматические термины вроде 'вспомогательный глагол' или 'причастие'. Покажи, чем это время отличается от 'Present Perfect' и 'Present Continuous' на простых примерах. В конце, дай краткую шпаргалку.
        "prompt": prompt,
        # Получить весь ответ сразу, а не по частям
        "stream": False 
    }

    try:
        response = requests.post(api_url, data=json.dumps(data))
        response.raise_for_status()  # Проверяем, что запрос успешный

        print("\033[32m   ✓ Запрос успешно отправлен и получен ответ.")
        
        # Парсим ответ.
        result = response.json()
        return 1, result

    except requests.exceptions.RequestException as e:
        print(f"   ✗ Ошибка: Не удалось подключиться к Ollama. Причина: {e}")
        return 0, f"Ошибка при подключении к Ollama: {e}"
    except KeyError:
        print("   ✗ Ошибка: Некорректный формат ответа. В ответе нет ключа 'response'.")
        return 0, {"error": "Ошибка: Некорректный формат ответа от Ollama."}
    except Exception as e:
        print(f"   ✗ Неизвестная ошибка: {e}")
        return 0, {"error": "Неизвестная ошибка."}