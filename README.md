# 🏭 کارخانه کانفیگ کلش | Clash Config Factory

[![Workflowname](https://github.com/10ium/ClashFactory/actions/workflows/main.yml/badge.svg)](https://github.com/10ium/ClashFactory/actions/workflows/main.yml)

این مخزن به صورت خودکار، فایل‌های کانفیگ پایدار و به‌روز برای **Clash** از روی لیستی از لینک‌های اشتراک (Subscription) شما می‌سازد. هدف اصلی این پروژه، داشتن کانفیگ‌هایی است که حتی در صورت از دسترس خارج شدن لینک اشتراک اصلی، همچنان فعال باقی بمانند.

---

<!-- START_LINKS -->

## 🔗 لینک‌های کانفیگ آماده (Raw)

برای استفاده، لینک‌های زیر را مستقیما در کلش کپی کنید.

* **Albania**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Albania.yaml`
* **Andorra**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Andorra.yaml`
* **Angola**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Angola.yaml`
* **Argentina**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Argentina.yaml`
* **Armenia**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Armenia.yaml`
* **Austria**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Austria.yaml`
* **Barbados**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Barbados.yaml`
* **Belarus**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Belarus.yaml`
* **Belgium**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Belgium.yaml`
* **Bhutan**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Bhutan.yaml`
* **Bolivia**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Bolivia.yaml`
* **Canada**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Canada.yaml`
* **CentralAfricanRepublic**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/CentralAfricanRepublic.yaml`
* **China**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/China.yaml`
* **Colombia**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Colombia.yaml`
* **Cyprus**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Cyprus.yaml`
* **DominicanRepublic**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/DominicanRepublic.yaml`
* **Eritrea**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Eritrea.yaml`
* **Estonia**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Estonia.yaml`
* **Ethiopia**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Ethiopia.yaml`
* **Finland**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Finland.yaml`
* **France**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/France.yaml`
* **Germany**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Germany.yaml`
* **Greece**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Greece.yaml`
* **Hungary**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Hungary.yaml`
* **Iceland**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Iceland.yaml`
* **India**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/India.yaml`
* **Iran**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Iran.yaml`
* **Italy**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Italy.yaml`
* **Japan**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Japan.yaml`
* **Laos**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Laos.yaml`
* **Latvia**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Latvia.yaml`
* **Lesotho**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Lesotho.yaml`
* **Liechtenstein**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Liechtenstein.yaml`
* **Lithuania**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Lithuania.yaml`
* **Namibia**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Namibia.yaml`
* **Netherlands**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Netherlands.yaml`
* **Norway**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Norway.yaml`
* **Romania**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Romania.yaml`
* **Russia**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Russia.yaml`
* **Spain**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/Spain.yaml`
* **UK**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/UK.yaml`
* **USA**: `https://raw.githubusercontent.com/10ium/ClashFactory/main/output/USA.yaml`

<!-- END_LINKS -->

---

## ✨ نحوه عملکرد

این سیستم تماماً خودکار است و با استفاده از **GitHub Actions** کار می‌کند. فرآیند به شرح زیر است:

1.  **خواندن قالب**: در هر بار اجرا، اسکریپت ابتدا **قالب کلی** کانفیگ شما را از فایل `template.yaml` می‌خواند.
2.  **خواندن فرمت لینک**: سپس به فایل `format.txt` مراجعه کرده و **قالب پردازش لینک** را از آنجا می‌خواند. این قالب مشخص می‌کند که لینک‌های اشتراک شما چگونه باید پردازش شوند (مثلاً با استفاده از یک سرویس مبدل).
3.  **پردازش لینک‌ها**: اسکریپت به سراغ فایل `subscriptions.txt` رفته و لینک‌های اشتراک شما را یک به یک برمی‌دارد. هر لینک را طبق فرمت مرحله قبل، پردازش کرده و **لینک نهایی** را می‌سازد.
4.  **دانلود و ذخیره محتوا**: محتوای هر لینک نهایی دانلود شده و به صورت یک فایل متنی مجزا در پوشه `providers/` ذخیره می‌شود. این کار باعث **پایداری ابدی** کانفیگ شما می‌شود.
5.  **تولید کانفیگ نهایی**: در نهایت، اسکریپت با استفاده از قالب مرحله اول، یک فایل کانفیگ کامل در پوشه `output/` می‌سازد که مستقیماً به محتوای دانلود شده در مخزن خودتان اشاره می‌کند.
6.  **به‌روزرسانی README**: این فایل `README.md` به طور خودکار با لیست جدید کانفیگ‌های تولید شده به‌روز می‌شود.

---

## 🚀 نحوه استفاده و شخصی‌سازی

شما می‌توانید این مخزن را به سادگی برای خودتان شخصی‌سازی کنید.

### ۱. افزودن لینک‌های اشتراک

فایل `subscriptions.txt` را باز کرده و لینک‌های اشتراک خود را در آن وارد کنید.

* **حالت عادی (نام خودکار):**
    ```
    [https://example.com/your-sub-link.txt](https://example.com/your-sub-link.txt)
    ```
* **با نام دلخواه (توصیه می‌شود):**
    ```
    [https://example.com/your-sub-link.txt,My-Custom-Name](https://example.com/your-sub-link.txt,My-Custom-Name)
    ```

### ۲. تغییر سرویس مبدل لینک (اختیاری)

اگر می‌خواهید از یک سرویس دیگر برای پردازش لینک‌ها استفاده کنید، فایل `format.txt` را ویرایش کنید. فقط مطمئن شوید که محل قرارگیری لینک اشتراک اصلی را با `[URL]` مشخص کرده‌اید.

**مثال `format.txt`:**
