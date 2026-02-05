#!/usr/bin/env python3
"""Convert screenshots to HTML for viewing in browser"""

import base64
import os

html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dubai Trading Tools - Screenshot References</title>
    <style>
        * { margin: 0; padding: 0; }
        body {
            font-family: Arial, sans-serif;
            background: #1a1a1a;
            color: #fff;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            color: #00c853;
        }
        .gallery {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }
        .image-card {
            background: #2a2a2a;
            border-radius: 8px;
            overflow: hidden;
            border: 2px solid #00c853;
            transition: transform 0.3s;
        }
        .image-card:hover {
            transform: scale(1.02);
        }
        .image-card img {
            width: 100%;
            height: auto;
            display: block;
        }
        .image-title {
            padding: 15px;
            background: #1a1a1a;
            font-weight: bold;
            color: #00c853;
        }
        @media (max-width: 768px) {
            .gallery {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Dubai Trading Tools - Reference Screenshots</h1>
        <p style="text-align: center; margin-bottom: 30px; color: #aaa;">
            XM Trading Platform - Professional Graph Layout Reference
        </p>
        
        <div class="gallery">
"""

images = [
    "Screenshot_2026-02-04-23-06-11-277_com.xm.webapp.jpg",
    "Screenshot_2026-02-04-23-06-50-790_com.xm.webapp.jpg",
    "Screenshot_2026-02-04-23-09-40-660_com.xm.webapp.jpg",
    "Screenshot_2026-02-04-23-09-55-792_com.xm.webapp.jpg"
]

for i, img_name in enumerate(images, 1):
    img_path = os.path.join("scripts", img_name)
    if os.path.exists(img_path):
        # Read image and encode to base64
        with open(img_path, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
        
        html_content += f"""
            <div class="image-card">
                <img src="data:image/jpeg;base64,{img_data}" alt="Screenshot {i}">
                <div class="image-title">Screenshot {i}: {img_name}</div>
            </div>
"""

html_content += """
        </div>
        
        <div style="background: #2a2a2a; padding: 20px; border-radius: 8px; margin-top: 30px; border-left: 4px solid #00c853;">
            <h2 style="color: #00c853; margin-bottom: 15px;">📌 Key Observations:</h2>
            <ul style="line-height: 1.8; color: #ddd;">
                <li>✅ Professional candlestick charts with clear green/red coloring</li>
                <li>✅ Volume bars at the bottom showing trading activity</li>
                <li>✅ Clean dark background (#0f1419 or similar)</li>
                <li>✅ Minimal indicators (focus on price action)</li>
                <li>✅ Clear price levels on Y-axis (right side)</li>
                <li>✅ Time periods on X-axis (bottom)</li>
                <li>✅ Mobile-optimized height and proportions</li>
                <li>✅ Professional typography and spacing</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

# Write HTML file
output_path = "view_chart_references.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ HTML file created: {output_path}")
print(f"📂 Open in browser: {os.path.abspath(output_path)}")
print("\nAll 4 screenshots embedded and ready to view!")
