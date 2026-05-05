# شرح CSS الانيميشن سطر بسطر

## ملف css/style.css - شرح مفصل

---

## الجزء الأول: انيميشن الترويسة (Header)

### 1. نزول الترويسة عند التحميل

```
css
#header {
    /* ... باقي الخصائص ... */
    animation: headerSlideDown 0.8s ease-out;
}

@keyframes headerSlideDown {
    from {
        transform: translateY(-100%);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}
```

**الشرح:**
- `animation` - خاصية الانيميشن في CSS
- `headerSlideDown` - اسم الانيميشن الذي سنعرّفه
- `0.8s` - مدة الانيميشن (ثانية ونصف إلا ربع)
- `ease-out` - نوع الحركة (تبطيء في النهاية)
- `@keyframes` - تعريف الانيميشن
- `from` - البداية (من عند)
- `to` - النهاية (إلى)
- `translateY(-100%)` - تحريك للأعلى 100%
- `opacity: 0` - شفافية كاملة (مخفي)

**النتيجة:** الترويسة تنزلق من فوق وتظهر

---

## الجزء الثاني: انيميشن الأيقونة (Logo)

### 2. نبض الأيقونة

```
css
.logo i {
    font-size: 2.5rem;
    color: #4dabf7;
    animation: logoPulse 2s infinite;
}

@keyframes logoPulse {
    0%, 100% {
        transform: scale(1);
        text-shadow: 0 0 10px rgba(77, 171, 247, 0.5);
    }
    50% {
        transform: scale(1.1);
        text-shadow: 0 0 20px rgba(77, 171, 247, 0.8);
    }
}
```

**الشرح:**
- `infinite` - تكرار لا نهائي
- `0%, 100%` - البداية والنهاية
- `50%` - في منتصف الانيميشن
- `transform: scale(1.1)` - تكبير بنسبة 10%
- `text-shadow` - ظل النص (توهج)
- `rgba(77, 171, 247, 0.5)` - لون أزرق مع شفافية 50%

**النتيجة:** الأيقونة تكبر وتصغر مع توهج

---

## الجزء الثالث: روابط القائمة

### 3. ظهور الروابط واحدة تلو الأخرى

```
css
#navbar li a {
    /* ... باقي الخصائص ... */
    animation: navLinkFade 0.5s ease forwards;
    opacity: 0;
}

@keyframes navLinkFade {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

**الشرح:**
- `forwards` - الاحتفاظ بالحالة النهائية
- `opacity: 0` - يبدأ مخفي
- `translateY(-20px)` - يبدأ أعلى بـ 20 بكسل

### 4. تأخير ظهور كل رابط

```
css
#navbar li:nth-child(1) a { animation-delay: 0.1s; }
#navbar li:nth-child(2) a { animation-delay: 0.2s; }
#navbar li:nth-child(3) a { animation-delay: 0.3s; }
#navbar li:nth-child(4) a { animation-delay: 0.4s; }
#navbar li:nth-child(5) a { animation-delay: 0.5s; }
```

**الشرح:**
- `nth-child(n)` - اختيار العنصر رقم n
- `animation-delay` - تأخير البداية

**النتيجة:** الروابط تظهر واحدة تلو الأخرى

### 5. خط يمتد تحت الرابط

```
css
#navbar li a::before {
    content: '';
    position: absolute;
    width: 0;              /* يبدأ بعرض 0 */
    height: 2px;
    bottom: 0;
    left: 50%;
    background: linear-gradient(90deg, #4dabf7, #c5f6fa);
    transition: all 0.3s ease;
    transform: translateX(-50%);
}

#navbar li a:hover::before {
    width: 100%;           /* يصبح عرض 100% */
}
```

**الشرح:**
- `::before` - عنصر زائف قبل المحتوى
- `position: absolute` - موقع ثابت
- `width: 0` - يبدأ بدون عرض
- `linear-gradient` - تدرج لوني
- `transition` - انتقالات سلسة
- `:hover` - عند مرور الماوس

**النتيجة:** خط يمتد من اليسار لليمين عند Hover

---

## الجزء الرابع: زر القائمة (موبايل)

```
css
#bar:hover {
    transform: rotate(90deg);
    color: #c5f6fa;
}
```

**الشرح:**
- `rotate(90deg)` - دوران 90 درجة

**النتيجة:** أيقونة“三个-lines” تدور عند اللمس

---

## الجزء الخامس: انيميشن الـ Hero

### 6. عنوان Hero

```
css
.hero h2 {
    animation: heroTitleFade 1s ease-out;
}

@keyframes heroTitleFade {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

### 7. نص Hero

```
css
.hero p {
    animation: heroTextFade 1s ease-out 0.3s forwards;
    opacity: 0;
}
```

- `0.3s` - تأخير 0.3 ثانية

### 8. الزر

```
css
.cta-button {
    animation: buttonFadeIn 1s ease-out 0.6s forwards;
    opacity: 0;
}
```

---

## الجزء السادس: انيميشن الـ Footer

### 9. الخلفية

```
css
footer {
    background: linear-gradient(135deg, #0a1628 0%, #1a3a8f 50%, #0d6efd 100%);
}
```

- تدرج لوني من أزرق داكن لأزرق فاتح

### 10. الشريط المتحرك في الأعلى

```
css
footer::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 5px;
    background: linear-gradient(90deg, #0d6efd, #4dabf7, #0d6efd);
    background-size: 200% 100%;
    animation: waveGradient 3s linear infinite;
}

@keyframes waveGradient {
    0% {
        background-position: 0% 50%;
    }
    100% {
        background-position: 200% 50%;
    }
}
```

**الشرح:**
- `::before` - عنصر زائف قبل محتوى الفوتر
- `background-size: 200% 100%` - ضعف عرض الخلفية
- `linear` - سرعة ثابتة
- `background-position` - موقع الخلفية يتحرك

**النتيجة:** شريط ملون يتحرك من اليمين لليسار باستمرار

### 11. دخول الفوتر

```
css
footer {
    animation: footerFadeIn 1s ease-out;
}

@keyframes footerFadeIn {
    from {
        opacity: 0;
        transform: translateY(50px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

### 12. روابط الفوتر

```
css
.footer-links a::after {
    content: '';
    position: absolute;
    width: 0;
    height: 2px;
    bottom: -2px;
    left: 0;
    background: #c5f6fa;
    transition: width 0.3s ease;
}

.footer-links a:hover::after {
    width: 100%;
}

.footer-links a:hover {
    transform: translateY(-2px);
}
```

---

## ملخص الخصائص المستخدمة

| الخاصية | معناها |
|---------|--------|
| `animation` | تشغيل الانيميشن |
| `@keyframes` | تعريف الانيميشن |
| `from` / `to` | البداية / النهاية |
| `0%` / `50%` / `100%` | نسب مئوية للزمن |
| `transform` | تحويل (تدوير، تكبير، تحريك) |
| `opacity` | الشفافية (0 = مخفي، 1 = ظاهر) |
| `transition` | انتقالات سلسة |
| `::before` / `::after` | عناصر زائفة |
| `infinite` | تكرار لا نهائي |
| `ease` / `linear` | أنواع الحركة |

---

## كيف يعمل انيميشن CSS؟

1. **التعريف** - نعرّف الانيميشن بـ `@keyframes`
2. **التطبيق** - نطبقه على العنصر بـ `animation`
3. **التفاعل** - نستخدم `:hover` للتفاعل مع الماوس

```
@keyframes اسم_الانيميشن {
    من_الحالة {
        خصائص
    }
    إلى_الحالة {
        خصائص
    }
}
```

---

## لتشغيل المشروع

افتح `index.html` في المتصفح ستعمل كل الانيميشنات تلقائياً!
