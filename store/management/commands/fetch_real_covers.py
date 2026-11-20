import os
from django.core.management.base import BaseCommand
from django.conf import settings
from store.models import Game
from PIL import Image, ImageDraw, ImageFont, ImageFilter

class Command(BaseCommand):
    help = 'Создает красивые обложки для игр'

    def handle(self, *args, **kwargs):
        media_path = os.path.join(settings.BASE_DIR, 'media', 'covers')
        os.makedirs(media_path, exist_ok=True)

        games = Game.objects.all().order_by('id')
        if not games:
            self.stdout.write(self.style.ERROR('Игр нет в базе!'))
            return

        # Разные цветовые схемы для разных игр
        themes = [
            ("#1a1a2e", "#e94560"), # Cyberpunk
            ("#2d4059", "#e8e8e8"), # Witcher
            ("#3e2723", "#ffccbc"), # Elden Ring
            ("#1c1c1c", "#d4af37"), # RDR2
            ("#003366", "#ffffff"), # God of War
            ("#0a0a0a", "#8bc34a"), # Hollow Knight
            ("#1b5e20", "#ffeb3b"), # GTA V
            ("#212121", "#b71c1c"), # Dark Souls
            ("#4a148c", "#e1bee7"), # Sekiro
            ("#bf360c", "#ffcc80"), # Ghost of Tsushima
            ("#004d40", "#b2dfdb"), # TLOU
            ("#b71c1c", "#ffcdd2"), # Spider-Man
            ("#01579b", "#81d4fa"), # Horizon
            ("#263238", "#ff7043"), # Resident Evil
            ("#311b92", "#b39ddb"), # Mass Effect
        ]

        for i, game in enumerate(games):
            if i >= len(themes):
                theme = themes[i % len(themes)]
            else:
                theme = themes[i]

            bg_color, accent_color = theme

            # Создаем вертикальную обложку 600x900 (как у Steam)
            img = Image.new('RGB', (600, 900), color=bg_color)
            draw = ImageDraw.Draw(img)

            # Добавляем градиент (имитация освещения)
            for y in range(900):
                alpha = int(50 * (y / 900))
                overlay = Image.new('RGBA', (600, 1), (0, 0, 0, alpha))
                img.paste(overlay, (0, y), overlay)

            # Пытаемся загрузить шрифты
            try:
                font_large = ImageFont.truetype("arialbd.ttf", 55)
                font_small = ImageFont.truetype("arial.ttf", 28)
            except:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()

            # Рисуем рамку
            draw.rectangle([20, 20, 580, 880], outline=accent_color, width=4)

            # Рисуем название игры с переносом строк
            title = game.title.upper()
            words = title.split()
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + word + " "
                # Проверяем ширину (чтобы не вылезало за рамку)
                if draw.textlength(test_line, font=font_large) < 520:
                    current_line = test_line
                else:
                    if current_line: lines.append(current_line.strip())
                    current_line = word + " "
            if current_line: lines.append(current_line.strip())

            # Центрируем текст по вертикали
            total_height = len(lines) * 65
            y_text = (900 - total_height) / 2

            for line in lines:
                line_w = draw.textlength(line, font=font_large)
                x_text = (600 - line_w) / 2
                
                # Тень
                draw.text((x_text+2, y_text+2), line, font=font_large, fill="black")
                # Текст
                draw.text((x_text, y_text), line, font=font_large, fill=accent_color)
                y_text += 65

            # Рисуем цену внизу
            price_text = f"{game.price} RUB"
            price_w = draw.textlength(price_text, font=font_small)
            draw.text(((600 - price_w) / 2, 800), price_text, font=font_small, fill="#ffffff")

            # Сохраняем
            filename = f"cover_{game.id}.jpg"
            filepath = os.path.join(media_path, filename)
            img.save(filepath, quality=95)

            game.cover = f"covers/{filename}"
            game.save()
            
            self.stdout.write(self.style.SUCCESS(f'Создана обложка: {game.title}'))

        self.stdout.write(self.style.SUCCESS('Все обложки успешно сгенерированы!'))