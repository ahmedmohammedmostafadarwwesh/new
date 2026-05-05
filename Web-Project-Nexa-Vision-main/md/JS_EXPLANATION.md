# شرح JavaScript سطر بسطر

## ملف main.js - شرح مفصل

---

## الجزء الأول: القائمة المتحركة للموبايل

```
javascript
// Mobile menu toggle
const bar = document.getElementById("bar");
const navbar = document.getElementById("navbar");

if (bar) {
  bar.addEventListener("click", () => {
    navbar.classList.toggle("active");
  });
}
```

**الشرح:**
- `const bar` - متغير يخزن عنصر أيقونة القائمة (ثلاث شرائط)
- `const navbar` - متغير يخزن قائمة التنقل
- `addEventListener("click", ...)` - عند الضغط على الأيقونة
- `toggle("active")` - إضافة/إزالة كلاس "active" للقائمة

---

## الجزء الثاني: التمرير السلس

```
javascript
// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
      });
    }
  });
});
```

**الشرح:**
- `querySelectorAll('a[href^="#"]')` - اختيار كل الروابط التي تبدأ بـ #
- `forEach` - لكل رابط
- `e.preventDefault()` - منع السلوك الافتراضي (القفلة)
- `scrollIntoView({ behavior: "smooth" })` - تمرير سلس للموقع

---

## الجزء الثالث: تحديد الرابط النشط

```
javascript
// Active link highlighting on scroll
const sections = document.querySelectorAll("section[id]");
const navLinks = document.querySelectorAll("#navbar li a");

window.addEventListener("scroll", () => {
  let current = "";

  sections.forEach((section) => {
    const sectionTop = section.offsetTop;
    const sectionHeight = section.clientHeight;
    if (scrollY >= sectionTop - 200) {
      current = section.getAttribute("id");
    }
  });

  navLinks.forEach((link) => {
    link.classList.remove("active");
    if (link.getAttribute("href") === "#" + current) {
      link.classList.add("active");
    }
  });
});
```

**الشرح:**
- `sections` - كل أقسام الصفحة التي لها id
- `navLinks` - روابط القائمة
- `addEventListener("scroll", ...)` - عند تمرير الصفحة
- `section.offsetTop` - موقع القسم من الأعلى
- إذا كان التمرير عند القسم، نضيف له class "active"

---

## الجزء الرابع: كلاس الجزيء (Particle)

```
javascript
class Particle {
  constructor(canvas) {
    this.canvas = canvas;
    this.x = Math.random() * canvas.width;  // موقع عشوائي أفقي
    this.y = Math.random() * canvas.height; // موقع عشوائي عمودي
    this.vx = (Math.random() - 0.5) * 2;    // سرعة أفقية عشوائية
    this.vy = (Math.random() - 0.5) * 2;    // سرعة عمودية عشوائية
    this.radius = Math.random() * 3 + 1;    // حجم عشوائي (1-4)
    this.color = `rgba(77, 171, 247, ${Math.random() * 0.5 + 0.3})`; // لون أزرق شفاف
    this.connected = false;
  }

  update() {
    this.x += this.vx;  // تحريك أفقي
    this.y += this.vy;  // تحريك عمودي

    // ارتداد عند الحواف
    if (this.x < 0 || this.x > this.canvas.width) this.vx *= -1;
    if (this.y < 0 || this.y > this.canvas.height) this.vy *= -1;
  }

  draw(ctx) {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.fill();
  }
}
```

**الشرح:**
- `constructor` - دالة البناء، تحدد الخصائص الأولية
- `this.x`, `this.y` - الإحداثيات
- `this.vx`, `this.vy` - السرعة (velocities)
- `Math.random()` - رقم عشوائي بين 0 و 1
- `update()` - تحديث الموقع في كل إطار
- `draw()` - رسم الدائرة على الكانفاس

---

## الجزء الخامس: كلاس نظام الجزيئات

```
javascript
class ParticleSystem {
  constructor() {
    this.canvas = document.getElementById("particles-canvas");
    if (!this.canvas) return;
    
    this.ctx = this.canvas.getContext("2d");
    this.particles = [];
    this.mouseX = null;
    this.mouseY = null;
    this.particleCount = 80;      // عدد الجزيئات
    this.connectionDistance = 150; // مسافة الربط بين الجزيئات

    this.init();
    this.animate();
    
    window.addEventListener("resize", () => this.resize());
    this.canvas.addEventListener("mousemove", (e) => this.handleMouseMove(e));
  }
```

**الشرح:**
- `getContext("2d")` - الحصول على سياق الرسم ثنائي الأبعاد
- `particles` - مصفوفة لتخزين الجزيئات
- `mouseX`, `mouseY` - موقع الماوس
- `particleCount = 80` - 80 جزيء
- `connectionDistance = 150` - ربط الجزيئات إذا كانت المسافة أقل من 150px
- `init()` - تهيئة النظام
- `animate()` - بدء الحركة
- `resize` - تحديث الحجم عند تغيير نافذة المتصفح
- `mousemove` - تتبع حركة الماوس

---

## الجزء السادس: دوال التهيئة

```
javascript
  init() {
    this.resize();
    this.createParticles();
  }

  resize() {
    const hero = document.querySelector(".hero");
    if (hero) {
      this.canvas.width = hero.offsetWidth;
      this.canvas.height = hero.offsetHeight;
    }
  }

  createParticles() {
    this.particles = [];
    for (let i = 0; i < this.particleCount; i++) {
      this.particles.push(new Particle(this.canvas));
    }
  }
```

**الشرح:**
- `init()` - استدعاء resize و createParticles
- `resize()` - جعل Canvas بنفس حجم قسم Hero
- `createParticles()` - إنشاء 80 جزيء وتخزينهم في المصفوفة

---

## الجزء السابع: التعامل مع الماوس

```
javascript
  handleMouseMove(e) {
    const rect = this.canvas.getBoundingClientRect();
    this.mouseX = e.clientX - rect.left;
    this.mouseY = e.clientY - rect.top;
  }
```

**الشرح:**
- `getBoundingClientRect()` - الحصول على موقع Canvas في الصفحة
- `clientX - rect.left` - حساب موقع الماوس داخل Canvas

---

## الجزء الثامن: رسم الخطوط بين الجزيئات

```
javascript
  drawConnections() {
    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const dx = this.particles[i].x - this.particles[j].x;
        const dy = this.particles[i].y - this.particles[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < this.connectionDistance) {
          const opacity = 1 - distance / this.connectionDistance;
          this.ctx.beginPath();
          this.ctx.strokeStyle = `rgba(77, 171, 247, ${opacity * 0.4})`;
          this.ctx.lineWidth = 1;
          this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
          this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
          this.ctx.stroke();
        }
      }
    }
  }
```

**الشرح:**
- `for` مزدوج - مقارنة كل جزيء مع كل الجزيئات الأخرى
- `dx`, `dy` - الفرق في الإحداثيات
- `distance` - المسافة باستخدام نظرية فيثاغورس
- إذا المسافة < 150: ارسم خط
- `opacity` - كلما زادت المسافة، ضعف الخط (تأثير جميل)
- `strokeStyle` - لون الخط بأزرق مع شفافية

---

## الجزء التاسع: رسم خطوط الماوس

```
javascript
  drawMouseConnections() {
    if (this.mouseX === null || this.mouseY === null) return;

    this.particles.forEach((particle) => {
      const dx = particle.x - this.mouseX;
      const dy = particle.y - this.mouseY;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < 200) {
        const opacity = 1 - distance / 200;
        this.ctx.beginPath();
        this.ctx.strokeStyle = `rgba(255, 255, 255, ${opacity * 0.6})`;
        this.ctx.lineWidth = 2;
        this.ctx.moveTo(particle.x, particle.y);
        this.ctx.lineTo(this.mouseX, this.mouseY);
        this.ctx.stroke();
      }
    });
  }
```

**الشرح:**
- نفس المنطق السابق لكن مع الماوس
- مسافة الربط 200 بكسل
- لون الخط أبيض (ليس أزرق)因为他 يتفاعل مع الماوس

---

## الجزء العاشر: دالة الحركة

```
javascript
  animate() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    // Update and draw particles
    this.particles.forEach((particle) => {
      particle.update();
      particle.draw(this.ctx);
    });

    // Draw connections between particles
    this.drawConnections();

    // Draw connections to mouse
    this.drawMouseConnections();

    requestAnimationFrame(() => this.animate());
  }
}
```

**الشرح:**
- `clearRect` - مسح الكانفاس في كل إطار
- تحديث ورسم كل الجزيئات
- رسم الخطوط بين الجزيئات
- رسم خطوط الماوس
- `requestAnimationFrame` - طلب الإطار التالي (60fps)

---

## الجزء الأخير: تشغيل النظام

```
javascript
// Initialize particle system when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  new ParticleSystem();
});
```

**الشرح:**
- `DOMContentLoaded` - عند تحميل HTML بالكامل
- `new ParticleSystem()` - إنشاء كائن جديد من كلاس النظام
- هذا يبدأ التأثير تلقائياً

---

## ملخص طريقة العمل:

1. **إنشاء Canvas** - منطقة للرسم
2. **إنشاء 80 جزيء** - كل واحد له موقع وسرعة عشوائية
3. **تحديث الموقع** - في كل إطار (60 مرة في الثانية)
4. **رسم الجزيئات** - ك دوائر زرقاء
5. **رسم الخطوط** - إذا كانت المسافة قريبة
6. **التفاعل مع الماوس** - خطوط تتصل بالمؤشر
7. **تكرار** - بشكل مستمر forever
