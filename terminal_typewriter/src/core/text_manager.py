import random
from typing import List


BEGINNER_TEXTS: List[str] = [
    "The sun rises in the east every morning. Birds sing sweet melodies in the trees. Children play in the park with their friends. Life is beautiful and simple.",
    "Today is a wonderful day to practice typing. Keep your fingers moving steadily across the keyboard. Focus on accuracy first, then speed will follow naturally.",
    "Reading books helps expand your knowledge. Walking in nature brings peace to the mind. Drinking water is essential for good health. Regular exercise keeps you fit.",
    "Music brings joy to everyone's life. Dancing makes people happy and energetic. Cooking is both an art and science. Learning new skills is always rewarding.",
    "Time passes quickly when you're having fun. Family gatherings create lasting memories. Friendship is a precious gift to treasure. Laughter is the best medicine.",
]

INTERMEDIATE_TEXTS: List[str] = [
    "On Tuesday, Sarah visited the local market & bought: fresh vegetables, fruits, and bread! The total cost was $45.75, which seemed reasonable.",
    "Have you ever wondered why typing skills are so important? In today's digital age, fast & accurate typing can save hours of time!",
    "The weather forecast predicts 75% chance of rain & thunderstorms tomorrow; don't forget your umbrella! Temperature will range from 18°C to 25°C.",
    "Mr. Smith's presentation impressed everyone - his charts showed 45% growth in Q2! The team celebrated with pizza & refreshments later.",
    "The museum's new exhibit features artwork from the 1800s & early 1900s; tickets cost $22.50 for adults, $15.75 for students.",
]

ADVANCED_TEXTS: List[str] = [
    "In Q1 2024, company XYZ reported 187.5% growth, processing @250,000 transactions/day! The CEO announced $2.5M investment in AI & ML tools.",
    "According to recent studies, ~75% of professionals type >65 WPM; however, only 15% achieve >100 WPM. Want to join the top 5%?",
    "Project #A-123 requires completion by 15/03/2024; estimated budget: $750K (+/- 10%). Contact support@company.com for queries.",
    "In 2023, global tech spending reached $4.5T (€4.1T); AI investments grew by 235%! Average ROI: 180% across 500+ companies.",
    "Database query optimized from O(n²) to O(log n), improving performance by 400%! Server load decreased from 85% to 23.5%.",
]

EXPERT_TEXTS: List[str] = [
    "def optimize_performance(data: List[int]) -> float:\n    return sum(x * 1.5 for x in data if x > 0) # O(n) complexity",
    "async def process_data(queue: asyncio.Queue) -> Dict[str, Any]:\n    while not queue.empty():\n        item = await queue.get()",
    "class DatabaseManager:\n    def __init__(self, config: Dict):\n        self.pool = await create_pool(**config)\n        self.cache = LRUCache(1000)",
    "@decorator(param='value')\ndef handle_request(request: Request) -> Response:\n    try:\n        data = validate_input(request.data)\n    except ValidationError as e:",
    "from typing import Optional, Union\n\nclass Node[T]:\n    def __init__(self, value: T, next: Optional['Node[T]'] = None):\n        self.value = value",
]


class TextManager:
    def __init__(self) -> None:
        self.level_to_texts = {
            "beginner": BEGINNER_TEXTS,
            "intermediate": INTERMEDIATE_TEXTS,
            "advanced": ADVANCED_TEXTS,
            "expert": EXPERT_TEXTS,
        }

    def get_text(self, level: str, duration_seconds: int) -> str:
        target_word_count = int(duration_seconds * 2.5)
        source_list = self.level_to_texts.get(level, BEGINNER_TEXTS)
        selected = random.choice(source_list)
        words = selected.split()
        while len(words) < target_word_count:
            words.extend(random.choice(source_list).split())
        return " ".join(words[:target_word_count])