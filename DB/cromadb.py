import chromadb
import uuid

from AI.Appeal_to_AI import appeal_to_ai
from AI.Requests_for_AI.Requests_for_AI import get_analyzed_data
chroma_client = chromadb.PersistentClient(path="./my_db")
collection = chroma_client.get_or_create_collection(name="my_collection")

def handle_user_request(user_id, user_message):
    print("\033[32m////////////////////////Шаг 2: Поиск в памяти ChromaDB...\033[0m")
    results = collection.query(
        query_texts=[user_message],
        where={"user_id": user_id},
        n_results=3
    )

    print("\033[32m////////////////////////Шаг 3: Создание 'умного' промпта для ИИ...\033[0m")
    if results['documents'] and results['documents'][0]:
        found_documents  = results['documents'][0]
        found_context = " ".join(found_documents)
        print("")
        print(f"\033[32m   ✓ Контекст найден: {found_context}\033[0m")
        print("")

        prompt_for_ai = f"""
        Вот контекст из нашей прошлой беседы: {found_context}
        Пользователь пишет: {user_message}
        Ответь, используя прошлый контекст, но не повторяй его.
        """
    else:
        print("✗ Контекст не найден. Создаём новый запрос.")
        
        prompt_for_ai = f"Пользователь пишет: {user_message}"
        
    statusIsTrue, ai_response = appeal_to_ai(prompt_for_ai)

    if statusIsTrue:
        print("\033[32m////////////////////////Шаг 4: Ответ от ИИ успешно получен.\033[0m")

        full_text_to_save = f"user: {user_message} | ai: {ai_response['response']}" 

        print("\033[32m////////////////////////Шаг 5: Анализ и сохранение новой 'памяти'...\033[0m")
        main_idea, keywords = get_analyzed_data(full_text_to_save) # там внутри с ии все в порядке 
        combined_text = f"Главная идея: {main_idea} | Ключевые слова: {keywords}"

        collection.add(
            documents=[combined_text],
            metadatas=[{"user_id": user_id, "type": "dialogue_summary"}],
            ids=[str(uuid.uuid4())]
        )

        print("\033[32m   ✓ Новая 'память' успешно сохранена.\033[0m")
        return ai_response['response']
        
    else:
        print("   ✗ Ошибка: Не удалось получить ответ от ИИ.")
        return "Произошла ошибка при получении ответа от ИИ. Попробуйте еще раз"