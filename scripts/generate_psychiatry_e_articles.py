from pathlib import Path
from datetime import date
import html
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "03_精神医学"
ATT = ROOT / "content" / "99_添付管理"
TODAY = date.today().isoformat()

SOURCES = {
    "WHO": "[1] World Health Organization. Mental disorders fact sheet. https://www.who.int/news-room/fact-sheets/detail/mental-disorders",
    "ICD": "[2] World Health Organization. Clinical descriptions and diagnostic requirements for ICD-11 mental, behavioural and neurodevelopmental disorders. https://www.who.int/publications/b/68103",
    "DSM": "[3] American Psychiatric Association. Diagnostic and Statistical Manual of Mental Disorders, Fifth Edition, Text Revision (DSM-5-TR). https://www.psychiatry.org/psychiatrists/practice/dsm",
    "RDOC": "[4] National Institute of Mental Health. About RDoC. https://www.nimh.nih.gov/research/research-funded-by-nimh/rdoc/about-rdoc",
    "KJ": "[5] Kendell, R., & Jablensky, A. (2003). Distinguishing between the validity and utility of psychiatric diagnoses. American Journal of Psychiatry, 160(1), 4-12. https://doi.org/10.1176/appi.ajp.160.1.4",
    "JAB": "[6] Jablensky, A. (2016). Psychiatric classifications: validity and utility. World Psychiatry, 15(1), 26-31. https://doi.org/10.1002/wps.20284",
    "ENGEL": "[7] Engel, G. L. (1977). The need for a new medical model: a challenge for biomedicine. Science, 196(4286), 129-136. https://doi.org/10.1126/science.847460",
    "MSE": "[8] Voss, R. M., & Das, J. M. Mental Status Examination. StatPearls. https://www.ncbi.nlm.nih.gov/books/NBK546682/",
    "CLINMSE": "[9] Trzepacz, P. T., & Baker, R. W. The Mental Status Examination. Clinical Methods. https://www.ncbi.nlm.nih.gov/books/NBK320/",
    "MERCK": "[10] Merck Manual Professional Edition. Initial Psychiatric Assessment. https://www.merckmanuals.com/professional/multimedia/table/initial-psychiatric-assessment",
    "NICE": "[11] NICE. Self-harm: assessment, management and preventing recurrence (NG225). https://www.nice.org.uk/guidance/ng225",
    "SAMHSA": "[12] SAMHSA. National Behavioral Health Crisis Care Guidance. https://www.samhsa.gov/mental-health/national-behavioral-health-crisis-care",
    "SAFETY": "[13] Stanley, B., et al. (2018). Comparison of the Safety Planning Intervention With Follow-up vs Usual Care of Suicidal Patients Treated in the Emergency Department. JAMA Psychiatry, 75(9), 894-900. https://doi.org/10.1001/jamapsychiatry.2018.1776",
    "WAKE": "[14] Wakefield, J. C. (1992). The concept of mental disorder: on the boundary between biological facts and social values. American Psychologist, 47(3), 373-388. https://doi.org/10.1037/0003-066X.47.3.373",
    "BERRIOS": "[15] Berrios, G. E. (1996). The History of Mental Symptoms: Descriptive Psychopathology since the Nineteenth Century. Cambridge University Press. https://doi.org/10.1017/CBO9780511526725",
    "HALL": "[16] Waters, F., et al. (2014). Auditory hallucinations in schizophrenia and nonschizophrenia populations. Schizophrenia Bulletin, 40(Suppl 4), S233-S245. https://doi.org/10.1093/schbul/sbu005",
    "DEL": "[17] Garety, P. A., & Freeman, D. (1999). Cognitive approaches to delusions: a critical review. British Journal of Clinical Psychology, 38(2), 113-154. https://doi.org/10.1348/014466599162700",
    "MOOD": "[18] Malhi, G. S., & Mann, J. J. (2018). Depression. The Lancet, 392(10161), 2299-2312. https://doi.org/10.1016/S0140-6736(18)31948-2",
    "ANX": "[19] Craske, M. G., & Stein, M. B. (2016). Anxiety. The Lancet, 388(10063), 3048-3059. https://doi.org/10.1016/S0140-6736(16)30381-6",
    "DISS": "[20] Spiegel, D., et al. (2011). Dissociative disorders in DSM-5. Depression and Anxiety, 28(12), E17-E45. https://doi.org/10.1002/da.20923",
}

ARTICLES = [
    {
        "title": "精神医学とは何か",
        "slug": "psychiatry-overview",
        "aliases": ["精神医学", "psychiatry"],
        "question": "精神医学を、脳の医学だけでも、社会的支援だけでもない臨床科学として理解する。",
        "lead": "精神医学は、精神的苦痛、行動の変化、対人・社会機能の障害を、身体・心理・社会の複数水準から評価し、理解し、支援する医学領域である。",
        "points": [
            "対象は「疾患名」だけではなく、苦痛、生活機能、安全、価値、環境を含む。",
            "診断分類は共通言語として有用だが、本人の語りと生活文脈を置き換えるものではない。",
            "精神医学の判断は、観察可能な所見、面接で得た主観的経験、経過、身体疾患・薬物・社会要因の鑑別を統合する。",
        ],
        "sections": [
            ("定義", "WHOは精神疾患を、認知、情動制御、行動に臨床的に意味のある障害があり、苦痛や機能障害と結びつく状態として説明している[1]。この定義は、単なる逸脱や不快感ではなく、本人と環境の相互作用の中で生じる支援ニーズを扱うという点を強調する。"),
            ("臨床実践", "精神医学の診療では、診断、重症度、リスク、併存症、生活史、文化的背景、支援資源を同時に考える。診断名は治療選択や制度利用を助けるが、同じ診断でも困り方、回復目標、リスクは大きく異なる。"),
            ("研究との接続", "DSMやICDは臨床分類、RDoCは研究枠組みとして発達してきた[2][3][4]。この違いを押さえると、精神医学が「分類の医学」であると同時に「機序を探す科学」でもあることが見えやすい。"),
        ],
        "refs": ["WHO", "ICD", "DSM", "RDOC", "ENGEL", "KJ"],
        "links": ["DSM・ICD・RDoCの違い", "生物心理社会モデル", "精神科診断の意義と限界"],
    },
    {
        "title": "精神疾患概念の歴史",
        "slug": "history-of-mental-disorder-concepts",
        "aliases": ["精神疾患の歴史", "精神医学史"],
        "question": "精神疾患という概念が、道徳・身体・分類・機能障害のあいだでどう変化してきたかを整理する。",
        "lead": "精神疾患概念は固定した自然種として発見されたというより、症状記述、施設医療、統計分類、科学的仮説、社会的価値が重なって形成されてきた。",
        "points": [
            "19世紀以降、記述精神病理学は症状を細かく名づけ、経過と予後から疾患単位を考えた。",
            "20世紀後半の操作的診断は信頼性を上げたが、妥当性の問題を残した。",
            "疾患概念には生物学的事実と社会的価値判断の境界問題が含まれる。",
        ],
        "sections": [
            ("記述の時代", "Berriosは、現代の精神症状語彙が19世紀以降の記述精神病理学の中で形成されたことを示した[15]。幻覚、妄想、気分、意欲といった語は、観察と患者の語りを結びつけるための臨床的道具である。"),
            ("操作的診断", "DSM-III以後の操作的基準は、臨床家間の一致を改善する方向に働いた。しかしKendellとJablenskyが論じたように、多くの診断カテゴリーが明確な自然境界をもつとは限らない[5]。"),
            ("価値と科学", "Wakefieldの有害な機能不全モデルは、精神疾患概念が生物学的機能の失調と価値判断の両方を含むことを示す代表的議論である[14]。したがって歴史を学ぶ目的は、古い分類名を暗記することではなく、概念の前提を点検することである。"),
        ],
        "refs": ["BERRIOS", "WAKE", "KJ", "JAB", "DSM", "ICD"],
        "links": ["精神医学とは何か", "精神症候学入門", "カテゴリ診断と次元モデル"],
    },
    {
        "title": "DSM・ICD・RDoCの違い",
        "slug": "dsm-icd-rdoc-differences",
        "aliases": ["DSM ICD RDoC", "精神医学分類"],
        "question": "3つの枠組みを、目的・利用場面・限界から比較する。",
        "lead": "DSM、ICD、RDoCは互いに競合する単一の正解ではなく、臨床診断、国際統計、研究機序という異なる目的をもつ枠組みである。",
        "points": [
            "DSMは米国精神医学会による臨床・研究の操作的診断体系である。",
            "ICDはWHOによる国際的な疾病・死亡・保健統計の分類で、精神疾患はその一章に位置づく。",
            "RDoCは診断マニュアルではなく、神経行動システムを次元的に研究するための枠組みである。",
        ],
        "sections": [
            ("DSM", "DSM-5-TRは精神疾患の診断基準、記述、鑑別、併存、文化的配慮をまとめた臨床分類である[3]。臨床や研究で共通言語を提供する一方、カテゴリーが病因単位と一致するとは限らない。"),
            ("ICD", "ICD-11 CDDRは、世界の多様な医療環境で使用できるよう、臨床記述と診断要件を提示する[2]。ICDは保健統計、行政、診療情報の国際比較に強い。"),
            ("RDoC", "NIMHのRDoCは、負の価システム、認知システムなどの機能ドメインを、遺伝子から自己報告まで複数の分析単位で扱う研究枠組みであり、DSMやICDを置き換える診断ガイドではない[4]。"),
        ],
        "refs": ["DSM", "ICD", "RDOC", "KJ", "JAB"],
        "links": ["精神科診断の意義と限界", "カテゴリ診断と次元モデル", "精神医学とは何か"],
    },
    {
        "title": "精神科診断の意義と限界",
        "slug": "meaning-and-limits-of-psychiatric-diagnosis",
        "aliases": ["精神科診断", "診断の限界"],
        "question": "診断名が何を助け、何を助けないのかを見分ける。",
        "lead": "精神科診断は、苦痛を説明し、支援をつなぎ、研究と制度を動かす共通言語である。しかし、それは本人の経験や原因を完全に説明するものではない。",
        "points": [
            "診断は臨床的有用性をもつが、病因的妥当性とは区別される。",
            "診断の前後には、重症度、経過、リスク、併存、文化、生活機能の評価が必要である。",
            "診断はラベルとして固定化されると、スティグマや自己理解の狭まりを生むことがある。",
        ],
        "sections": [
            ("意義", "診断名は、症状のまとまり、予後、治療選択、研究知見、制度上の支援を結びつける。ICDやDSMが臨床記述を整備するのは、評価とケアの最低限の共通基盤を作るためである[2][3]。"),
            ("限界", "KendellとJablenskyは、診断の妥当性と有用性を区別した[5]。多くの精神疾患カテゴリーは、感染症のような単一病因や明確な境界をもつわけではない。"),
            ("実践上の工夫", "診断を使うときは、ケースフォーミュレーション、本人の語り、文化的意味、リスク評価を組み合わせる。診断を入口にしつつ、支援目標を診断名だけに還元しない姿勢が重要である。"),
        ],
        "refs": ["KJ", "JAB", "DSM", "ICD", "WHO", "WAKE"],
        "links": ["ケースフォーミュレーション入門", "カテゴリ診断と次元モデル", "精神科面接の基本"],
    },
    {
        "title": "精神科面接の基本",
        "slug": "basics-of-psychiatric-interview",
        "aliases": ["精神科面接", "初回面接"],
        "question": "精神科面接を、情報収集だけでなく関係形成と安全確認の場として理解する。",
        "lead": "精神科面接は、症状を聞き出す手続きであると同時に、本人が何に困り、何を恐れ、何を望むのかを共同で明らかにする対話である。",
        "points": [
            "面接は主訴、現病歴、既往歴、生活史、家族歴、物質使用、身体疾患、リスクを統合する。",
            "開かれた質問と焦点化した質問を往復し、本人の言葉を尊重する。",
            "危機や自殺リスクが疑われるときは、共感的姿勢を保ちながら具体的に確認する。",
        ],
        "sections": [
            ("構造", "初回評価では、現在の困りごと、発症時期、経過、誘因、生活機能、過去の治療、身体疾患、服薬、物質使用、家族・社会状況を系統的に確認する[10]。"),
            ("関係形成", "面接の質は情報量だけでは決まらない。本人が恥、恐怖、不信、混乱を抱えている場合、性急な解釈よりも、理解した内容を確認しながら進めることが安全な情報収集につながる。"),
            ("観察", "MSEは面接中の観察と質問から構成される[8]。話す速さ、表情、思考のまとまり、知覚体験、見当識、洞察などは、質問票だけでは捉えにくい臨床情報である。"),
        ],
        "refs": ["MERCK", "MSE", "CLINMSE", "NICE", "SAMHSA"],
        "links": ["精神科病歴聴取の技法", "精神状態診察 MSE 入門", "精神科リスク評価の基本"],
    },
    {
        "title": "精神状態診察 MSE 入門",
        "slug": "mental-status-examination-introduction",
        "aliases": ["MSE", "精神状態診察"],
        "question": "MSEを、現在の精神状態を記述するための観察フレームとして学ぶ。",
        "lead": "精神状態診察（MSE）は、面接時点での外観、行動、気分、思考、知覚、認知、洞察、判断を構造化して記述する方法である。",
        "points": [
            "MSEは診断そのものではなく、診断・リスク評価・経過観察を支える記述である。",
            "観察所見と本人の主観的報告を区別して書く。",
            "正常・異常の二分法ではなく、文脈、文化、発達段階、身体状態を考慮する。",
        ],
        "sections": [
            ("領域", "MSEの代表的領域は、外観、行動、精神運動、発話、気分と感情、思考過程、思考内容、知覚、認知、洞察、判断である[8]。"),
            ("書き方", "『不安そう』だけではなく、『落ち着きなく手を動かし、声量は小さく、気分は不安と述べ、感情は制限される』のように観察と引用を分けると再評価しやすい。"),
            ("限界", "MSEは横断面の記述であり、病歴や経過を代替しない[9]。せん妄、神経疾患、薬物、睡眠不足など、精神症状に見える身体・環境要因も同時に考える。"),
        ],
        "refs": ["MSE", "CLINMSE", "MERCK", "DSM", "ICD"],
        "links": ["精神科面接の基本", "精神症候学入門", "精神科病歴聴取の技法"],
    },
    {
        "title": "精神科病歴聴取の技法",
        "slug": "psychiatric-history-taking",
        "aliases": ["病歴聴取", "精神科アセスメント"],
        "question": "症状の羅列ではなく、時間軸と意味づけをもつ病歴として聴く。",
        "lead": "精神科病歴聴取は、いつ、何が、どのように始まり、何で悪化・軽快し、生活や安全にどう影響したかを時間軸で組み立てる技法である。",
        "points": [
            "現病歴は発症、経過、誘因、重症度、機能障害、対処、受療歴を含める。",
            "既往歴、家族歴、発達歴、トラウマ、物質使用、身体疾患、薬剤を確認する。",
            "本人の説明モデルと支援希望を聞くことで、治療同盟が作りやすくなる。",
        ],
        "sections": [
            ("時間軸", "症状の有無だけでなく、初発、エピソード、寛解、再燃、生活上の転機を時系列に置く。これにより、気分症状、精神病症状、不安、解離、物質使用、身体疾患の鑑別が進めやすくなる。"),
            ("情報源", "本人の語りは中心だが、同意を得たうえで家族、紹介状、処方歴、検査、過去記録を統合することがある[10]。情報の不一致は『矛盾』ではなく、状況理解の材料として扱う。"),
            ("質問技法", "最初は開かれた質問で語りを広げ、次に期間、頻度、重症度、機能影響、リスクを具体化する。侵襲的な話題は、目的を説明し、答えたくない権利も尊重する。"),
        ],
        "refs": ["MERCK", "MSE", "NICE", "DSM", "ICD"],
        "links": ["精神科面接の基本", "ケースフォーミュレーション入門", "精神科リスク評価の基本"],
    },
    {
        "title": "精神科リスク評価の基本",
        "slug": "psychiatric-risk-assessment-basics",
        "aliases": ["リスク評価", "精神科安全評価"],
        "question": "リスク評価を、予言ではなく安全計画と支援調整のための臨床推論として捉える。",
        "lead": "精神科リスク評価は、自殺、自傷、他害、セルフネグレクト、虐待、事故、医療中断などを、動的な状況として把握し安全につなげる作業である。",
        "points": [
            "リスクは固定属性ではなく、急性要因、保護要因、アクセス可能な手段、支援資源で変化する。",
            "尺度は補助であり、将来の行為を単独で予測する道具ではない。",
            "評価の目的は分類ではなく、具体的な安全行動と連携を決めることである。",
        ],
        "sections": [
            ("対象", "精神科で扱うリスクには、自殺・自傷、暴力、被害、医学的急変、薬物・アルコール、離脱、家庭内安全、児童・高齢者・障害者保護が含まれる。"),
            ("構造化", "評価では、過去歴、現在の意図、計画、手段、衝動性、物質使用、精神症状、身体状態、社会的孤立、保護要因を確認する。NICEはリスク尺度を将来予測のために単独使用しないことを勧めている[11]。"),
            ("対応", "リスクが高いほど、面接室内の安全、同席者、危険物へのアクセス、緊急連絡先、危機サービス、入院適応、法的枠組みを確認する。評価と介入は同時に進む。"),
        ],
        "refs": ["NICE", "SAMHSA", "SAFETY", "MERCK", "WHO"],
        "links": ["自殺リスク評価と安全確保", "精神科医療安全と危機対応", "精神科救急の基本構造"],
    },
    {
        "title": "自殺リスク評価と安全確保",
        "slug": "suicide-risk-assessment-and-safety",
        "aliases": ["自殺リスク", "安全計画"],
        "question": "自殺リスクを、恐れず、決めつけず、具体的に確認し安全へつなげる。",
        "lead": "自殺リスク評価は、希死念慮の有無を尋ねるだけではなく、意図、計画、手段、過去歴、苦痛、保護要因、直近の変化を統合する安全確保の実践である。",
        "points": [
            "自殺について尋ねること自体が自殺を誘発するという前提で避けるべきではない。",
            "リスク尺度の点数だけで退院・入院・観察水準を決めない。",
            "安全計画は本人と共同で作り、警告サイン、対処、連絡先、手段制限を含める。",
        ],
        "sections": [
            ("評価項目", "現在の希死念慮、具体的計画、準備行動、手段へのアクセス、過去の自殺企図、自傷、物質使用、精神病症状、絶望感、急な喪失を確認する。"),
            ("安全確保", "NICEは自傷後の心理社会的評価を重視し、リスク分類だけで処遇を決めないことを示している[11]。危険が切迫している場合は、本人を一人にしない、手段を遠ざける、救急・危機サービスと連携する。"),
            ("安全計画", "Stanleyらの安全計画介入は、警告サイン、内的対処、気をそらせる場所・人、支援者、専門窓口、致死的手段へのアクセス低減を共同で整理する[13]。これは契約書ではなく、危機時の実行可能な手順である。"),
        ],
        "refs": ["NICE", "SAFETY", "SAMHSA", "WHO", "MERCK"],
        "links": ["精神科リスク評価の基本", "精神科医療安全と危機対応", "精神科救急の基本構造"],
    },
    {
        "title": "精神科医療安全と危機対応",
        "slug": "psychiatric-patient-safety-and-crisis-response",
        "aliases": ["精神科医療安全", "危機対応"],
        "question": "危機を個人の問題だけでなく、環境・チーム・制度の安全設計として扱う。",
        "lead": "精神科医療安全は、自殺・暴力・離院・誤薬・身体合併症・拘束隔離・情報共有の失敗を、個人責任だけでなくシステムとして予防する視点である。",
        "points": [
            "危機対応では、落ち着いた関係形成、環境調整、身体評価、薬物・物質・せん妄の鑑別が重要である。",
            "最小制限原則と尊厳の保持は、安全確保と両立させる必要がある。",
            "チーム内の役割分担、記録、引き継ぎ、事後レビューが再発予防につながる。",
        ],
        "sections": [
            ("危機の見立て", "危機は単に『危険な患者』ではなく、苦痛、認知の混乱、物質使用、環境刺激、支援不足、医療側の対応が重なった状態として理解する。"),
            ("システム", "SAMHSAの危機ケア指針は、電話・チャット相談、モバイル危機対応、危機安定化サービスなどを連続体として位置づける[12]。医療機関内でも、単独対応を避け、出口と連絡手段を確保し、身体的緊急性を見落とさない。"),
            ("事後対応", "危機後には、本人の体験、チームの判断、環境要因、情報共有、次回の早期警告サインをレビューする。責めるためではなく、次の安全行動を具体化するために行う。"),
        ],
        "refs": ["SAMHSA", "NICE", "MERCK", "MSE", "WHO"],
        "links": ["精神科リスク評価の基本", "自殺リスク評価と安全確保", "精神科救急の基本構造"],
    },
    {
        "title": "ケースフォーミュレーション入門",
        "slug": "case-formulation-introduction",
        "aliases": ["ケースフォーミュレーション", "症例定式化"],
        "question": "診断名から一歩進み、なぜ今この人がこの困り方をしているのかを仮説化する。",
        "lead": "ケースフォーミュレーションは、診断、病歴、心理、身体、社会、リスク、強みを統合し、支援方針を導くための作業仮説である。",
        "points": [
            "代表的には4P、すなわち素因、誘発、維持、保護要因で整理する。",
            "定式化は正解探しではなく、本人と共有しながら更新する仮説である。",
            "診断名、症状、生活課題、治療目標をつなぐ橋渡しになる。",
        ],
        "sections": [
            ("4P", "素因は長期的脆弱性、誘発は発症や悪化のきっかけ、維持は問題を長引かせる要因、保護は回復を支える要因である。これを生物・心理・社会の列で整理すると、抜け漏れが見えやすい[7]。"),
            ("使い方", "たとえば同じ抑うつでも、睡眠相の乱れ、喪失体験、反すう、孤立、身体疾患、職場環境のどれが中心かで支援は変わる。"),
            ("限界", "フォーミュレーションは本人を説明し尽くす物語ではない。文化的背景や本人の価値を無視した専門家側の物語にならないよう、共同で修正する。"),
        ],
        "refs": ["ENGEL", "MERCK", "DSM", "ICD", "KJ"],
        "links": ["生物心理社会モデル", "精神科診断の意義と限界", "精神科病歴聴取の技法"],
    },
    {
        "title": "生物心理社会モデル",
        "slug": "biopsychosocial-model",
        "aliases": ["BPSモデル", "生物心理社会モデル"],
        "question": "生物・心理・社会を並べるだけでなく、相互作用として理解する。",
        "lead": "生物心理社会モデルは、健康と病を、身体過程、心理過程、社会環境が階層的・相互的に関わる現象として捉える枠組みである。",
        "points": [
            "Engelは、還元的な生物医学モデルだけでは患者の病い経験を十分に扱えないと論じた。",
            "精神医学では、遺伝・神経・睡眠・認知・感情・家族・労働・文化を同時に考える。",
            "『何でもあり』にしないためには、各水準で検証可能な仮説を置く必要がある。",
        ],
        "sections": [
            ("由来", "Engelの1977年論文は、生物医学モデルへの挑戦として、患者を身体だけでなく心理・社会的文脈の中で理解する必要を主張した[7]。"),
            ("精神医学での意味", "精神症状は、神経伝達物質や脳回路だけでなく、認知、トラウマ、対人関係、貧困、差別、文化的意味と結びつく。モデルは原因を一つに決めるためではなく、介入可能な水準を増やすために使う。"),
            ("注意点", "BPSモデルは便利なチェックリストに縮むと、説明力を失う。各要因がどの時間スケールで、どの症状や機能に関わるのかを明示することが重要である。"),
        ],
        "refs": ["ENGEL", "WHO", "MERCK", "KJ", "JAB"],
        "links": ["ケースフォーミュレーション入門", "精神医学とは何か", "精神科診断の意義と限界"],
    },
    {
        "title": "カテゴリ診断と次元モデル",
        "slug": "categorical-and-dimensional-models",
        "aliases": ["カテゴリ診断", "次元モデル"],
        "question": "精神疾患を『ある/ない』で分ける発想と、連続量として捉える発想を比較する。",
        "lead": "カテゴリ診断は臨床判断と制度運用に強く、次元モデルは症状の連続性や併存を捉えやすい。精神医学では両者を目的に応じて使い分ける。",
        "points": [
            "カテゴリは意思決定、研究登録、保険・福祉制度に使いやすい。",
            "次元は重症度、特性、症状スペクトラム、閾値下の困難を扱いやすい。",
            "多くの精神症状は明確な自然境界よりも連続性を示す。",
        ],
        "sections": [
            ("カテゴリの強み", "DSMやICDは、診断基準を満たすかどうかで共通言語を作る[2][3]。これは臨床コミュニケーションや制度利用に不可欠である。"),
            ("次元の強み", "症状の重症度、頻度、機能障害、特性を連続量として評価すると、閾値下の苦痛や併存を把握しやすい。RDoCは研究上、機能システムを次元的に扱う[4]。"),
            ("統合", "KendellとJablenskyが述べたように、妥当な分類には自然境界の検証が重要だが、多くの精神疾患では境界が曖昧である[5]。臨床ではカテゴリ診断に重症度・リスク・定式化を重ねる。"),
        ],
        "refs": ["DSM", "ICD", "RDOC", "KJ", "JAB"],
        "links": ["DSM・ICD・RDoCの違い", "精神科診断の意義と限界", "精神症候学入門"],
    },
    {
        "title": "精神症候学入門",
        "slug": "introduction-to-psychopathology",
        "aliases": ["精神症候学", "記述精神病理学"],
        "question": "症状名をラベルではなく、経験を精密に記述する語彙として学ぶ。",
        "lead": "精神症候学は、患者の主観的経験と観察可能な行動を、診断前のレベルで丁寧に記述するための学問である。",
        "points": [
            "症候は診断名に先立つ記述単位であり、同じ症候が複数の疾患・状態に現れる。",
            "幻覚、妄想、気分、不安、解離などは、内容だけでなく形式・確信度・文脈を評価する。",
            "身体疾患、薬物、文化、発達、トラウマを考慮する。",
        ],
        "sections": [
            ("なぜ必要か", "診断基準だけを読むと、症状がチェック項目に見える。しかし臨床では、患者がどのように体験しているか、どの程度現実検討が保たれるか、生活にどう影響するかが重要である。"),
            ("記述の単位", "Berriosは精神症状の歴史的形成を分析し、症候名が観察、言語、文化、理論の産物であることを示した[15]。したがって症候学は、用語を固定的に暗記するよりも、経験の差異を聞き分ける訓練である。"),
            ("臨床への接続", "MSEは症候学を面接記録に落とす器である[8]。症候を記述したうえで、DSM・ICD診断、リスク、フォーミュレーションへ進む。"),
        ],
        "refs": ["BERRIOS", "MSE", "CLINMSE", "DSM", "ICD"],
        "links": ["精神状態診察 MSE 入門", "幻覚とは何か", "妄想とは何か"],
    },
    {
        "title": "幻覚とは何か",
        "slug": "what-are-hallucinations",
        "aliases": ["幻覚", "hallucination"],
        "question": "幻覚を『ないものが見える』だけでなく、知覚様体験の構造として理解する。",
        "lead": "幻覚は、外界に対応する刺激がないにもかかわらず、知覚に似た生々しさと外在性をもって体験される現象である。",
        "points": [
            "幻覚は統合失調症だけでなく、気分障害、PTSD、解離、神経疾患、睡眠、物質、身体疾患でも起こりうる。",
            "評価では感覚様式、頻度、内容、苦痛、命令性、現実検討、リスクを確認する。",
            "文化的・宗教的体験や正常範囲の知覚体験との鑑別が必要である。",
        ],
        "sections": [
            ("定義", "幻覚は知覚体験としての性質をもつが、外部刺激に対応しない。MSEでは知覚の領域として記述される[8]。"),
            ("評価", "聴覚、視覚、嗅覚、体感などの様式、単純か複雑か、命令性、自他への危険、本人の解釈、睡眠・薬物・身体症状との関係を確認する。"),
            ("研究", "聴覚幻覚は統合失調症以外にも分布し、音声知覚、内言、自己モニタリング、予測処理、トラウマ記憶など複数モデルで研究されている[16]。"),
        ],
        "refs": ["HALL", "MSE", "DSM", "ICD", "BERRIOS"],
        "links": ["精神症候学入門", "妄想とは何か", "精神状態診察 MSE 入門"],
    },
    {
        "title": "妄想とは何か",
        "slug": "what-are-delusions",
        "aliases": ["妄想", "delusion"],
        "question": "妄想を、内容の奇異さだけでなく確信・訂正困難性・文脈から理解する。",
        "lead": "妄想は、文化的文脈に照らして共有されにくく、強い確信を伴い、反証によって容易に修正されない信念として記述される。",
        "points": [
            "妄想の評価では、内容よりも確信度、占有度、苦痛、行動化、現実検討を確認する。",
            "被害、関係、誇大、罪業、身体、嫉妬など多様な主題がある。",
            "文化、宗教、集団信念、トラウマ、実際の被害経験を慎重に区別する。",
        ],
        "sections": [
            ("定義", "DSM・ICDでは妄想は精神病症状の重要な構成要素として扱われる[2][3]。ただし、臨床では『間違った考え』と断じる前に、本人の背景と現実的根拠を確認する。"),
            ("評価", "確信の強さ、考えに費やす時間、反証への反応、生活上の影響、怒りや恐怖、他害・自傷リスク、幻覚との関係を聞く。"),
            ("形成モデル", "GaretyとFreemanは、妄想の形成に推論バイアス、情動、自己・他者スキーマ、異常体験の解釈が関わると論じた[17]。これは妄想を単なる内容異常ではなく、経験への意味づけとして見る視点を与える。"),
        ],
        "refs": ["DEL", "DSM", "ICD", "BERRIOS", "MSE"],
        "links": ["精神症候学入門", "幻覚とは何か", "精神状態診察 MSE 入門"],
    },
    {
        "title": "気分症状の見方",
        "slug": "assessing-mood-symptoms",
        "aliases": ["気分症状", "抑うつと躁"],
        "question": "気分を、主観的訴え、観察される感情、エピソード経過から評価する。",
        "lead": "気分症状の評価では、抑うつ、不快、興味低下、高揚、易怒性、活動性、睡眠、食欲、希死念慮を時間軸で捉える。",
        "points": [
            "気分は本人が述べる持続的な感情状態、感情は観察される表出として区別する。",
            "抑うつ症状では、快感消失、罪責感、認知・身体症状、自殺リスクを確認する。",
            "躁・軽躁では、高揚だけでなく易怒性、睡眠欲求低下、活動増加、浪費、危険行動を確認する。",
        ],
        "sections": [
            ("MSEでの位置", "MSEでは、気分は主観的報告、感情は観察可能な表情・声・反応の幅として記述する[8]。両者が一致するかも重要である。"),
            ("時間軸", "気分症状は一日の変動、持続期間、エピソード性、季節性、産後、物質・薬剤、身体疾患との関係を確認する。DSM・ICD診断では期間や症状数が基準化される[2][3]。"),
            ("リスク", "うつ病研究では抑うつが認知、身体、社会機能に広く影響することが示されている[18]。臨床では希死念慮、焦燥、混合状態、精神病症状、セルフネグレクトを見落とさない。"),
        ],
        "refs": ["MOOD", "MSE", "DSM", "ICD", "NICE"],
        "links": ["精神状態診察 MSE 入門", "自殺リスク評価と安全確保", "不安症状の見方"],
    },
    {
        "title": "不安症状の見方",
        "slug": "assessing-anxiety-symptoms",
        "aliases": ["不安症状", "不安"],
        "question": "不安を、危険予測、身体反応、回避、生活機能のパターンとして評価する。",
        "lead": "不安症状は、恐怖や心配だけでなく、動悸、過呼吸、緊張、確認、回避、安全行動として現れる。",
        "points": [
            "不安は適応的反応でもあり、問題になるのは過度、持続、制御困難、機能障害がある場合である。",
            "評価では対象、誘因、身体症状、回避、安全行動、発作性、予期不安を分ける。",
            "甲状腺疾患、不整脈、薬物、カフェイン、離脱、トラウマ反応を鑑別する。",
        ],
        "sections": [
            ("臨床像", "不安症は頻度が高く、恐怖条件づけ、脅威注意、回避、身体覚醒、認知的予測が関与する[19]。"),
            ("面接", "『何が怖いか』『何を避けるか』『避けると短期的に楽になるか』『生活の範囲が狭まっているか』を確認する。パニックでは発作のピーク、身体感覚への解釈、救急受診歴も重要である。"),
            ("MSEと診断", "MSEでは落ち着きなさ、発話速度、緊張、注意集中、気分、思考内容を記述する[8]。DSM・ICD診断は、症状のまとまりと持続期間、機能障害から判断される[2][3]。"),
        ],
        "refs": ["ANX", "MSE", "DSM", "ICD", "MERCK"],
        "links": ["気分症状の見方", "精神科面接の基本", "精神科病歴聴取の技法"],
    },
    {
        "title": "解離症状の見方",
        "slug": "assessing-dissociative-symptoms",
        "aliases": ["解離症状", "解離"],
        "question": "解離を、意識・記憶・自己感・身体感覚の統合が一時的にほどける現象として理解する。",
        "lead": "解離症状は、記憶の空白、離人感、現実感消失、同一性の変化、身体感覚の変容などとして現れる。",
        "points": [
            "解離はトラウマ関連症状でみられることが多いが、疲労、睡眠、物質、神経疾患でも鑑別が必要である。",
            "評価では、症状の始まり、誘因、時間経過、意識水準、記憶、危険行動、てんかん等を確認する。",
            "本人の体験を否定せず、現実検討と安全確保を同時に行う。",
        ],
        "sections": [
            ("現象", "離人感は自分から離れている感覚、現実感消失は周囲が現実でないように感じる体験である。解離性健忘では重要な自伝的情報の想起困難が問題になる。"),
            ("評価", "症状がいつ起こるか、どのくらい続くか、記憶の連続性、外傷想起、睡眠、物質使用、頭部外傷、てんかん、危険行動の有無を確認する。"),
            ("分類と限界", "SpiegelらはDSM-5における解離症群の整理を論じ、解離が単一現象ではなく複数の症候群を含むことを示した[20]。臨床では診断名よりも安全、安定化、生活機能の把握が先行する。"),
        ],
        "refs": ["DISS", "DSM", "ICD", "MSE", "MERCK"],
        "links": ["精神症候学入門", "精神科病歴聴取の技法", "精神科リスク評価の基本"],
    },
    {
        "title": "精神科救急の基本構造",
        "slug": "structure-of-psychiatric-emergency-care",
        "aliases": ["精神科救急", "危機介入"],
        "question": "精神科救急を、緊急度評価、身体鑑別、安全確保、継続支援への接続として理解する。",
        "lead": "精神科救急は、急性の精神症状や危機的行動に対し、身体的緊急性、リスク、意思決定能力、環境安全、継続ケアを短時間で統合する臨床場面である。",
        "points": [
            "まず生命危機、せん妄、物質、頭部外傷、代謝異常など身体要因を評価する。",
            "自殺・他害・セルフネグレクト・被害リスクを確認し、安全な場所と人員を確保する。",
            "救急対応の出口は、入院だけでなく、危機安定化、地域支援、外来、家族・支援者連携を含む。",
        ],
        "sections": [
            ("初期評価", "精神科救急では、バイタル、意識、せん妄、薬物・アルコール、身体疾患、外傷、服薬、妊娠可能性などを確認する。精神症状に見えても、医学的緊急事態が背景にあることがある。"),
            ("安全と関係", "落ち着いた声かけ、刺激の少ない環境、出口の確保、複数名対応、危険物確認を行う。暴力的行動だけでなく、本人が被害を受けやすい状況にも注意する。"),
            ("連続体", "SAMHSAは危機ケアを、相談窓口、モバイル対応、危機安定化、継続ケアを含む連続システムとして整理している[12]。救急の目的は、その場をしのぐだけでなく次の支援へつなぐことである。"),
        ],
        "refs": ["SAMHSA", "MERCK", "MSE", "NICE", "SAFETY"],
        "links": ["精神科医療安全と危機対応", "精神科リスク評価の基本", "自殺リスク評価と安全確保"],
    },
]


def slugify_title(title: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", title.lower()).strip("-")


def wrap_svg_text(lines, x, y, size=24, gap=34):
    return "\n".join(
        f'<text x="{x}" y="{y + i * gap}" font-size="{size}" fill="#15202b">{html.escape(line)}</text>'
        for i, line in enumerate(lines)
    )


def make_svg(article, kind):
    title = article["title"]
    if kind == 1:
        lines = ["中心問い", article["question"][:34], "見る水準", "症状・経過・機能・安全・文脈"]
        body = f"""
<rect x="38" y="46" width="824" height="100" rx="8" fill="#f5f7fb" stroke="#264653" stroke-width="3"/>
<text x="64" y="108" font-size="32" font-weight="700" fill="#0f172a">{html.escape(title)}</text>
<circle cx="210" cy="290" r="92" fill="#d8f3dc" stroke="#2d6a4f" stroke-width="3"/>
<circle cx="430" cy="290" r="92" fill="#ffe8cc" stroke="#bc6c25" stroke-width="3"/>
<circle cx="650" cy="290" r="92" fill="#dbeafe" stroke="#1d4ed8" stroke-width="3"/>
<text x="164" y="282" font-size="28" font-weight="700" fill="#123">記述</text>
<text x="384" y="282" font-size="28" font-weight="700" fill="#123">推論</text>
<text x="604" y="282" font-size="28" font-weight="700" fill="#123">支援</text>
<path d="M305 290 H335 M525 290 H555" stroke="#344054" stroke-width="5" marker-end="url(#arrow)"/>
{wrap_svg_text(lines, 80, 470, 22, 32)}
"""
    else:
        labels = ["聴く", "観察する", "鑑別する", "共有する", "更新する"]
        x_positions = [76, 234, 392, 550, 708]
        boxes = []
        for x, label in zip(x_positions, labels):
            boxes.append(f'<rect x="{x}" y="180" width="120" height="72" rx="8" fill="#fff" stroke="#457b9d" stroke-width="3"/>')
            boxes.append(f'<text x="{x+26}" y="225" font-size="24" font-weight="700" fill="#123">{label}</text>')
        arrows = "".join(f'<path d="M{x_positions[i]+120} 216 H{x_positions[i+1]}" stroke="#334155" stroke-width="4" marker-end="url(#arrow)"/>' for i in range(4))
        body = f"""
<rect x="38" y="46" width="824" height="100" rx="8" fill="#fff7ed" stroke="#9a3412" stroke-width="3"/>
<text x="64" y="108" font-size="30" font-weight="700" fill="#0f172a">{html.escape(title)}：臨床での使い方</text>
{''.join(boxes)}
{arrows}
<text x="76" y="330" font-size="23" fill="#15202b">この図は教育・研究目的の概念図であり、個別診断や治療指示ではない。</text>
<text x="76" y="380" font-size="23" fill="#15202b">診断名より先に、本人の語り、安全、生活機能、文脈を確認する。</text>
"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="900" height="560" viewBox="0 0 900 560">
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
    <path d="M0,0 L0,6 L9,3 z" fill="#334155"/>
  </marker>
</defs>
<rect width="900" height="560" fill="#ffffff"/>
{body}
</svg>
"""


def md(article):
    title = article["title"]
    slug = article["slug"]
    aliases = "\n".join(f'  - "{a}"' for a in article["aliases"])
    refs = "\n".join(SOURCES[k] for k in article["refs"])
    links = "\n".join(f"- [[{x}]]" for x in article["links"])
    points = "\n".join(f"- {p}" for p in article["points"])
    sections = "\n\n".join(f"## {h}\n\n{b}" for h, b in article["sections"])
    return f"""---
title: "{title}"
description: "{article['lead']}"
aliases:
{aliases}
tags:
  - 領域/精神医学
  - 種類/総論
  - 担当範囲/E
created: "{TODAY}"
updated: "{TODAY}"
draft: true
publish: false
status: draft
enableToc: true
---

# {title}

> このノートは教育・研究目的の概説であり、個別の診断、治療、危機対応の指示ではない。具体的な健康問題や切迫した危険がある場合は、地域の救急・専門機関につなぐ必要がある。

## このノートの問い

{article['question']}

## 先に結論

{article['lead']}

{points}

![{title}の概念マップ](../99_添付管理/{slug}/01_concept-map.svg)

{sections}

![{title}の臨床フロー](../99_添付管理/{slug}/02_clinical-flow.svg)

## よくある誤解

- 診断名や症状名は、本人の経験全体を説明し尽くすものではない。
- 精神症状は「気の持ちよう」でも「脳だけの問題」でもなく、身体、心理、環境、文化、時間経過の中で理解する。
- リスク評価は将来を当てる作業ではなく、今できる安全確保と支援調整を決める作業である。

## 関連ノート候補

{links}

## MOC更新候補

- `content/03_精神医学/MOC_精神医学.md` に追加候補。
- `content/03_精神医学/MOC_精神科診断と面接.md` に追加候補。

## 未解決問題

- 診断分類と個別事例の定式化を、教育現場でどの順序で教えるのがよいか。
- 文化差、制度差、当事者視点を、標準的な評価枠組みにどう組み込むか。
- 研究上の次元モデルを、日常臨床の意思決定へどこまで翻訳できるか。

## 参考文献

{refs}

## 更新ログ

- {TODAY}: 担当範囲Eの記事として初版作成。本文中引用、図解2点、関連ノート候補、MOC更新候補、未解決問題を追加。
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    ATT.mkdir(parents=True, exist_ok=True)
    for article in ARTICLES:
        slug = article["slug"]
        adir = ATT / slug
        adir.mkdir(parents=True, exist_ok=True)
        (adir / "01_concept-map.svg").write_text(make_svg(article, 1), encoding="utf-8")
        (adir / "02_clinical-flow.svg").write_text(make_svg(article, 2), encoding="utf-8")
        (OUT / f"{article['title']}.md").write_text(md(article), encoding="utf-8")
    print(f"generated {len(ARTICLES)} articles and {len(ARTICLES) * 2} diagrams")


if __name__ == "__main__":
    main()
