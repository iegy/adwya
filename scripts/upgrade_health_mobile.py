from pathlib import Path
from html import escape
from datetime import date
import json, re, shutil

ROOT = Path('.')
SITE = 'https://iegy.net/adwya'
TODAY = '2026-08-29'

articles = [
  {
    'slug':'healthy-diet','cat':'تغذية','title':'أساسيات التغذية الصحية المتوازنة','desc':'كيف تبني نظامًا غذائيًا متنوعًا ومتوازنًا بدون تعقيد، وفق مبادئ منظمة الصحة العالمية.','lead':'الغذاء الصحي ليس قائمة ممنوعات ثابتة؛ الأساس هو الكفاية والتوازن والاعتدال والتنوع، مع الاعتماد أكثر على الأطعمة قليلة التصنيع.','points':[
      'اجعل الخضار والفواكه والبقول والحبوب الكاملة جزءًا ثابتًا من نمط أكلك.',
      'وازن كمية الطاقة التي تتناولها مع احتياجاتك ونشاطك بدل الاعتماد على حمية قصيرة المدى.',
      'قلل الأطعمة والمشروبات الغنية بالسكريات الحرة والصوديوم والدهون غير الصحية.',
      'نوّع مصادر البروتين بين البقول والأسماك والبيض واللحوم قليلة الدهون بحسب احتياجاتك.'
    ],
    'note':'الاحتياجات تختلف حسب العمر والنشاط والحالة الصحية، لذلك لا توجد خطة واحدة مناسبة للجميع.',
    'sources':[('منظمة الصحة العالمية — Healthy diet','https://www.who.int/news-room/fact-sheets/detail/healthy-diet'),('WHO/FAO — What are healthy diets?','https://www.who.int/publications/i/item/9789240101876')]
  },
  {
    'slug':'fruit-vegetables-fiber','cat':'تغذية','title':'الخضار والفواكه والألياف: لماذا هي مهمة؟','desc':'دليل عملي لزيادة الخضار والفواكه والألياف الغذائية يوميًا بصورة بسيطة ومتدرجة.','lead':'توصي منظمة الصحة العالمية لمن هم أكبر من 10 سنوات بما لا يقل عن 400 جرام من الخضار والفواكه يوميًا، مع استهداف 25 جرامًا على الأقل من الألياف الطبيعية من الطعام.','points':[
      'وزّع الخضار والفواكه على وجبات اليوم بدل محاولة تناول الكمية مرة واحدة.',
      'اختر الحبوب الكاملة والبقول مثل العدس والفول والحمص لرفع كمية الألياف.',
      'الفاكهة الكاملة عادة أفضل من العصير لأنها تحتفظ بالألياف وتشبع أكثر.',
      'زد الألياف تدريجيًا واشرب سوائل كافية حتى لا تسبب الزيادة المفاجئة انزعاجًا هضميًا.'
    ],
    'note':'الأطفال الأصغر لهم احتياجات مختلفة، وبعض أمراض الجهاز الهضمي قد تحتاج تعديل كمية الألياف بإرشاد مختص.',
    'sources':[('منظمة الصحة العالمية — Healthy diet','https://www.who.int/news-room/fact-sheets/detail/healthy-diet')]
  },
  {
    'slug':'salt-blood-pressure','cat':'صحة عامة','title':'الملح وضغط الدم: أين المشكلة؟','desc':'كيف يرتبط الإفراط في الملح بضغط الدم وما الخطوات العملية لتقليل الصوديوم في الطعام.','lead':'النظام الغذائي المرتفع بالملح من العوامل التي تزيد احتمال ارتفاع ضغط الدم، وارتفاع الضغط غالبًا لا يسبب أعراضًا واضحة.','points':[
      'خفف إضافة الملح أثناء الطبخ وعلى المائدة تدريجيًا حتى تتكيف حاسة التذوق.',
      'انتبه للأطعمة المصنعة والمخللات والصلصات والوجبات الجاهزة لأنها قد تحتوي صوديومًا مرتفعًا.',
      'قارن الملصقات الغذائية واختر المنتج الأقل صوديومًا عندما تتوفر بدائل متقاربة.',
      'قياس ضغط الدم مهم لأن الاعتماد على الأعراض وحدها لا يكشف ارتفاع الضغط.'
    ],
    'note':'من يتناول أدوية ضغط أو لديه مرض كلوي أو قلبي يجب أن يتبع تعليمات فريقه الطبي، خصوصًا فيما يتعلق بالصوديوم والبوتاسيوم.',
    'sources':[('NHS — High blood pressure','https://www.nhs.uk/conditions/high-blood-pressure/'),('منظمة الصحة العالمية — Healthy diet','https://www.who.int/news-room/fact-sheets/detail/healthy-diet')]
  },
  {
    'slug':'free-sugars','cat':'تغذية','title':'السكريات الحرة والمضافة: كيف تقللها بذكاء؟','desc':'فهم السكريات الحرة والمضافة وتقليلها بدون حرمان مبالغ فيه.','lead':'توصي منظمة الصحة العالمية بأن تكون السكريات الحرة أقل من 10% من الطاقة اليومية، وقد توجد فائدة إضافية عند خفضها إلى 5% أو أقل.','points':[
      'ابدأ بالمشروبات المحلاة لأنها من أسهل مصادر السكر التي يمكن خفضها.',
      'اقرأ قائمة المكونات لأن السكر قد يظهر بأسماء مختلفة أو في منتجات لا تتوقعها.',
      'اختر الفاكهة الكاملة بدل الاعتماد المتكرر على العصائر حتى غير المضاف لها سكر.',
      'قلل السكر تدريجيًا في الشاي والقهوة والحلويات المنزلية بدل التغيير الحاد إذا كان ذلك أسهل للاستمرار.'
    ],
    'note':'العسل والشراب المركز وعصائر الفاكهة تدخل ضمن مصادر السكريات الحرة وفق تعريف منظمة الصحة العالمية.',
    'sources':[('منظمة الصحة العالمية — Healthy diet','https://www.who.int/news-room/fact-sheets/detail/healthy-diet')]
  },
  {
    'slug':'healthy-fats','cat':'تغذية','title':'الدهون الصحية والدهون التي تحتاج تقليلها','desc':'الفرق بين الدهون غير المشبعة والمشبعة والمتحولة وكيف تختار مصادر دهون أفضل.','lead':'جودة الدهون مهمة بقدر كميتها؛ منظمة الصحة العالمية تفضّل الدهون غير المشبعة وتوصي بالحد من الدهون المشبعة وتجنب الدهون المتحولة الصناعية.','points':[
      'اختر المكسرات والبذور والأسماك والأفوكادو والزيوت النباتية غير المهدرجة كمصادر شائعة للدهون غير المشبعة.',
      'قلل الاعتماد المتكرر على الأطعمة المقلية والمخبوزات والوجبات شديدة التصنيع.',
      'استبدل جزءًا من الدهون المشبعة بمصادر دهون غير مشبعة بدل مجرد إضافة دهون جديدة للنظام.',
      'اجعل طريقة الطهي جزءًا من الاختيار: الشوي أو السلق أو الطهي بالبخار قد يقلل الحاجة للدهون المضافة.'
    ],
    'note':'توصي WHO بألا تتجاوز الدهون المشبعة 10% من الطاقة والدهون المتحولة 1% من الطاقة اليومية.',
    'sources':[('منظمة الصحة العالمية — Healthy diet','https://www.who.int/news-room/fact-sheets/detail/healthy-diet')]
  },
  {
    'slug':'protein-basics','cat':'تغذية','title':'البروتين: الكمية ليست كل شيء','desc':'اختيار مصادر بروتين متنوعة وفهم دور البروتين دون إفراط غير ضروري.','lead':'البروتين ضروري لبناء وصيانة أنسجة الجسم، لكن الاحتياج يختلف حسب العمر والوزن والنشاط والحالة الصحية.','points':[
      'نوّع بين البقول والبيض والأسماك والدواجن واللحوم ومنتجات الألبان وفق ما يناسبك.',
      'مصادر البروتين النباتي مثل العدس والفول والحمص تضيف أليافًا وعناصر غذائية أخرى.',
      'ليس كل شخص بحاجة لمساحيق البروتين أو كميات مرتفعة جدًا من البروتين.',
      'الرياضيون وبعض المراحل العمرية قد تكون احتياجاتهم أعلى، ويفضل حسابها بشكل فردي عند الحاجة.'
    ],
    'note':'الإفراط في البروتين قد لا يكون مناسبًا لبعض مرضى الكلى أو الحالات الطبية الأخرى؛ استشر مختصًا عند وجود مرض مزمن.',
    'sources':[('منظمة الصحة العالمية — Healthy diet','https://www.who.int/news-room/fact-sheets/detail/healthy-diet')]
  },
  {
    'slug':'hydration','cat':'صحة عامة','title':'الماء والترطيب: احتياجاتك ليست رقمًا ثابتًا','desc':'علامات الترطيب والجفاف وكيف تتعامل مع السوائل بطريقة عملية وآمنة.','lead':'احتياج السوائل يختلف حسب العمر والوزن والنشاط والجو والحالة الصحية، كما أن جزءًا من الماء يأتي من الطعام وليس المشروبات فقط.','points':[
      'اشرب بانتظام خلال اليوم وخصوصًا مع الحر والنشاط البدني والمرض المصحوب بفقد سوائل.',
      'العطش وجفاف الفم والبول الداكن والدوخة قد تكون علامات على نقص السوائل.',
      'الماء خيار جيد بدون سعرات أو سكر مضاف، ويمكن أن تساهم أطعمة غنية بالماء في الترطيب.',
      'القيء أو الإسهال الشديد قد يحتاجان محلول إماهة فموي وتقييمًا طبيًا بحسب شدة الأعراض.'
    ],
    'note':'بعض أمراض القلب والكلى تتطلب أحيانًا تقييد السوائل؛ لا تطبق نصائح عامة على هذه الحالات دون توجيه طبي.',
    'sources':[('MedlinePlus — Water in diet','https://www.medlineplus.gov/ency/article/002471.htm'),('MedlinePlus — Dehydration','https://medlineplus.gov/dehydration.html')]
  },
  {
    'slug':'physical-activity','cat':'نمط حياة','title':'النشاط البدني للبالغين: هدف واقعي يمكن تقسيمه','desc':'كمية الحركة الأسبوعية الموصى بها وكيف تبدأ وتستمر بدون خطة معقدة.','lead':'توصي إرشادات CDC للبالغين بما لا يقل عن 150 دقيقة من النشاط متوسط الشدة أسبوعيًا، مع يومين على الأقل لتمارين تقوية العضلات.','points':[
      'يمكن تقسيم 150 دقيقة على فترات قصيرة خلال الأسبوع؛ ليس مطلوبًا أداؤها في جلسة واحدة.',
      'المشي السريع والسباحة وركوب الدراجة أمثلة شائعة لنشاط هوائي متوسط الشدة.',
      'تمارين المقاومة تشمل الأوزان وتمارين وزن الجسم وأشكالًا أخرى تستهدف العضلات الرئيسية.',
      'البدء بكمية صغيرة أفضل من انتظار خطة مثالية؛ أي حركة أفضل من عدم الحركة.'
    ],
    'note':'من لديه أعراض قلبية أو مرض مزمن أو محدودية حركية قد يحتاج تحديد نوع وشدة التمرين مع مختص صحي.',
    'sources':[('CDC — Adult Activity: An Overview','https://www.cdc.gov/physical-activity-basics/guidelines/adults.html')]
  },
  {
    'slug':'sleep','cat':'نمط حياة','title':'النوم الصحي: لماذا 7 ساعات ليست رفاهية؟','desc':'عدد ساعات النوم المناسبة للبالغين وعادات تساعد على نوم أفضل.','lead':'المعهد القومي للقلب والرئة والدم في NIH يذكر أن الخبراء يوصون غالبًا للبالغين بنحو 7 إلى 9 ساعات من النوم ليلًا.','points':[
      'حافظ قدر الإمكان على مواعيد نوم واستيقاظ متقاربة حتى في أيام العطلة.',
      'التعرض للضوء الطبيعي والنشاط البدني أثناء النهار يمكن أن يدعم نمط النوم.',
      'قلل الضوء القوي والشاشات في الساعات القريبة من النوم إذا كانت تؤثر عليك.',
      'الشخير الشديد أو الاختناق أثناء النوم أو النعاس النهاري المستمر أسباب تستحق التقييم الطبي.'
    ],
    'note':'احتياج النوم يختلف بين الأفراد والمراحل العمرية، وجودة النوم مهمة بجانب عدد الساعات.',
    'sources':[('NIH/NHLBI — How Much Sleep Is Enough?','https://www.nhlbi.nih.gov/health/sleep/how-much-sleep'),('CDC — Sleep and Heart Health','https://www.cdc.gov/heart-disease/about/sleep-and-heart-health.html')]
  },
  {
    'slug':'food-safety','cat':'سلامة الغذاء','title':'سلامة الطعام في المنزل: خمس قواعد أساسية','desc':'قواعد منظمة الصحة العالمية الخمس للتعامل الآمن مع الطعام وتقليل خطر الأمراض المنقولة بالغذاء.','lead':'تلخص منظمة الصحة العالمية سلامة التعامل مع الغذاء في خمس رسائل: النظافة، فصل النيء عن المطهو، الطهي الجيد، حفظ الطعام في درجات حرارة آمنة، واستخدام ماء ومواد خام آمنة.','points':[
      'اغسل اليدين وأسطح وأدوات إعداد الطعام جيدًا.',
      'افصل اللحوم والدواجن والأسماك النيئة عن الأطعمة الجاهزة للأكل.',
      'اطه الطعام جيدًا وتأكد من نضجه خصوصًا المنتجات الحيوانية.',
      'لا تترك الأطعمة سريعة التلف فترات طويلة في درجة حرارة الغرفة، واحفظها بالطريقة المناسبة.'
    ],
    'note':'الحوامل وكبار السن والأطفال الصغار وذوو المناعة الضعيفة قد يكونون أكثر عرضة لمضاعفات بعض الأمراض المنقولة بالغذاء.',
    'sources':[('WHO — Five keys to safer food','https://www.who.int/activities/promoting-safe-food-handling/five-key-to-safer-food')]
  },
  {
    'slug':'supplements','cat':'تغذية','title':'المكملات الغذائية: متى تكون مفيدة ومتى تحتاج حذرًا؟','desc':'المكملات ليست بديلًا للغذاء المتنوع وقد تتداخل مع الأدوية أو لا تناسب بعض الحالات.','lead':'يؤكد مكتب المكملات الغذائية في NIH أن بعض المكملات قد تساعد في سد نقص معين، لكنها لا تستبدل التنوع الغذائي، كما أن السلامة والتداخلات الدوائية مهمة.','points':[
      'لا تبدأ عدة مكملات لمجرد أنها تباع بدون وصفة؛ وجود حاجة فعلية هو الأهم.',
      'بعض الفيتامينات والمعادن يمكن أن تسبب أضرارًا عند تناول جرعات مرتفعة لفترات طويلة.',
      'أخبر الطبيب أو الصيدلي بكل المكملات والأعشاب التي تتناولها عند استخدام أدوية مزمنة.',
      'التحاليل أو التقييم الطبي قد يكونان أكثر فائدة من التخمين في حالات الاشتباه بنقص غذائي.'
    ],
    'note':'الحمل والرضاعة وأمراض الكبد والكلى واستخدام مميعات الدم أمثلة على حالات تستلزم انتباهًا أكبر قبل المكملات.',
    'sources':[('NIH ODS — Dietary Supplements: What You Need to Know','https://ods.od.nih.gov/factsheets/WYNTK-Consumer/'),('NIH ODS — Health Information','https://ods.od.nih.gov/HealthInformation/healthinformation.aspx')]
  },
  {
    'slug':'diabetes-prevention','cat':'صحة عامة','title':'تقليل خطر السكري من النوع الثاني','desc':'خطوات نمط الحياة التي تساعد على تقليل أو تأخير خطر السكري من النوع الثاني لدى المعرضين للإصابة.','lead':'تشير NIDDK إلى أن خفض الوزن عند وجود زيادة في الوزن، مع نمط أكل أقل في السعرات وزيادة النشاط البدني، يمكن أن يساعد في منع أو تأخير السكري من النوع الثاني لدى الأشخاص المعرضين للخطر.','points':[
      'ركز على تغييرات يمكن استمرارها مثل المشي المنتظم وتحسين جودة الوجبات.',
      'المشروبات المحلاة والوجبات شديدة التصنيع أهداف عملية للخفض عند استهلاكها بكثرة.',
      'إذا كان لديك تاريخ عائلي قوي أو زيادة وزن أو سكر حدودي فالمتابعة والفحوصات الدورية مهمة.',
      'التغييرات الصغيرة المتراكمة عادة أكثر قابلية للاستمرار من الحميات القاسية قصيرة الأمد.'
    ],
    'note':'هذه الصفحة للوقاية العامة وليست خطة علاج للسكري؛ من شُخّص بالسكري يحتاج متابعة فردية مع فريقه الطبي.',
    'sources':[('NIDDK — Preventing Type 2 Diabetes','https://www.niddk.nih.gov/health-information/diabetes/overview/preventing-type-2-diabetes/game-plan')]
  },
  {
    'slug':'heart-health','cat':'صحة عامة','title':'نمط غذائي يدعم صحة القلب','desc':'مبادئ غذائية وعادات يومية تدعم صحة القلب والأوعية الدموية.','lead':'توصيات القلب الحديثة تركز على نمط كامل: خضار وفواكه متنوعة، حبوب كاملة، بروتينات صحية، دهون غير مشبعة، وتقليل الصوديوم والسكريات المضافة والأطعمة فائقة التصنيع.','points':[
      'اجعل الطعام قليل التصنيع هو القاعدة، والمنتجات فائقة التصنيع استثناءً أقل تكرارًا.',
      'استبدل بعض الدهون المشبعة بدهون غير مشبعة بدل التركيز على منع الدهون كليًا.',
      'قلل الصوديوم خصوصًا إذا كان ضغط الدم مرتفعًا أو لديك عوامل خطر قلبية.',
      'النشاط البدني والنوم والإقلاع عن التدخين عناصر موازية للتغذية وليست منفصلة عنها.'
    ],
    'note':'أمراض القلب والكلى قد تحتاج تعديلات غذائية دقيقة لا يمكن تعميمها، خصوصًا فيما يتعلق بالسوائل والبوتاسيوم والصوديوم.',
    'sources':[('American Heart Association — 2026 Dietary Guidance','https://professional.heart.org/en/science-news/2026-dietary-guidance-to-improve-cardiovascular-health/top-things-to-know')]
  },
  {
    'slug':'healthy-weight','cat':'نمط حياة','title':'الوزن الصحي: ركز على العادات قبل الميزان','desc':'إدارة الوزن بصورة عملية عبر الطعام والنشاط والنوم بدل الحلول السريعة.','lead':'إدارة الوزن على المدى الطويل تعتمد على توازن الطاقة وجودة الطعام والحركة المنتظمة وعادات يمكن الاستمرار عليها، وليس على نظام قصير يسبب فقدًا سريعًا ثم ارتدادًا.','points':[
      'راقب أحجام الحصص والأطعمة عالية السعرات قليلة الشبع بدل منع مجموعات غذائية كاملة بلا سبب.',
      'زد الخضار والبقول والحبوب الكاملة ومصادر البروتين المناسبة لأنها تساعد على بناء وجبات أكثر إشباعًا.',
      'النشاط البدني مهم للصحة والحفاظ على الوزن بعد فقدانه، حتى لو كان خفض السعرات عاملًا رئيسيًا في فقد الوزن.',
      'النوم والضغط النفسي قد يؤثران في الشهية والقدرة على الالتزام بالعادات اليومية.'
    ],
    'note':'تقييم الوزن لا يعتمد على رقم واحد فقط؛ التاريخ الصحي ومحيط الخصر والأدوية والحالة النفسية وعوامل أخرى قد تكون مهمة.',
    'sources':[('CDC — Physical Activity and Your Weight and Health','https://www.cdc.gov/healthy-weight-growth/physical-activity/'),('WHO — Healthy diet','https://www.who.int/news-room/fact-sheets/detail/healthy-diet')]
  },
  {
    'slug':'vitamins-minerals','cat':'تغذية','title':'الفيتامينات والمعادن: الأفضل من الطعام أولًا غالبًا','desc':'لماذا التنوع الغذائي مهم للحصول على العناصر الدقيقة، ومتى قد نحتاج تقييمًا أو مكملًا.','lead':'الفيتامينات والمعادن ضرورية لوظائف عديدة في الجسم، لكن الاحتياج يختلف، والمكمل ليس بديلًا تلقائيًا لنظام غذائي متنوع.','points':[
      'التنوع بين الخضار والفواكه والبقول والحبوب ومنتجات الألبان أو بدائلها ومصادر البروتين يزيد فرص تغطية الاحتياجات.',
      'النقص الحقيقي قد يحتاج تحليلًا أو تقييمًا سريريًا بدل الاعتماد على أعراض عامة وغير محددة.',
      'الحديد وفيتامين د وB12 وحمض الفوليك أمثلة لعناصر قد تحتاج اهتمامًا خاصًا في ظروف معينة.',
      'التزم بالجرعة الموصى بها ولا تجمع منتجات متعددة تحتوي العنصر نفسه دون مراجعة مجموع الجرعات.'
    ],
    'note':'مكتب المكملات الغذائية التابع لـNIH يوفر نشرات تفصيلية لكل عنصر تشمل الجرعات والسلامة والتداخلات الدوائية.',
    'sources':[('NIH ODS — Dietary Supplement Fact Sheets','https://ods.od.nih.gov/HealthInformation/healthinformation.aspx')]
  }
]

common_head = '''<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#0b746d"><link rel="icon" href="../assets/mark.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="../styles.css"><link rel="stylesheet" href="../theme-v2.css">'''

def source_list(sources):
    return ''.join(f'<li><a href="{escape(u)}" target="_blank" rel="noopener noreferrer">{escape(n)} ↗</a></li>' for n,u in sources)

def card(a):
    return f'''<article class="health-card"><div class="health-card-top"><span>{escape(a['cat'])}</span><b>موثّق</b></div><h2>{escape(a['title'])}</h2><p>{escape(a['desc'])}</p><a href="health/{a['slug']}.html" class="health-read">اقرأ الدليل الكامل ←</a></article>'''

def nav(prefix=''):
    return f'''<header class="site-header health-header"><a class="brand" href="{prefix}./" aria-label="أدوية مصر - الرئيسية"><img src="{prefix}assets/logo.png" class="brand-logo" width="92" height="76" alt="أدوية مصر - ADWYA EGYPT"><span class="brand-text"><strong>أدوية مصر</strong><small>ADWYA EGYPT</small></span></a><nav class="header-links" aria-label="التنقل الرئيسي"><a class="nav-link" href="{prefix}./">البحث</a><a class="nav-link active" href="{prefix}health.html">صحة وتغذية</a><a class="nav-link" href="{prefix}sources.html">المصادر</a><a class="nav-link" href="{prefix}about.html">عن الموقع</a></nav><div class="header-actions"><button class="icon-btn" id="themeBtn" type="button" title="الوضع الليلي" aria-label="تبديل الوضع الليلي"></button></div></header>'''

def footer(prefix=''):
    return f'''<footer><div><strong>أدوية مصر — ADWYA EGYPT</strong><p>محتوى معلوماتي عام، لا يقدّم تشخيصًا ولا يصف جرعات أو علاجًا فرديًا.</p></div><div class="footer-links"><a href="{prefix}./">بحث الأدوية</a><a href="{prefix}health.html">صحة وتغذية</a><a href="{prefix}sources.html">المصادر</a><a href="{prefix}privacy.html">الخصوصية</a></div></footer>'''

# Create health hub
hub_schema = {
  '@context':'https://schema.org','@type':'CollectionPage','name':'صحة وتغذية | أدوية مصر',
  'description':'مكتبة عربية مبسطة للمعلومات الصحية والتغذوية المبنية على مصادر موثوقة.',
  'url':f'{SITE}/health.html','inLanguage':'ar',
  'hasPart':[{'@type':'MedicalWebPage','name':a['title'],'url':f"{SITE}/health/{a['slug']}.html"} for a in articles]
}
hub = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#0b746d"><title>صحة وتغذية — معلومات موثوقة ومبسطة | أدوية مصر</title><meta name="description" content="مكتبة صحة وتغذية عربية: التغذية المتوازنة، السكر والملح والدهون، الماء، النشاط، النوم، المكملات، سلامة الغذاء، صحة القلب والوقاية من السكري — بمصادر WHO وNIH وCDC وNHS."><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{SITE}/health.html"><meta property="og:type" content="website"><meta property="og:title" content="صحة وتغذية | أدوية مصر"><meta property="og:description" content="أدلة صحية وتغذوية عربية مختصرة وعملية مبنية على مصادر موثوقة."><meta property="og:url" content="{SITE}/health.html"><meta property="og:image" content="{SITE}/assets/logo.png"><link rel="icon" href="assets/mark.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="theme-v2.css"><script type="application/ld+json">{json.dumps(hub_schema,ensure_ascii=False)}</script></head><body>{nav('')}<main class="health-page"><section class="health-hero"><span class="health-kicker">معلومات صحية بمصادر واضحة</span><h1>صحة وتغذية، بدون تهويل ولا وصفات عشوائية.</h1><p>مكتبة مبسطة تساعدك تفهم أساسيات التغذية ونمط الحياة الصحي. كل موضوع يذكر مصادره الأصلية بوضوح، والمحتوى للتثقيف العام ولا يستبدل الطبيب أو الصيدلي.</p><div class="health-source-badges"><span>WHO</span><span>NIH</span><span>CDC</span><span>NHS</span><span>NIDDK</span></div></section><section class="health-feature"><div><span>ابدأ من هنا</span><h2>أهم قاعدة: النمط الكامل أهم من الطعام الواحد</h2><p>تحسين الصحة عادة يأتي من مجموعة عادات متكررة: طعام متنوع قليل التصنيع، حركة منتظمة، نوم كافٍ، ومتابعة عوامل الخطورة عند الحاجة. لا يوجد غذاء منفرد يعالج كل شيء.</p></div><a href="health/healthy-diet.html">دليل التغذية المتوازنة ←</a></section><section class="health-grid">{''.join(card(a) for a in articles)}</section><section class="health-disclaimer"><strong>تنبيه طبي</strong><p>هذه المعلومات عامة للتثقيف وليست تشخيصًا أو خطة علاج أو بديلًا للاستشارة الطبية. إذا كان لديك مرض مزمن، حمل، أعراض مقلقة، أو تستخدم أدوية منتظمة، فناقش أي تغيير كبير في الغذاء أو المكملات أو النشاط مع مختص صحي.</p></section></main>{footer('')}<script src="app.js"></script></body></html>'''
(ROOT/'health.html').write_text(hub,encoding='utf-8')

health_dir = ROOT/'health'; health_dir.mkdir(exist_ok=True)
for a in articles:
    schema = {
      '@context':'https://schema.org','@type':'MedicalWebPage','name':a['title'],'headline':a['title'],
      'description':a['desc'],'url':f"{SITE}/health/{a['slug']}.html",'inLanguage':'ar',
      'dateModified':TODAY,'isPartOf':{'@type':'WebSite','name':'أدوية مصر','url':f'{SITE}/'},
      'publisher':{'@type':'Organization','name':'أدوية مصر — ADWYA EGYPT','url':f'{SITE}/'}
    }
    bullets=''.join(f'<li>{escape(p)}</li>' for p in a['points'])
    page=f'''<!doctype html><html lang="ar" dir="rtl"><head>{common_head}<title>{escape(a['title'])} | صحة وتغذية | أدوية مصر</title><meta name="description" content="{escape(a['desc'])}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{SITE}/health/{a['slug']}.html"><meta property="og:type" content="article"><meta property="og:title" content="{escape(a['title'])}"><meta property="og:description" content="{escape(a['desc'])}"><meta property="og:url" content="{SITE}/health/{a['slug']}.html"><meta property="og:image" content="{SITE}/assets/logo.png"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body>{nav('../')}<main class="health-article"><nav class="breadcrumbs" aria-label="مسار الصفحة"><a href="../health.html">صحة وتغذية</a><span>←</span><span>{escape(a['cat'])}</span></nav><article><div class="article-label">{escape(a['cat'])} · آخر مراجعة {TODAY}</div><h1>{escape(a['title'])}</h1><p class="article-lead">{escape(a['lead'])}</p><div class="article-summary"><strong>الخلاصة العملية</strong><ul>{bullets}</ul></div><h2>كيف تطبق المعلومة في حياتك اليومية؟</h2><p>ابدأ بتغيير واحد يمكن قياسه والاستمرار عليه لمدة أسبوعين أو أكثر، ثم أضف تغييرًا آخر. الهدف ليس الكمال، بل تحسين الاتجاه العام لعاداتك. إذا وجدت نصيحة تتعارض مع خطة علاج أو تعليمات طبية خاصة بك، فالأولوية لتوجيه فريقك المعالج.</p><h2>نقطة مهمة</h2><p>{escape(a['note'])}</p><section class="article-sources"><h2>المصادر</h2><p>تمت مراجعة هذا الملخص بالرجوع إلى المصادر التالية. افتح المصدر الأصلي للحصول على التفاصيل الكاملة والتحديثات الأحدث.</p><ul>{source_list(a['sources'])}</ul></section><div class="article-warning"><strong>المحتوى للتثقيف العام فقط.</strong> لا يصف أدوية أو جرعات ولا يشخّص الأمراض.</div></article><aside class="related-health"><h2>اقرأ أيضًا</h2>{''.join(f'<a href="{x["slug"]}.html">{escape(x["title"])} ←</a>' for x in articles if x['slug']!=a['slug'])[:3000]}</aside></main>{footer('../')}<script src="../app.js"></script></body></html>'''
    (health_dir/f"{a['slug']}.html").write_text(page,encoding='utf-8')

# Add nav tab to existing root pages
for name in ['index.html','about.html','sources.html','privacy.html']:
    p=ROOT/name
    if not p.exists(): continue
    txt=p.read_text(encoding='utf-8')
    if 'href="health.html"' not in txt:
        txt=txt.replace('<a class="nav-link" href="sources.html">المصادر</a>', '<a class="nav-link" href="health.html">صحة وتغذية</a>\n      <a class="nav-link" href="sources.html">المصادر</a>')
    p.write_text(txt,encoding='utf-8')

# Responsive/mobile fixes + proper crescent icon + health styles
cssp=ROOT/'theme-v2.css'; css=cssp.read_text(encoding='utf-8')
marker='/* Health hub + responsive hardening v3 */'
if marker not in css:
    css += r'''

/* Health hub + responsive hardening v3 */
html,body{width:100%;max-width:100%;overflow-x:hidden}
html{overflow-x:clip}
body{overflow-x:clip}
main,.site-header,.hero,footer{max-width:100%}
img,svg,video,canvas{max-width:100%}
.brand,.brand-text,.header-links,.header-actions,.search-shell,.search-row,#searchInput,.results-shell,.results-panel,.drug-card,.card-top,.drug-names,.browse-section,.safety-section{min-width:0}
.header-links{max-width:100%;overscroll-behavior-inline:contain;scrollbar-width:none}
.header-links::-webkit-scrollbar{display:none}
#themeBtn{position:relative;overflow:hidden;font-size:0}
#themeBtn::before{content:"";width:19px;height:19px;border-radius:50%;background:var(--brand-dark);box-shadow:-6px -2px 0 0 var(--surface);transform:rotate(-24deg);transition:.25s ease}
body.dark #themeBtn::before{width:17px;height:17px;background:#f5c56a;box-shadow:0 0 0 3px color-mix(in srgb,#f5c56a 18%,transparent);transform:none}
body.dark #themeBtn::after{content:"✦";position:absolute;font-size:9px;color:#f5c56a;inset-inline-end:6px;top:5px}
.health-page,.health-article{max-width:1180px;margin:0 auto;padding:38px clamp(14px,3vw,34px) 70px}
.health-hero{padding:42px clamp(18px,4vw,54px);border:1px solid var(--line);border-radius:28px;background:linear-gradient(135deg,var(--surface),var(--surface-2));box-shadow:var(--shadow);text-align:center;overflow:hidden}
.health-kicker,.article-label{display:inline-flex;padding:6px 10px;border-radius:999px;background:color-mix(in srgb,var(--brand) 10%,var(--surface));color:var(--brand-dark);font-size:12px;font-weight:800}
.health-hero h1{font-size:clamp(32px,5vw,54px);max-width:900px;margin:16px auto 12px}.health-hero p{max-width:820px;margin:0 auto;color:var(--muted);font-size:17px}.health-source-badges{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:22px}.health-source-badges span{padding:7px 11px;border:1px solid var(--line);background:var(--surface);border-radius:10px;font-weight:800;font-size:12px;color:var(--brand-dark)}
.health-feature{margin:20px 0;display:grid;grid-template-columns:1fr auto;gap:20px;align-items:center;padding:24px;border:1px solid var(--line);border-radius:22px;background:var(--surface)}.health-feature span{font-size:12px;font-weight:800;color:var(--brand)}.health-feature h2{margin:3px 0 8px;font-size:24px}.health-feature p{margin:0;color:var(--muted)}.health-feature>a{padding:11px 15px;border-radius:12px;background:var(--brand-dark);color:#fff;font-weight:800;white-space:nowrap}
.health-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.health-card{display:flex;flex-direction:column;min-width:0;padding:20px;border:1px solid var(--line);border-radius:20px;background:var(--surface);box-shadow:0 4px 16px rgba(24,53,50,.035)}.health-card:hover{border-color:color-mix(in srgb,var(--brand) 35%,var(--line));transform:translateY(-2px)}.health-card-top{display:flex;justify-content:space-between;gap:8px;font-size:11px}.health-card-top span{color:var(--brand);font-weight:800}.health-card-top b{color:var(--muted)}.health-card h2{font-size:18px;line-height:1.55;margin:10px 0 7px}.health-card p{color:var(--muted);font-size:13px;margin:0 0 16px}.health-read{margin-top:auto;font-weight:800;color:var(--brand-dark)}
.health-disclaimer,.article-warning{margin-top:22px;padding:16px 18px;border-radius:16px;background:color-mix(in srgb,var(--warn) 9%,var(--surface));border:1px solid color-mix(in srgb,var(--warn) 30%,var(--line))}.health-disclaimer p{margin:4px 0 0;color:var(--muted)}
.health-article{display:grid;grid-template-columns:minmax(0,1fr) 290px;gap:22px;align-items:start}.breadcrumbs{grid-column:1/-1;display:flex;gap:8px;color:var(--muted);font-size:13px}.health-article>article{background:var(--surface);border:1px solid var(--line);border-radius:24px;padding:clamp(20px,4vw,40px)}.health-article h1{font-size:clamp(30px,5vw,46px);margin:14px 0}.article-lead{font-size:18px;color:var(--muted);line-height:1.9}.article-summary{margin:24px 0;padding:18px;border-radius:18px;background:var(--surface-2)}.article-summary ul{margin:10px 0 0;padding-inline-start:22px}.article-summary li{margin:8px 0}.health-article h2{margin:28px 0 8px;font-size:22px}.health-article p{color:var(--muted)}.article-sources ul{padding-inline-start:20px}.article-sources a{color:var(--brand-dark);font-weight:700}.related-health{position:sticky;top:110px;background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:17px;display:grid;gap:8px;max-height:72vh;overflow:auto}.related-health h2{font-size:17px;margin:0 0 4px}.related-health a{padding:9px 10px;background:var(--surface-2);border-radius:10px;font-size:12px;color:var(--ink)}
@media(max-width:900px){.health-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.health-article{grid-template-columns:1fr}.related-health{position:static;max-height:none}.health-feature{grid-template-columns:1fr}.health-feature>a{justify-self:start}}
@media(max-width:640px){
  .site-header{padding-inline:10px!important;gap:8px!important;width:100%;max-width:100vw}
  .brand{max-width:calc(100vw - 150px);gap:6px}.brand-logo{flex:0 0 auto}.brand-text{overflow:hidden}.brand-text strong{overflow:hidden;text-overflow:ellipsis}
  .header-actions{flex:0 0 auto}.header-links{width:100%;overflow-x:auto;overflow-y:hidden;justify-content:flex-start!important;padding-inline:2px;padding-bottom:5px}.nav-link{flex:0 0 auto;padding-inline:11px}
  .hero{width:100%;padding-inline:10px!important}.hero-inner,.search-shell{width:100%;max-width:100%}.search-row{width:100%;grid-template-columns:38px minmax(0,1fr) 34px!important}.search-icon{font-size:26px!important}#searchInput{width:100%;max-width:100%;font-size:16px!important;padding-inline:4px}
  .stats-strip{width:calc(100% - 20px);max-width:calc(100vw - 20px);margin-inline:auto!important}
  .results-shell,.browse-section,.safety-section{width:calc(100% - 20px);max-width:calc(100vw - 20px);margin-inline:auto!important;padding-inline:0}.browse-section,.safety-section{padding:20px 14px!important}
  .drug-card,.card-top,.drug-names{max-width:100%}.price{max-width:94px;overflow:hidden;text-overflow:ellipsis}.tag{max-width:150px}
  .compare-dock{width:calc(100vw - 20px);max-width:calc(100vw - 20px);grid-template-columns:auto 1fr}.compare-dock .primary-btn{grid-column:1/-1;width:100%}
  .modal{width:calc(100vw - 16px);max-width:calc(100vw - 16px)}.modal-body{padding:20px 15px}.drug-hero{flex-wrap:wrap}.modal-price{font-size:22px}
  .health-page,.health-article{width:100%;padding:20px 10px 50px}.health-hero{padding:28px 16px}.health-hero h1{font-size:32px}.health-hero p{font-size:15px}.health-grid{grid-template-columns:1fr}.health-feature{padding:18px}.health-card{padding:17px}.health-article>article{padding:20px 16px}.article-lead{font-size:16px}
}
'''
    cssp.write_text(css,encoding='utf-8')

# Update builder for custom Pages workflow
bp=ROOT/'scripts/build-pages.mjs'; b=bp.read_text(encoding='utf-8')
b=b.replace("process.env.SITE_URL||'https://iegy.github.io/adwya'", "process.env.SITE_URL||'https://iegy.net/adwya'")
b=b.replace("'privacy.html']", "'privacy.html','health.html']")
if "fs.cpSync(path.join(root,'health')" not in b:
    b=b.replace("fs.cpSync(path.join(root,'data'),path.join(out,'data'),{recursive:true});", "fs.cpSync(path.join(root,'data'),path.join(out,'data'),{recursive:true});if(fs.existsSync(path.join(root,'health')))fs.cpSync(path.join(root,'health'),path.join(out,'health'),{recursive:true});")
health_urls=",".join([f"`${{site}}/health/{a['slug']}.html`" for a in articles])
b=re.sub(r"const urls=\[([^\]]+)\];", lambda m: "const urls=["+m.group(1)+",`${site}/health.html`,"+health_urls+"];", b, count=1)
bp.write_text(b,encoding='utf-8')

# Update workflow SITE_URL to custom live URL
wp=ROOT/'.github/workflows/pages.yml'; w=wp.read_text(encoding='utf-8').replace('SITE_URL: https://iegy.github.io/adwya','SITE_URL: https://iegy.net/adwya'); wp.write_text(w,encoding='utf-8')

# Root sitemap + robots
urls=[f'{SITE}/',f'{SITE}/about.html',f'{SITE}/sources.html',f'{SITE}/privacy.html',f'{SITE}/health.html']+[f"{SITE}/health/{a['slug']}.html" for a in articles]
xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls)+'</urlset>\n'
(ROOT/'sitemap.xml').write_text(xml,encoding='utf-8')
(ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n',encoding='utf-8')

# Basic assertions
assert (ROOT/'health.html').exists() and len(list(health_dir.glob('*.html'))) == len(articles)
assert 'overflow-x:clip' in cssp.read_text(encoding='utf-8')
assert 'صحة وتغذية' in (ROOT/'index.html').read_text(encoding='utf-8')
print('Generated',len(articles),'health articles and completed responsive/SEO upgrade')
