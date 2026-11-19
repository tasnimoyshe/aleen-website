import os
from io import BytesIO
import requests
from PIL import Image, ImageFilter
from dotenv import load_dotenv


def has_transparent_background(img):
    """ছবিটি আগে থেকেই ব্যাকগ্রাউন্ডলেস PNG কি না চেক করে"""
    if img.mode != 'RGBA':
        return False
    w, h = img.size
    points = [
        (0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
        (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2),
    ]
    transparent_count = sum(1 for x, y in points if img.getpixel((x, y))[3] < 20)
    return transparent_count >= 6


def process_hero_bouquet(image_field, canvas_size=(1000, 1050)):
    """
    1. ব্যাকগ্রাউন্ড থাকলে remove.bg API দিয়ে রিমুভ করে
    2. কোণার সূক্ষ্ম নয়েজ বাদ দিয়ে একদম ফুলের আসল বর্ডার অনুযায়ী টাইট ক্রপ করে
    3. গোল, চওড়া বা লম্বা—সব বুকেকে সমানভাবে বড় করে (৯৬% ফ্রেম জুড়ে) সেভ করে
    """
    load_dotenv(override=True)

    with image_field.open('rb') as f:
        f.seek(0)
        raw_bytes = f.read()

    img = Image.open(BytesIO(raw_bytes))
    if img.mode in ('RGBA', 'LA') or 'transparency' in img.info:
        img = img.convert('RGBA')

    status_msg = "Already transparent — tightly cropped & resized!"

    if not has_transparent_background(img):
        api_key = os.environ.get('REMOVEBG_API_KEY', '').strip()
        if not api_key:
            return None, ".env ফাইলে REMOVEBG_API_KEY পাওয়া যায়নি।"

        try:
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': ('bouquet.png', raw_bytes)},
                data={'size': 'auto'},
                headers={'X-Api-Key': api_key},
                timeout=40,
            )
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content)).convert('RGBA')
                status_msg = "Background removed & resized successfully!"
            else:
                return None, f"remove.bg API Error ({response.status_code}): {response.text}"
        except requests.RequestException as e:
            return None, f"Network Error: {e}"

    # ধাপ ২: অদৃশ্য ছায়া বা ১-২ পিক্সেল নয়েজ বাদ দিয়ে একদম ফুলের আসল বর্ডার শনাক্ত করা
    alpha = img.getchannel('A')
    solid_mask = alpha.point(lambda p: 255 if p > 80 else 0)
    cleaned_mask = solid_mask.filter(ImageFilter.MinFilter(3))
    bbox = cleaned_mask.getbbox() or alpha.point(lambda p: 255 if p > 25 else 0).getbbox()

    if bbox:
        w_orig, h_orig = img.size
        pad_x = max(8, int((bbox[2] - bbox[0]) * 0.02))
        pad_y = max(8, int((bbox[3] - bbox[1]) * 0.02))
        crop_box = (
            max(0, bbox[0] - pad_x),
            max(0, bbox[1] - pad_y),
            min(w_orig, bbox[2] + pad_x),
            min(h_orig, bbox[3] + pad_y),
        )
        img = img.crop(crop_box)

    # ধাপ ৩: সব বুকেকে সমানভাবে বড় (ক্যানভাসের ৯৬% জুড়ে) করে মাঝখানে বসানো
    canvas_w, canvas_h = canvas_size
    max_w = int(canvas_w * 0.96)
    max_h = int(canvas_h * 0.96)

    w, h = img.size
    if w > 0 and h > 0:
        scale = min(max_w / w, max_h / h)
        new_w = max(1, int(w * scale))
        new_h = max(1, int(h * scale))
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        canvas = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
        paste_x = (canvas_w - new_w) // 2
        paste_y = (canvas_h - new_h) // 2
        canvas.paste(img, (paste_x, paste_y), img)
        img = canvas

    output = BytesIO()
    img.save(output, format='PNG', optimize=True)
    output.seek(0)
    return output, status_msg