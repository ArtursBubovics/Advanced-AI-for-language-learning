import requests
import json

from AI.Appeal_to_AI import appeal_to_ai


def get_analyzed_data(prompt):
    print("\n\033[32m--- Шаг 5: В функции(Анализ и сохранение новой 'памяти') ---\033[0m")
    print("\033[32m   -> Создаётся объединённый промпт для ИИ...\033[0m")


    combined_prompt = f"""
        Проанализируй следующий текст.

        1. Выдели и верни только главную идею одним предложением.
        2. Выдели и верни только самые важные имена, даты и термины. Верни их списком, разделенным запятыми.

        Свой ответ структурируй строго по шаблону:

        Главная идея: [Твоя главная идея]
        Ключевые слова: [Твои ключевые слова]

        Текст для анализа: {prompt}
        """
            
    print(f"   -> Отправляется промпт: {combined_prompt.strip()[:100]}...")

    statusIsTrue, ai_response = appeal_to_ai(combined_prompt)

    if statusIsTrue:
        print("\033[32m   -> Ответ от ИИ успешно получен.\033[0m")
        full_response = ai_response['response'].strip()
        print(f"   -> Полный ответ ИИ: {full_response}")

        # Разделяем ответ на две части по маркерам
        try:
            main_idea = full_response.split("Главная идея:")[1].split("Ключевые слова:")[0].strip()
            keywords = full_response.split("Ключевые слова:")[1].strip()

            print(f"\033[32m   ✓ Главная идея извлечена: '{main_idea}'\033[0m")
            print(f"\033[32m   ✓ Ключевые слова извлечены: '{keywords}'\033[0m")
            return main_idea, keywords
        except IndexError:
            # Обработка ошибки, если формат ответа не соответствует ожидаемому
            print("   ✗ Ошибка: Не удалось разобрать ответ ИИ. Проверьте формат.")
            return "", ""
    else:
        print("   ✗ Ошибка: Не удалось получить ответ от ИИ.")
        return "", ""