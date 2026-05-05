# شرح الانيميشن - MEGASYST

## الانيميشن المضافة

---

## 1. انيميشن الـ Header (الترويسة)

### slideDown Animation
```
css
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
- عند تحميل الصفحة، القائمة تنزلق من الأعلى
- مدة الانيميشن: 0.8 ثانية

---

## 2. انيميشن الـ Logo

### logoPulse Animation
```
css
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
- الأيقونة تضء وتنبض بشكل مستمر
- تأثير التوهج الأزرق
- مدة التكرار: 2 ثانية

---

## 3. انيميشن روابط القائمة

### navLinkFade Animation
```
css
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
- الروابط تظهر واحدة تلو الأخرى
- تأخير لكل رابط (0.1s, 0.2s, 0.3s...)

### Hover Animation
```
css
#navbar li a::before {
    content: '';
    position: absolute;
    width: 0;
    height: 2px;
    bottom: 0;
    left: 50%;
    background: linear-gradient(90deg, #4dabf7, #c5f6fa);
    transition: all 0.3s ease;
    transform: translateX(-50%);
}

#navbar li a:hover::before {
    width: 100%;
}
```
- عند مرور الماوس، خط يمتد من اليسار لليمين
- تدرج لوني جميل

---

## 4. انيميشن زر القائمة (موبايل)

```
css
#bar:hover {
    transform: rotate(90deg);
    color: #c5f6fa;
}
```
- أيقونة القائمة تدور عند اللمس

---

## 5. انيميشن الـ Hero Section

### heroTitleFade
- العنوان ينزلق من الأسفل

### heroTextFade
- النص يظهر بتأخير 0.3 ثانية

### buttonFadeIn
- الزر يظهر بتأخير 0.6 ثانية
- يبدأ شفاف ثم يظهر

---

## 6. انيميشن الـ Footer

### waveGradient
```
css
@keyframes waveGradient {
    0% {
        background-position: 0% 50%;
    }
    100% {
        background-position: 200% 50%;
    }
}
```
- شريط ملون يتحرك بشكل مستمر في أعلى الفوتر
- تدرج لوني يتحرك من اليمين لليسار

### footerFadeIn
- الفوتر整体的 ينزلق من الأسفل عند التحميل

### Link Hover
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
- خط يمتد تحت الرابط
- الرابط يرتفع قليلاً

---

## ملخص الانيميشنات

| العنصر | الانيميشن | المدة |
|--------|-----------|-------|
| Header | slideDown | 0.8s |
| Logo | pulse | 2s (تكرار) |
| Nav Links | fadeIn + hover | 0.5s |
| Hero Title | fadeIn + slideUp | 1s |
| Hero Text | fadeIn + slideUp | 1s |
| CTA Button | fadeIn | 1s |
| Feature Icons | rotate + scale | 0.3s |
| Tech Items | slideUp | 0.3s |
| Footer | fadeIn + wave | 1s + تكرار |
| Footer Links | slideUp + line | 0.3s |

---

## تشغيل الانيميشنات

افتح index.html في المتصفح وشاهد الانيميشنات تعمل تلقائياً عند:
1. تحميل الصفحة
2. تمرير الماوس على الروابط
3. تمرير الماوس على أزرار التواصل
