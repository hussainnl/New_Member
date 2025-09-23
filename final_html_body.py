# 5. محتوى البريد الإلكتروني (HTML)
# استخدم {file_name} و {file_link} كمتغيرات سيتم استبدالها لاحقًا
EMAIL_HTML_BODY = """
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {{
      font-family: 'Arial', sans-serif;
      background-color: #fdfaf3;
      color: #333333;
      margin: 0;
      padding: 0;
    }}
    .container {{
      max-width: 600px;
      margin: auto;
      background: #ffffff;
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
    .header {{
      text-align: center;
      border-bottom: 3px solid #f7931e;
      padding-bottom: 15px;
      margin-bottom: 20px;
    }}
    .header img {{
      width: 80px;
    }}
    .header h1 {{
      color: #1d4e89;
      font-size: 22px;
      margin-top: 10px;
    }}
    p {{
      line-height: 1.6;
      font-size: 15px;
    }}
    a.button {{
      display: inline-block;
      margin: 10px 0;
      padding: 12px 20px;
      background: #1d4e89;
      color: #ffffff;
      text-decoration: none;
      border-radius: 8px;
      font-weight: bold;
    }}
    a.button:hover {{
      background: #14507d;
    }}
    .footer {{
      margin-top: 30px;
      font-size: 13px;
      color: #666666;
      text-align: center;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <img src="https://avatars.githubusercontent.com/u/230738679?s=400&u=64d3db5100ec6d5bef5a0457a2e13bc3c8242dd3&v=4" alt="Nawaa Logo">
      <h1>فريق نواة</h1>
    </div>

    <p dir="rtl" style="text-align:right;">أهلاً {name},</p>
    <p dir="rtl" style="text-align:right;">
        التقييم معمول على خطة مدتها <strong>6 أيام</strong>.<br><br>
        خلال الفترة دي:<br>
        • كل يوم هتكتب الساعات اللي اشتغلت فيها على نفسك.<br>
        • في آخر اليوم، هتدي لنفسك تقييم بسيط.<br>
        • وبعد ما الـ 6 أيام يخلصوا، هيوصلك تقرير يوضح قد إيه كنت ملتزم، وعلى الأساس ده بيتحدد موقفك.<br>
    </p>

    <p dir="rtl" style="text-align:right;">ده ملف التقييم بتاعك:</p>  
    <div style="text-align:right;">
        <a class="button" href="{file_link}">{file_name}</a>  
    </div>

    <p dir="rtl" style="text-align:right;">شرح المهمات وطريقة استخدام الملف هتلاقيه في قسم المهمات:</p>
    <div style="text-align:right;">
        <a class="button" href="{tasks_link}">الذهاب لقسم المهمات</a> 
    </div>

    <p dir="rtl" style="text-align:right;">وكمان تقدر تنضم للمجموعة الرئيسية للمشروع، ولو محتاج مساعدة أو عندك أي سؤال، إسأل على طول:</p>
    <div style="text-align:right;">
        <a class="button" href="{support_asking_link}">انضم دلوقتي</a> 
    </div>

    <p dir="rtl" style="text-align:right;">خلينا نشوف شغلك ونكمل الرحلة سوا 🚀</p>

    <div class="footer">
      <p>© 2025 نواة – رحلتك للتطور تبدأ من هنا</p>
    </div>
  </div>
</body>
</html>
"""

PASS_HTML_BODY = """
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {{
      font-family: 'Arial', sans-serif;
      background-color: #fdfaf3;
      color: #333333;
      margin: 0;
      padding: 0;
    }}
    .container {{
      max-width: 600px;
      margin: auto;
      background: #ffffff;
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
    .header {{
      text-align: center;
      border-bottom: 3px solid #f7931e; /* برتقالي */
      padding-bottom: 15px;
      margin-bottom: 20px;
    }}
    .header img {{
      width: 80px;
    }}
    .header h1 {{
      color: #1d4e89; /* الأزرق */
      font-size: 22px;
      margin-top: 10px;
    }}
    p {{
      line-height: 1.6;
      font-size: 15px;
    }}
    a.button {{
      display: inline-block;
      margin: 20px 0;
      padding: 14px 24px;
      background: #1d4e89; /* الأزرق */
      color: #ffffff;
      text-decoration: none;
      border-radius: 8px;
      font-weight: bold;
      font-size: 16px;
    }}
    a.button:hover {{
      background: #14507d;
    }}
    .footer {{
      margin-top: 30px;
      font-size: 13px;
      color: #666666;
      text-align: center;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <!-- ضع رابط اللوجو هنا -->
      <img src="https://avatars.githubusercontent.com/u/230738679?s=400&u=64d3db5100ec6d5bef5a0457a2e13bc3c8242dd3&v=4" alt="Nawaa Logo">
      <h1>فريق نواة</h1>
    </div>

    <p dir="rtl" style="text-align:right;">مرحباً {name},</p>
    <p dir="rtl" style="text-align:right;">
      🎉 مبروك! تم قبولك رسميًا للانضمام إلى <strong>فريق نواة</strong>.<br>
      رحلتك معنا بدأت الآن، ومستنيين نشوف إبداعك ومساهمتك في بناء المستقبل 🌱
    </p>

    <div style="text-align:center;">
        <a class="button" href="{pass_state_link}">انضم إلى الفريق</a>  
    </div>

    <div class="footer">
      <p>© 2025 نواة – معًا نحو التغيير</p>
    </div>
  </div>
</body>
</html>
"""

NOT_PASS_HTML_BODY = """
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {{
      font-family: 'Arial', sans-serif;
      background-color: #fdfaf3;
      color: #333333;
      margin: 0;
      padding: 0;
    }}
    .container {{
      max-width: 600px;
      margin: auto;
      background: #ffffff;
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
    .header {{
      text-align: center;
      border-bottom: 3px solid #f7931e; /* برتقالي */
      padding-bottom: 15px;
      margin-bottom: 20px;
    }}
    .header img {{
      width: 80px;
    }}
    .header h1 {{
      color: #1d4e89; /* الأزرق */
      font-size: 22px;
      margin-top: 10px;
    }}
    p {{
      line-height: 1.6;
      font-size: 15px;
    }}
    a.button {{
      display: inline-block;
      margin: 20px 0;
      padding: 14px 24px;
      background: #1d4e89; /* الأزرق */
      color: #ffffff;
      text-decoration: none;
      border-radius: 8px;
      font-weight: bold;
      font-size: 16px;
    }}
    a.button:hover {{
      background: #d87c16;
    }}
    .footer {{
      margin-top: 30px;
      font-size: 13px;
      color: #666666;
      text-align: center;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <!-- ضع رابط اللوجو هنا -->
      <img src="https://avatars.githubusercontent.com/u/230738679?s=400&u=64d3db5100ec6d5bef5a0457a2e13bc3c8242dd3&v=4" alt="Nawaa Logo">
      <h1>فريق نواة</h1>
    </div>

    <p dir="rtl" style="text-align:right;">مرحباً {name},</p>
    <p dir="rtl" style="text-align:right;">
      شكرًا جدًا على التزامك ومجهودك في فترة التقييم 🙏 <br>
      بعد المراجعة، حابّين نقولك إنك المرة دي<strong>ما اتقبلتش في المرحلة دي.</strong>.  
    </p>

    <p dir="rtl" style="text-align:right;">
    بس خليك فاكر ده مش آخر الطريق 🚀، بالعكس! تقدر تقدّم تاني قدّام بعد ما تجهز نفسك أكتر
    . وإحنا واثقين إن المحاولات المتكررة هي اللي بتعمل النجاح 🌱
    </p>

    <div style="text-align:center;">
        <a class="button" href="{pass_state_link}">قدّم مرة أخرى</a>  
    </div>

    <div class="footer">
      <p>© 2025 نواة – مع كل محاولة، خطوة أقرب للنجاح</p>
    </div>
  </div>
</body>
</html>
"""
