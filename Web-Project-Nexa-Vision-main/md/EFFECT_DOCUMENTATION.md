# توثيق تأثير الجزيئات - MEGASYST

## ملخص التغييرات

تم إضافة تأثير حركة الجزيئات (Particles Animation) على قسم الرئيسية Hero Section فقط.

---

## الملفات المعدلة

### 1. ملف CSS (css/style.css)

#### التغييرات على قسم الـ Hero:
```
css
.hero {
    /* الخلفية الجديدة - تدرج لوني داكن */
    background: linear-gradient(135deg, #0a1628 0%, #1a3a8f 50%, #0d6efd 100%);
    
    /* خصائص جديدة للتنسيق */
    position: relative;
    overflow: hidden;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

/* Canvas للجزيئات */
#particles-canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
}

/* محتوى الـ Hero */
.hero-content {
    position: relative;
    z-index: 2;
}
```

---

### 2. ملف HTML (index.html)

#### الإضافات في قسم Hero:
```
html
<section class="hero" id="home">
    <!-- عنصر Canvas للجزيئات -->
    <canvas id="particles-canvas"></canvas>
    
    <!-- تغليف المحتوى -->
    <div class="hero-content">
        <h2>MEGASYST: نظام فحص الأنابيب الذكي</h2>
        <p>...</p>
        <a href="#features" class="cta-button">...</a>
    </div>
</section>
```

---

### 3. ملف JavaScript (main.js)

#### نظام الجزيئات يتضمن:

**الكلاس Particle (جزيء منفرد):**
- موقع عشوائي (x, y)
- سرعة عشوائية (vx, vy)
- نصف قطر عشوائي (1-4 بكسل)
- لون أزرق شفاف

**الكلاس ParticleSystem (نظام الجزيئات):**
- 80 جزيء تتحرك بشكل مستمر
- رسم خطوط بين الجزيئات المتقاربة (مسافة 150 بكسل)
- استجابة لحركة الماوس (توصيل حتى 200 بكسل)
- تحديث مستمر بـ requestAnimationFrame

---

## كيف يعمل التأثير؟

1. عند تحميل الصفحة، يتم إنشاء 80 جزيء
2. كل جزيء يتحرك بشكل عشوائي داخل القسم
3. عندما تقترب جزيئات من بعضها، ترسم خط يربطها
4. عند تحريك الماوس، تتصل الجزيئات بموقع الماوس
5. كل هذا يحدث بسرعة 60 إطار في الثانية

---

## لتشغيل المشروع

افتح ملف `index.html` في المتصفح وسترى التأثير على قسم الرئيسية فقط.

---

## ملاحظات

- التأثير يظهر فقط على قسم الرئيسية (Hero Section)
- باقي أقسام الموقع (الميزات، التقنية، الفوتر) بدون تغيير
- الخلفية تغيرت من صورة إلى تدرج لوني داكن
