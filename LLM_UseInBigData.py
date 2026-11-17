import pandas as pd
import requests
import json
import sys

# ============================================================
# 1. КОНФИГУРАЦИЯ – API ключът е директно в кода (без .env)
# ============================================================
OPENROUTER_API_KEY = "secret-key-goes-here"

MODEL = "deepseek/deepseek-v3.2-exp"

# ============================================================
# 2. ЗАРЕЖДАНЕ И СТАТИСТИЧЕСКИ ИЗЧИСЛЕНИЯ
# ============================================================
def load_and_analyze(csv_path):
    df = pd.read_csv(csv_path)
    df = df.dropna().drop_duplicates()
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if not numeric_cols:
        raise ValueError("CSV файлът не съдържа числови колони за анализ.")

    target_col = 'Sales' if 'Sales' in df.columns else numeric_cols[0]

    stats = {}

    stats['target_column'] = target_col
    stats['total_records'] = len(df)
    stats['total_sum'] = float(df[target_col].sum())
    stats['mean'] = float(df[target_col].mean())
    stats['median'] = float(df[target_col].median())
    stats['min'] = float(df[target_col].min())
    stats['max'] = float(df[target_col].max())
    stats['std'] = float(df[target_col].std())

    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    grouped_results = {}

    for col in cat_cols[:2]:
        try:
            grouped = df.groupby(col)[target_col].agg(['sum', 'mean', 'count']).round(2)
            grouped_results[col] = grouped.to_dict('index')
        except Exception:
            pass

    stats['grouped_by'] = grouped_results

    return df, stats

# ============================================================
# 3. ИЗПРАЩАНЕ КЪМ OPENROUTER
# ============================================================
def ask_llm_for_business_analysis(stats_dict):

    stats_json = json.dumps(stats_dict, indent=2, ensure_ascii=False)

    system_prompt = (
        "Ти си старши бизнес анализатор. Получаваш статистически обобщения от dataset с продажби. "
        "Направи кратък, изпълнителен бизнес анализ на български език. "
        "Структурирай отговора така: 1) Ключови наблюдения, 2) Силни страни, 3) Рискове/проблеми, 4) Конкретни препоръки. "
        "Бъди конкретен и базирай изводите си САМО на подадените числа."
    )

    user_prompt = f"Ето статистиките от продажбите:\n\n{stats_json}\n\nНаправи бизнес анализ."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost",
        "X-OpenRouter-Title": "Sales Analysis Script"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 2000
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=60
        )
        response.raise_for_status()
        result = response.json()

        analysis_text = result['choices'][0]['message']['content']
        return analysis_text

    except requests.exceptions.RequestException as e:
        return f"Грешка при връзка с OpenRouter: {e}\n\nОтговор: {getattr(e.response, 'text', 'N/A')}"
    except KeyError as e:
        return f"Неочакван формат на отговора от API: {e}\nПълен отговор: {result}"

# ============================================================
# 4. ГЛАВНА ФУНКЦИЯ
# ============================================================
def main():
    csv_path = "order_details.csv"

    print("=" * 60)
    print("1. Зареждане и анализ на данните...")
    print("=" * 60)

    try:
        df, stats = load_and_analyze(csv_path)
    except FileNotFoundError:
        print(f"ГРЕШКА: Файлът '{csv_path}' не е намерен. Създайте го или сменете пътя.")
        sys.exit(1)
    except Exception as e:
        print(f"ГРЕШКА при обработка на CSV: {e}")
        sys.exit(1)

    print(f"Заредени записи: {stats['total_records']}")
    print(f"Анализирана метрика: {stats['target_column']}")
    print(f"Общо: {stats['total_sum']:.2f}")
    print(f"Средно: {stats['mean']:.2f}")
    print(f"Медиана: {stats['median']:.2f}")
    print(f"Мин/Макс: {stats['min']:.2f} / {stats['max']:.2f}")

    if stats['grouped_by']:
        print("\nГрупирани статистики (първите няколко реда):")
        for col, groups in stats['grouped_by'].items():
            print(f"\n  По '{col}':")
            for key, vals in list(groups.items())[:3]:
                print(f"    {key}: {vals}")
            if len(groups) > 3:
                print(f"    ... и още {len(groups) - 3} групи")

    print("\n" + "=" * 60)
    print("2. Изпращане към DeepSeek V4 Flash за бизнес анализ...")
    print("=" * 60)

    analysis = ask_llm_for_business_analysis(stats)

    print("\n" + "=" * 60)
    print("БИЗНЕС АНАЛИЗ ОТ LLM:")
    print("=" * 60)
    print(analysis)

if __name__ == "__main__":
    main()


