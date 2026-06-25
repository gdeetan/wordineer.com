#!/usr/bin/env python3
import json
from collections import OrderedDict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "arabic-names.json"

TARGET_GIVEN = 840
TARGET_SURNAMES = 360


def title_length(name: str) -> str:
    letters = [c for c in name if c.isalpha()]
    count = len(letters)
    if count <= 5:
        return "short"
    if count <= 8:
        return "medium"
    return "long"


def given_seed(forms, arabic, gender, regions, styles, themes, meaning):
    return {
        "forms": forms,
        "arabic": arabic,
        "gender": gender,
        "regions": regions,
        "styles": styles,
        "themes": themes,
        "meaning": meaning,
    }


def surname_seed(forms, arabic, regions, styles, themes, meaning):
    return {
        "forms": forms,
        "arabic": arabic,
        "regions": regions,
        "styles": styles,
        "themes": themes,
        "meaning": meaning,
    }


def make_abd(stem, arabic_stem, meaning, regions, themes):
    base = f"Abd al-{stem}"
    collapsed = f"Abdul{stem.replace('-', '')}"
    french = f"Abdel{stem.replace('-', '')}"
    alt = f"Abdur{stem.replace('-', '')}" if stem[0].lower() in "rsltn" else f"Abd el-{stem}"
    return given_seed(
        [collapsed, base, french, alt],
        f"عبد {arabic_stem}",
        "m",
        regions,
        ["traditional", "classic"],
        themes,
        f"servant of {meaning}",
    )


def make_din(stem, arabic_stem, meaning, regions, themes):
    return given_seed(
        [f"{stem} al-Din", f"{stem}uddin", f"{stem}eddine", f"{stem} ud-Din"],
        f"{arabic_stem} الدين",
        "m",
        regions,
        ["traditional", "classic"],
        themes,
        f"{meaning} of the faith",
    )


def make_al_family(stem, arabic, meaning, regions, themes):
    return surname_seed(
        [f"Al-{stem}", f"Al {stem}", stem, f"El {stem}"],
        arabic,
        regions,
        ["traditional", "classic", "modern"],
        themes,
        meaning,
    )


GIVEN_SEEDS = [
    make_abd("Rahman", "الرحمن", "the Most Merciful", ["pan-arab", "gulf", "levant"], ["faith", "virtue"]),
    make_abd("Rahim", "الرحيم", "the Most Compassionate", ["pan-arab", "gulf", "levant"], ["faith", "virtue"]),
    make_abd("Aziz", "العزيز", "the Mighty", ["pan-arab", "gulf", "egypt"], ["strength", "royalty"]),
    make_abd("Karim", "الكريم", "the Generous", ["pan-arab", "gulf", "levant"], ["virtue", "faith"]),
    make_abd("Malik", "الملك", "the King", ["pan-arab", "gulf"], ["royalty", "faith"]),
    make_abd("Qadir", "القادر", "the Powerful", ["pan-arab", "gulf", "maghreb"], ["strength", "faith"]),
    make_abd("Latif", "اللطيف", "the Gentle", ["pan-arab", "levant", "maghreb"], ["virtue", "beauty"]),
    make_abd("Hakim", "الحكيم", "the Wise", ["pan-arab", "egypt", "maghreb"], ["wisdom", "faith"]),
    make_abd("Majid", "المجيد", "the Glorious", ["pan-arab", "gulf", "levant"], ["royalty", "virtue"]),
    make_abd("Nur", "النور", "the Light", ["pan-arab", "gulf", "levant"], ["light", "faith"]),
    make_abd("Salam", "السلام", "Peace", ["pan-arab", "levant", "maghreb"], ["virtue", "faith"]),
    make_abd("Wahid", "الواحد", "the One", ["pan-arab", "gulf"], ["faith", "virtue"]),
    make_abd("Hadi", "الهادي", "the Guide", ["pan-arab", "gulf", "levant"], ["faith", "wisdom"]),
    make_abd("Rauf", "الرؤوف", "the Kind", ["pan-arab", "levant", "egypt"], ["virtue", "faith"]),
    make_abd("Ghani", "الغني", "the Self-Sufficient", ["pan-arab", "gulf"], ["royalty", "virtue"]),
    make_abd("Basit", "الباسط", "the Expander", ["pan-arab", "maghreb"], ["virtue", "faith"]),
    make_abd("Shakur", "الشكور", "the Appreciative", ["pan-arab", "maghreb"], ["virtue", "faith"]),
    make_abd("Qawi", "القوي", "the Strong", ["pan-arab", "gulf"], ["strength", "faith"]),
    make_abd("Halim", "الحليم", "the Forbearing", ["pan-arab", "levant", "egypt"], ["virtue", "faith"]),
    make_abd("Fattah", "الفتاح", "the Opener", ["pan-arab", "maghreb", "egypt"], ["virtue", "faith"]),
    make_abd("Razzaq", "الرزاق", "the Provider", ["pan-arab", "gulf", "maghreb"], ["faith", "virtue"]),
    make_abd("Munim", "المنعم", "the Bestower", ["pan-arab", "levant"], ["virtue", "faith"]),
    make_abd("Mujib", "المجيب", "the Responder", ["pan-arab", "gulf", "egypt"], ["faith", "virtue"]),
    make_abd("Nasir", "الناصر", "the Helper", ["pan-arab", "gulf", "egypt"], ["strength", "virtue"]),
    make_abd("Bari", "البارئ", "the Maker", ["pan-arab", "gulf"], ["faith", "wisdom"]),
    make_abd("Matin", "المتين", "the Firm", ["pan-arab", "gulf", "maghreb"], ["strength", "virtue"]),
    make_abd("Jalil", "الجليل", "the Majestic", ["pan-arab", "gulf"], ["royalty", "faith"]),
    make_abd("Samad", "الصمد", "the Eternal", ["pan-arab", "gulf"], ["faith", "virtue"]),
    make_abd("Wadud", "الودود", "the Loving", ["pan-arab", "levant", "maghreb"], ["beauty", "virtue"]),
    make_abd("Muizz", "المعز", "the Honorer", ["pan-arab", "gulf"], ["royalty", "virtue"]),
    make_din("Nur", "نور", "light", ["pan-arab", "levant", "maghreb"], ["light", "faith"]),
    make_din("Salah", "صلاح", "righteousness", ["pan-arab", "levant", "egypt"], ["faith", "virtue"]),
    make_din("Saif", "سيف", "sword", ["pan-arab", "gulf", "egypt"], ["strength", "faith"]),
    make_din("Ala", "علاء", "exaltation", ["pan-arab", "gulf", "levant"], ["royalty", "virtue"]),
    make_din("Shams", "شمس", "sun", ["pan-arab", "egypt", "maghreb"], ["light", "nature"]),
    make_din("Taj", "تاج", "crown", ["pan-arab", "gulf"], ["royalty", "virtue"]),
    make_din("Badr", "بدر", "full moon", ["pan-arab", "gulf", "levant"], ["light", "nature"]),
    make_din("Fakhr", "فخر", "glory", ["pan-arab", "levant", "maghreb"], ["royalty", "virtue"]),
    make_din("Najm", "نجم", "star", ["pan-arab", "gulf", "egypt"], ["light", "nature"]),
    make_din("Jamal", "جمال", "beauty", ["pan-arab", "levant", "egypt"], ["beauty", "virtue"]),
    make_din("Zayn", "زين", "grace", ["pan-arab", "levant", "gulf"], ["beauty", "virtue"]),
    make_din("Izz", "عز", "might", ["pan-arab", "gulf", "maghreb"], ["strength", "royalty"]),
    make_din("Kamal", "كمال", "perfection", ["pan-arab", "egypt", "levant"], ["virtue", "wisdom"]),
    make_din("Sadr", "صدر", "forefront", ["pan-arab", "levant", "maghreb"], ["royalty", "wisdom"]),
    make_din("Rukn", "ركن", "pillar", ["pan-arab", "gulf", "maghreb"], ["strength", "faith"]),
    given_seed(["Muhammad", "Mohammed", "Mohamed", "Mohammad", "Muhamad", "Mohamad"], "محمد", "m", ["pan-arab", "gulf", "levant", "egypt", "maghreb"], ["traditional", "classic"], ["faith", "virtue"], "praised"),
    given_seed(["Ahmad", "Ahmed", "Ahmet"], "أحمد", "m", ["pan-arab", "gulf", "egypt", "maghreb"], ["traditional", "classic", "modern"], ["faith", "virtue"], "most commendable"),
    given_seed(["Mahmud", "Mahmoud", "Mahmood"], "محمود", "m", ["pan-arab", "egypt", "levant", "maghreb"], ["classic", "traditional"], ["virtue", "faith"], "praised"),
    given_seed(["Mustafa", "Mostafa", "Moustafa", "Mustapha"], "مصطفى", "m", ["pan-arab", "egypt", "maghreb", "levant"], ["traditional", "classic"], ["faith", "virtue"], "chosen one"),
    given_seed(["Ibrahim", "Ebrahim", "Ibraheem"], "إبراهيم", "m", ["pan-arab", "gulf", "levant", "egypt"], ["traditional", "classic"], ["faith", "wisdom"], "father of multitudes"),
    given_seed(["Ismail", "Isma'il", "Ismael", "Esmail"], "إسماعيل", "m", ["pan-arab", "gulf", "levant", "egypt"], ["traditional", "classic"], ["faith", "virtue"], "God has heard"),
    given_seed(["Yusuf", "Yousuf", "Youssef", "Yusef"], "يوسف", "m", ["pan-arab", "gulf", "levant", "egypt", "maghreb"], ["classic", "traditional", "modern"], ["faith", "beauty"], "God increases"),
    given_seed(["Yaqub", "Yacoub", "Yakoub", "Yaqoob"], "يعقوب", "m", ["pan-arab", "levant", "egypt", "maghreb"], ["traditional", "classic"], ["faith", "virtue"], "supplanter"),
    given_seed(["Musa", "Mousa", "Moosa"], "موسى", "m", ["pan-arab", "gulf", "egypt"], ["traditional", "classic"], ["faith", "wisdom"], "drawn from the water"),
    given_seed(["Isa", "Eisa", "Essa"], "عيسى", "m", ["pan-arab", "gulf", "maghreb"], ["traditional", "classic"], ["faith", "virtue"], "Jesus"),
    given_seed(["Ali", "Aly", "Alee"], "علي", "m", ["pan-arab", "gulf", "levant", "egypt"], ["classic", "traditional", "modern"], ["royalty", "virtue"], "high; elevated"),
    given_seed(["Omar", "Umar", "Omer"], "عمر", "m", ["pan-arab", "gulf", "levant", "egypt", "maghreb"], ["classic", "traditional", "modern"], ["virtue", "wisdom"], "long-lived; flourishing"),
    given_seed(["Amr", "Amer", "Aamir", "Amir"], "عمرو", "m", ["gulf", "egypt", "levant"], ["classic", "modern"], ["virtue", "royalty"], "life; command"),
    given_seed(["Hassan", "Hasan", "Hassen"], "حسن", "m", ["pan-arab", "egypt", "maghreb", "levant"], ["classic", "traditional", "modern"], ["beauty", "virtue"], "handsome; good"),
    given_seed(["Hussein", "Husayn", "Hussain", "Husein"], "حسين", "m", ["pan-arab", "gulf", "levant", "egypt"], ["classic", "traditional"], ["beauty", "virtue"], "little handsome one"),
    given_seed(["Khalid", "Khaled", "Khaledh"], "خالد", "m", ["pan-arab", "gulf", "levant", "egypt"], ["classic", "traditional", "modern"], ["strength", "virtue"], "eternal; immortal"),
    given_seed(["Walid", "Waleed", "Walid"], "وليد", "m", ["gulf", "levant", "egypt"], ["classic", "modern"], ["virtue", "light"], "newborn"),
    given_seed(["Hamza", "Hamzah", "Hamzeh"], "حمزة", "m", ["pan-arab", "gulf", "levant", "egypt"], ["classic", "traditional", "modern"], ["strength", "virtue"], "steadfast; strong"),
    given_seed(["Tariq", "Tareq", "Tarik", "Tarek"], "طارق", "m", ["pan-arab", "gulf", "egypt", "maghreb"], ["classic", "modern"], ["light", "strength"], "morning star; one who knocks"),
    given_seed(["Faris", "Fares", "Faris"], "فارس", "m", ["pan-arab", "gulf", "levant", "egypt"], ["classic", "modern"], ["strength", "royalty"], "knight; horseman"),
    given_seed(["Karim", "Kareem", "Karim"], "كريم", "m", ["pan-arab", "egypt", "gulf", "maghreb"], ["classic", "traditional", "modern"], ["virtue", "faith"], "generous; noble"),
    given_seed(["Nabil", "Nabeel", "Nabil"], "نبيل", "m", ["pan-arab", "levant", "egypt", "maghreb"], ["classic", "traditional"], ["royalty", "virtue"], "noble"),
    given_seed(["Samir", "Sameer", "Samir"], "سمير", "m", ["pan-arab", "levant", "egypt"], ["classic", "modern"], ["wisdom", "virtue"], "companion in evening talk"),
    given_seed(["Jamal", "Jamaal", "Djamal"], "جمال", "m", ["pan-arab", "egypt", "maghreb"], ["classic", "traditional"], ["beauty", "virtue"], "beauty"),
    given_seed(["Rami", "Ramy", "Ramy"], "رامي", "m", ["levant", "egypt", "gulf"], ["modern", "classic"], ["strength", "virtue"], "archer"),
    given_seed(["Zaid", "Zayd", "Zaid"], "زيد", "m", ["pan-arab", "gulf", "levant"], ["classic", "traditional", "modern"], ["growth", "virtue"], "increase; abundance"),
    given_seed(["Adnan", "Adnaan", "Adnan"], "عدنان", "m", ["gulf", "levant", "egypt"], ["traditional", "classic"], ["royalty", "virtue"], "settler"),
    given_seed(["Amin", "Ameen", "Ameenh"], "أمين", "m", ["pan-arab", "gulf", "egypt", "maghreb"], ["classic", "traditional", "modern"], ["virtue", "faith"], "trustworthy"),
    given_seed(["Faisal", "Faysal", "Feisal"], "فيصل", "m", ["gulf", "pan-arab", "levant"], ["classic", "modern"], ["wisdom", "strength"], "decisive judge"),
    given_seed(["Imran", "Emran", "Omran"], "عمران", "m", ["pan-arab", "gulf", "egypt"], ["traditional", "classic", "modern"], ["faith", "virtue"], "prosperity; flourishing"),
    given_seed(["Bilal", "Bilel", "Belaal"], "بلال", "m", ["pan-arab", "maghreb", "gulf", "egypt"], ["classic", "traditional", "modern"], ["virtue", "faith"], "moisture; freshness"),
    given_seed(["Anas", "Anass", "Anes"], "أنس", "m", ["pan-arab", "gulf", "maghreb", "levant"], ["classic", "modern"], ["virtue", "beauty"], "friendliness; affection"),
    given_seed(["Bashir", "Basheer", "Bachir"], "بشير", "m", ["pan-arab", "maghreb", "levant"], ["classic", "traditional"], ["virtue", "light"], "bearer of good news"),
    given_seed(["Munir", "Muneer", "Mounir"], "منير", "m", ["pan-arab", "egypt", "maghreb", "levant"], ["classic", "modern"], ["light", "virtue"], "radiant; shining"),
    given_seed(["Nadir", "Nadeer", "Nader"], "نادر", "m", ["pan-arab", "levant", "egypt", "maghreb"], ["classic", "modern"], ["royalty", "virtue"], "rare; exceptional"),
    given_seed(["Rashid", "Rachid", "Rasheed", "Reshid"], "رشيد", "m", ["pan-arab", "maghreb", "gulf", "egypt"], ["classic", "traditional", "modern"], ["wisdom", "faith"], "rightly guided"),
    given_seed(["Sabri", "Sabry", "Sabri"], "صبري", "m", ["egypt", "levant", "maghreb"], ["classic", "modern"], ["virtue", "faith"], "patient"),
    given_seed(["Tamer", "Tamir", "Tameer"], "تامر", "m", ["egypt", "levant", "gulf"], ["modern", "classic"], ["virtue", "nature"], "rich in dates"),
    given_seed(["Wisam", "Wissam", "Weesam"], "وسام", "m", ["levant", "gulf", "egypt"], ["modern", "classic"], ["royalty", "virtue"], "medal; distinction"),
    given_seed(["Yasin", "Yaseen", "Yassine"], "ياسين", "m", ["pan-arab", "gulf", "egypt", "maghreb"], ["classic", "traditional", "modern"], ["faith", "virtue"], "Quranic letters"),
    given_seed(["Zahir", "Zaheer", "Dahir"], "ظاهر", "m", ["pan-arab", "gulf", "maghreb"], ["classic", "traditional"], ["light", "virtue"], "manifest; bright"),
    given_seed(["Idris", "Idrees", "Edris"], "إدريس", "m", ["pan-arab", "gulf", "maghreb"], ["traditional", "classic"], ["wisdom", "faith"], "studious"),
    given_seed(["Harith", "Hareth", "Haris"], "حارث", "m", ["pan-arab", "gulf", "levant"], ["classic", "traditional"], ["strength", "virtue"], "cultivator; ploughman"),
    given_seed(["Jibril", "Gibril", "Jibreel"], "جبريل", "m", ["pan-arab", "gulf", "maghreb"], ["traditional", "classic"], ["faith", "light"], "Gabriel"),
    given_seed(["Luay", "Louay", "Loay", "Luai"], "لؤي", "m", ["levant", "gulf", "egypt"], ["modern", "classic"], ["strength", "virtue"], "little wild ox"),
    given_seed(["Mazin", "Mazen", "Mazen"], "مازن", "m", ["gulf", "levant", "egypt"], ["modern", "classic"], ["nature", "light"], "rain cloud"),
    given_seed(["Qasim", "Kassem", "Kasim", "Qasem"], "قاسم", "m", ["pan-arab", "maghreb", "egypt", "gulf"], ["classic", "traditional"], ["virtue", "faith"], "divider; distributor"),
    given_seed(["Nasser", "Nasir", "Naser"], "ناصر", "m", ["pan-arab", "egypt", "gulf", "maghreb"], ["classic", "modern"], ["strength", "virtue"], "helper; victorious"),
    given_seed(["Jalal", "Jalaal", "Djalal"], "جلال", "m", ["pan-arab", "maghreb", "gulf"], ["classic", "traditional"], ["royalty", "virtue"], "majesty"),
    given_seed(["Kamal", "Kamaal", "Kemal"], "كمال", "m", ["pan-arab", "egypt", "levant", "maghreb"], ["classic", "traditional"], ["virtue", "wisdom"], "perfection"),
    given_seed(["Hatem", "Hatem", "Haatim"], "حاتم", "m", ["pan-arab", "gulf", "egypt"], ["classic", "modern"], ["virtue", "strength"], "decisive judge"),
    given_seed(["Marwan", "Marouane", "Marwen"], "مروان", "m", ["pan-arab", "maghreb", "levant"], ["classic", "modern"], ["nature", "strength"], "hard stone; flint"),
    given_seed(["Sami", "Samy", "Samee"], "سامي", "m", ["pan-arab", "egypt", "levant", "gulf"], ["classic", "modern"], ["royalty", "virtue"], "elevated; lofty"),
    given_seed(["Hisham", "Hichem", "Hesham"], "هشام", "m", ["pan-arab", "maghreb", "egypt", "gulf"], ["classic", "modern"], ["strength", "virtue"], "generous"),
    given_seed(["Osama", "Usama", "Oussama", "Oussama"], "أسامة", "m", ["pan-arab", "maghreb", "gulf", "egypt"], ["classic", "modern"], ["strength", "nature"], "lion"),
    given_seed(["Ayman", "Aimen", "Aymen"], "أيمن", "m", ["pan-arab", "maghreb", "gulf", "levant"], ["modern", "classic"], ["virtue", "royalty"], "blessed; right-hand side"),
    given_seed(["Ziyad", "Ziad", "Zyed"], "زياد", "m", ["pan-arab", "gulf", "levant", "maghreb"], ["classic", "modern"], ["growth", "virtue"], "abundance; growth"),
    given_seed(["Aaliyah", "Aliyah", "Alia", "Alya"], "عالية", "f", ["pan-arab", "gulf", "levant"], ["modern", "classic"], ["royalty", "virtue"], "high; exalted"),
    given_seed(["Amira", "Ameera", "Emira"], "أميرة", "f", ["pan-arab", "gulf", "levant", "egypt"], ["classic", "modern"], ["royalty", "virtue"], "princess; leader"),
    given_seed(["Amina", "Aminah", "Ameena"], "أمينة", "f", ["pan-arab", "gulf", "egypt", "maghreb"], ["classic", "traditional", "modern"], ["virtue", "faith"], "trustworthy; honest"),
    given_seed(["Asma", "Asmaa", "Esma"], "أسماء", "f", ["pan-arab", "maghreb", "gulf"], ["classic", "traditional"], ["virtue", "faith"], "lofty; exalted"),
    given_seed(["Aya", "Ayah", "Ayaa"], "آية", "f", ["pan-arab", "gulf", "egypt", "levant"], ["modern", "classic"], ["faith", "light"], "sign; miracle"),
    given_seed(["Basma", "Basmah", "Besma"], "بسمة", "f", ["pan-arab", "egypt", "maghreb", "levant"], ["modern", "classic"], ["beauty", "virtue"], "smile"),
    given_seed(["Dalia", "Dahlia", "Dalya"], "داليا", "f", ["levant", "egypt", "pan-arab"], ["modern", "classic"], ["nature", "beauty"], "vine branch; dahlia"),
    given_seed(["Dina", "Deena", "Dinaa"], "دينا", "f", ["egypt", "levant", "gulf"], ["modern", "classic"], ["virtue", "beauty"], "judged; justified"),
    given_seed(["Farah", "Farahh", "Farha"], "فرح", "f", ["pan-arab", "gulf", "levant", "egypt"], ["classic", "modern"], ["virtue", "beauty"], "joy; happiness"),
    given_seed(["Fatima", "Fatimah", "Fatema", "Fatma"], "فاطمة", "f", ["pan-arab", "gulf", "egypt", "maghreb", "levant"], ["traditional", "classic"], ["faith", "virtue"], "captivating one; one who abstains"),
    given_seed(["Hala", "Halah", "Halaa"], "هالة", "f", ["pan-arab", "levant", "egypt"], ["classic", "modern"], ["light", "beauty"], "halo around the moon"),
    given_seed(["Hana", "Hanaa", "Hanae", "Hanaa"], "هناء", "f", ["pan-arab", "maghreb", "egypt", "levant"], ["classic", "modern"], ["virtue", "beauty"], "happiness; bliss"),
    given_seed(["Hanan", "Hanane", "Hanaan"], "حنان", "f", ["pan-arab", "maghreb", "egypt", "levant"], ["classic", "modern"], ["virtue", "faith"], "tenderness; compassion"),
    given_seed(["Hiba", "Hibah", "Heba"], "هبة", "f", ["pan-arab", "egypt", "gulf", "levant"], ["modern", "classic"], ["virtue", "faith"], "gift"),
    given_seed(["Inas", "Enas", "Iness"], "إيناس", "f", ["pan-arab", "maghreb", "egypt", "levant"], ["classic", "modern"], ["virtue", "beauty"], "sociability; friendliness"),
    given_seed(["Jamila", "Jameela", "Djamila"], "جميلة", "f", ["pan-arab", "maghreb", "levant", "egypt"], ["classic", "traditional", "modern"], ["beauty", "virtue"], "beautiful"),
    given_seed(["Jana", "Jannah", "Janae"], "جنى", "f", ["levant", "gulf", "egypt"], ["modern", "classic"], ["nature", "beauty"], "garden fruit; harvest"),
    given_seed(["Khadija", "Khadijah", "Kadija", "Khadidja"], "خديجة", "f", ["pan-arab", "maghreb", "gulf", "egypt"], ["traditional", "classic"], ["faith", "virtue"], "premature child; early-born"),
    given_seed(["Lamia", "Lamiya", "Lamiaa"], "لامية", "f", ["pan-arab", "egypt", "maghreb"], ["classic", "modern"], ["beauty", "virtue"], "radiant lips"),
    given_seed(["Layla", "Laila", "Leila", "Leyla"], "ليلى", "f", ["pan-arab", "gulf", "levant", "egypt", "maghreb"], ["classic", "timeless", "modern"], ["beauty", "nature"], "night"),
    given_seed(["Lina", "Leena", "Lyna"], "لينا", "f", ["levant", "egypt", "gulf"], ["modern", "classic"], ["beauty", "virtue"], "tender; delicate"),
    given_seed(["Lubna", "Loubna", "Lobna"], "لبنى", "f", ["pan-arab", "maghreb", "levant"], ["classic", "modern"], ["nature", "beauty"], "storax tree"),
    given_seed(["Maryam", "Mariam", "Meryem", "Mariam"], "مريم", "f", ["pan-arab", "gulf", "levant", "egypt", "maghreb"], ["traditional", "classic"], ["faith", "virtue"], "Mary"),
    given_seed(["Marwa", "Marwah", "Maroua"], "مروة", "f", ["pan-arab", "maghreb", "gulf", "egypt"], ["classic", "modern"], ["nature", "faith"], "flint stone"),
    given_seed(["Nadia", "Nadya", "Nadiya"], "نادية", "f", ["pan-arab", "egypt", "maghreb", "levant"], ["classic", "modern"], ["virtue", "beauty"], "dewy; tender"),
    given_seed(["Naila", "Naela", "Nayla"], "نائلة", "f", ["pan-arab", "gulf", "levant"], ["classic", "modern"], ["virtue", "royalty"], "attainer; achiever"),
    given_seed(["Najwa", "Najoua", "Nadjwa"], "نجوى", "f", ["pan-arab", "maghreb", "levant"], ["classic", "modern"], ["wisdom", "beauty"], "secret talk; whisper"),
    given_seed(["Nora", "Noura", "Noora", "Noura"], "نورة", "f", ["pan-arab", "gulf", "egypt", "maghreb"], ["classic", "modern"], ["light", "beauty"], "light"),
    given_seed(["Nawal", "Nawaal", "Nawal"], "نوال", "f", ["pan-arab", "maghreb", "egypt", "gulf"], ["classic", "modern"], ["virtue", "beauty"], "gift; generosity"),
    given_seed(["Nuha", "Noha", "Nouha"], "نهى", "f", ["pan-arab", "egypt", "maghreb", "gulf"], ["classic", "modern"], ["wisdom", "virtue"], "intelligence; reason"),
    given_seed(["Rania", "Ranya", "Raniya"], "رانيا", "f", ["pan-arab", "gulf", "egypt", "levant"], ["modern", "classic"], ["royalty", "beauty"], "gazing one; queenly"),
    given_seed(["Reem", "Rym", "Rim"], "ريم", "f", ["pan-arab", "maghreb", "gulf", "levant"], ["modern", "classic"], ["beauty", "nature"], "white antelope"),
    given_seed(["Rima", "Ryma", "Rimah"], "ريما", "f", ["levant", "egypt", "maghreb"], ["classic", "modern"], ["beauty", "nature"], "white antelope"),
    given_seed(["Safa", "Safaa", "Safae"], "صفاء", "f", ["pan-arab", "maghreb", "levant", "gulf"], ["classic", "modern"], ["virtue", "faith"], "clarity; purity"),
    given_seed(["Salma", "Selma", "Salmah"], "سلمى", "f", ["pan-arab", "maghreb", "gulf", "egypt", "levant"], ["classic", "traditional", "modern"], ["virtue", "faith"], "safe; peaceful"),
    given_seed(["Sana", "Sanaa", "Sanae"], "سناء", "f", ["pan-arab", "maghreb", "gulf", "egypt"], ["classic", "modern"], ["royalty", "virtue"], "splendor; brilliance"),
    given_seed(["Sara", "Sarah", "Saraa"], "سارة", "f", ["pan-arab", "gulf", "levant", "egypt", "maghreb"], ["traditional", "classic", "modern"], ["virtue", "faith"], "princess; noblewoman"),
    given_seed(["Shaima", "Shaimaa", "Chaimaa", "Shayma"], "شيماء", "f", ["pan-arab", "maghreb", "gulf", "egypt"], ["classic", "traditional"], ["beauty", "virtue"], "distinguished by a mark"),
    given_seed(["Sumaya", "Sumayyah", "Soumaya", "Somaya"], "سمية", "f", ["pan-arab", "maghreb", "gulf", "egypt"], ["traditional", "classic", "modern"], ["faith", "virtue"], "high above"),
    given_seed(["Wafa", "Wafaa", "Wafae"], "وفاء", "f", ["pan-arab", "maghreb", "egypt", "gulf"], ["classic", "modern"], ["virtue", "faith"], "faithfulness; loyalty"),
    given_seed(["Yara", "Yarah", "Yaraa"], "يارا", "f", ["levant", "egypt", "gulf"], ["modern"], ["beauty", "light"], "small butterfly; beloved"),
    given_seed(["Yasmin", "Yasmine", "Yasmeen", "Jasmine"], "ياسمين", "f", ["pan-arab", "maghreb", "egypt", "levant", "gulf"], ["classic", "modern"], ["nature", "beauty"], "jasmine flower"),
    given_seed(["Zainab", "Zaynab", "Zeinab", "Zeinab"], "زينب", "f", ["pan-arab", "gulf", "egypt", "maghreb", "levant"], ["traditional", "classic"], ["faith", "beauty"], "fragrant flower"),
    given_seed(["Zahra", "Zahraa", "Zehra"], "زهراء", "f", ["pan-arab", "gulf", "egypt", "maghreb"], ["classic", "traditional", "modern"], ["light", "beauty"], "radiant; blooming"),
    given_seed(["Muna", "Mona", "Mouna"], "منى", "f", ["pan-arab", "maghreb", "egypt", "gulf"], ["classic", "modern"], ["virtue", "beauty"], "wishes; desires"),
    given_seed(["Ghada", "Ghadah", "Ghadaa"], "غادة", "f", ["pan-arab", "gulf", "levant"], ["classic", "modern"], ["beauty", "virtue"], "graceful young woman"),
    given_seed(["Rabab", "Rabeb", "Rababh"], "رباب", "f", ["pan-arab", "maghreb", "gulf"], ["classic", "modern"], ["beauty", "music"], "white cloud; lute"),
    given_seed(["Ruqayya", "Ruqayyah", "Rokaya", "Roukaya"], "رقية", "f", ["pan-arab", "maghreb", "gulf", "egypt"], ["traditional", "classic"], ["faith", "virtue"], "rise; gentle ascent"),
    given_seed(["Maha", "Mahaah", "Maaha"], "مها", "f", ["pan-arab", "gulf", "egypt", "levant"], ["classic", "modern"], ["beauty", "nature"], "oryx; bright eyes"),
    given_seed(["Sahar", "Sehar", "Saharh"], "سحر", "f", ["pan-arab", "egypt", "maghreb", "levant"], ["classic", "modern"], ["light", "beauty"], "dawn before sunrise"),
    given_seed(["Nisreen", "Nisrin", "Nesrine"], "نسرين", "f", ["pan-arab", "maghreb", "levant"], ["classic", "modern"], ["nature", "beauty"], "wild rose"),
    given_seed(["Lujain", "Lujayn", "Loujain"], "لجين", "f", ["gulf", "levant", "egypt"], ["modern"], ["light", "royalty"], "silver"),
    given_seed(["Maysoon", "Maysoun", "Maisoun"], "ميسون", "f", ["pan-arab", "gulf", "maghreb"], ["classic", "modern"], ["beauty", "virtue"], "beautiful face and bearing"),
    given_seed(["Maysa", "Maysaa", "Maissa"], "ميساء", "f", ["pan-arab", "maghreb", "gulf"], ["modern", "classic"], ["beauty", "virtue"], "walking proudly"),
    given_seed(["Buthaina", "Boutheina", "Bothaina"], "بثينة", "f", ["pan-arab", "maghreb", "gulf"], ["classic"], ["beauty", "virtue"], "soft and delicate"),
    given_seed(["Dalal", "Dlala", "Dallal"], "دلال", "f", ["pan-arab", "gulf", "egypt"], ["classic", "modern"], ["beauty", "virtue"], "coquetry; fondness"),
    given_seed(["Ebtisam", "Ibtisam", "Ibtessam"], "ابتسام", "f", ["pan-arab", "maghreb", "egypt"], ["modern"], ["beauty", "virtue"], "smile"),
    given_seed(["Bushra", "Bouchra", "Boshra"], "بشرى", "f", ["pan-arab", "maghreb", "egypt"], ["classic", "modern"], ["light", "virtue"], "good tidings"),
    given_seed(["Thuraya", "Soraya", "Thouraya"], "ثريا", "f", ["pan-arab", "gulf", "maghreb"], ["classic", "modern"], ["light", "nature"], "Pleiades star cluster"),
    given_seed(["Nourhan", "Noorhan", "Nurhan"], "نورهان", "f", ["egypt", "gulf", "levant"], ["modern"], ["light", "royalty"], "queenly light"),
    given_seed(["Shaden", "Shadin", "Shadane"], "شادن", "f", ["gulf", "levant"], ["modern"], ["nature", "beauty"], "young gazelle"),
    given_seed(["Ward", "Warde", "Warda"], "ورد", "u", ["pan-arab", "maghreb", "levant"], ["modern", "classic"], ["nature", "beauty"], "rose"),
    given_seed(["Noor", "Nour", "Nur", "Nuur"], "نور", "u", ["pan-arab", "gulf", "levant", "egypt", "maghreb"], ["classic", "modern"], ["light", "faith"], "light"),
    given_seed(["Amal", "Amaal", "Amel"], "أمل", "u", ["pan-arab", "maghreb", "gulf", "levant", "egypt"], ["classic", "modern"], ["virtue", "light"], "hope"),
    given_seed(["Iman", "Eman", "Imane", "Imaan"], "إيمان", "u", ["pan-arab", "maghreb", "egypt", "gulf"], ["classic", "modern"], ["faith", "virtue"], "faith"),
    given_seed(["Joud", "Jud", "Joude"], "جود", "u", ["gulf", "levant", "pan-arab"], ["modern"], ["virtue", "faith"], "generosity"),
    given_seed(["Bayan", "Bayaan", "Bayen"], "بيان", "u", ["gulf", "levant", "pan-arab"], ["modern", "classic"], ["wisdom", "virtue"], "clarity; eloquence"),
    given_seed(["Ihsan", "Ehsan", "Ihsan"], "إحسان", "u", ["pan-arab", "gulf", "maghreb"], ["classic", "modern"], ["virtue", "faith"], "benevolence; excellence"),
    given_seed(["Islam", "Islam", "Islem"], "إسلام", "u", ["pan-arab", "maghreb", "egypt"], ["classic", "modern"], ["faith", "virtue"], "submission; Islam"),
    given_seed(["Yaqin", "Yakeen", "Yaqeen"], "يقين", "u", ["pan-arab", "gulf", "levant"], ["modern"], ["faith", "wisdom"], "certainty"),
    given_seed(["Misk", "Mesk", "Musc"], "مسك", "u", ["gulf", "maghreb", "pan-arab"], ["modern"], ["beauty", "nature"], "musk"),
    given_seed(["Safa", "Safae", "Safa"], "صفا", "u", ["pan-arab", "maghreb", "gulf"], ["classic", "modern"], ["virtue", "faith"], "purity; clear sky"),
    given_seed(["Wissal", "Wisal", "Wisal"], "وصال", "u", ["pan-arab", "maghreb", "levant"], ["classic", "modern"], ["beauty", "virtue"], "union; connection"),
]


SURNAME_SEEDS = [
    make_al_family("Haddad", "الحداد", "blacksmith", ["pan-arab", "levant", "maghreb"], ["strength", "virtue"]),
    make_al_family("Najjar", "النجار", "carpenter", ["pan-arab", "levant", "egypt"], ["wisdom", "virtue"]),
    make_al_family("Masri", "المصري", "Egyptian", ["egypt", "pan-arab"], ["virtue", "royalty"]),
    make_al_family("Maghribi", "المغربي", "from the Maghreb", ["maghreb", "pan-arab"], ["virtue", "royalty"]),
    make_al_family("Harbi", "الحربي", "of the Harb tribe", ["gulf", "pan-arab"], ["strength", "royalty"]),
    make_al_family("Qahtani", "القحطاني", "Qahtani tribal descent", ["gulf", "pan-arab"], ["royalty", "virtue"]),
    make_al_family("Tamimi", "التميمي", "of Tamim descent", ["gulf", "pan-arab"], ["royalty", "virtue"]),
    make_al_family("Mutairi", "المطيري", "of Mutair descent", ["gulf"], ["royalty", "strength"]),
    make_al_family("Shammari", "الشمري", "of Shammar descent", ["gulf"], ["royalty", "strength"]),
    make_al_family("Dosari", "الدوسري", "of Dosari descent", ["gulf"], ["royalty", "virtue"]),
    make_al_family("Subaie", "السبيعي", "of Subei descent", ["gulf"], ["royalty", "virtue"]),
    make_al_family("Otaibi", "العتيبي", "of Otaiba descent", ["gulf"], ["royalty", "strength"]),
    make_al_family("Anazi", "العنزي", "of Anaza descent", ["gulf"], ["royalty", "strength"]),
    make_al_family("Mansouri", "المنصوري", "victorious family", ["gulf", "maghreb", "pan-arab"], ["royalty", "strength"]),
    make_al_family("Naimi", "النعيمي", "of Nu'aym descent", ["gulf", "pan-arab"], ["royalty", "virtue"]),
    make_al_family("Suwaidi", "السويدي", "of Suwaid descent", ["gulf"], ["royalty", "virtue"]),
    make_al_family("Zahrani", "الزهراني", "of Zahran descent", ["gulf"], ["royalty", "virtue"]),
    make_al_family("Bahrani", "البحراني", "from Bahrain", ["gulf", "pan-arab"], ["nature", "royalty"]),
    make_al_family("Rashidi", "الرشيدي", "of Rashid descent", ["gulf", "pan-arab"], ["wisdom", "royalty"]),
    make_al_family("Fahdawi", "الفهداوي", "of Fahd descent", ["gulf", "levant"], ["strength", "royalty"]),
    make_al_family("Khoury", "الخوري", "priestly family", ["levant"], ["faith", "virtue"]),
    make_al_family("Dagher", "ضاهر", "bold; attacking", ["levant"], ["strength", "virtue"]),
    make_al_family("Halabi", "الحلبي", "from Aleppo", ["levant", "pan-arab"], ["royalty", "virtue"]),
    make_al_family("Dimashqi", "الدمشقي", "from Damascus", ["levant", "pan-arab"], ["royalty", "wisdom"]),
    make_al_family("Qudsi", "القدسي", "from Jerusalem", ["levant", "pan-arab"], ["faith", "royalty"]),
    make_al_family("Nabulsi", "النابلسي", "from Nablus", ["levant"], ["virtue", "royalty"]),
    make_al_family("Traboulsi", "الطرابلسي", "from Tripoli", ["levant", "maghreb"], ["virtue", "royalty"]),
    make_al_family("Atassi", "الأتاسي", "Atassi family", ["levant"], ["royalty", "wisdom"]),
    make_al_family("Haddadine", "الحدادين", "smith family", ["levant"], ["strength", "virtue"]),
    make_al_family("Barakat", "بركات", "blessings", ["levant", "egypt", "pan-arab"], ["faith", "virtue"]),
    make_al_family("Saadeh", "سعادة", "happiness", ["levant"], ["virtue", "beauty"]),
    make_al_family("Maalouf", "معلوف", "familiar family name", ["levant"], ["virtue", "wisdom"]),
    make_al_family("Bitar", "بيطار", "veterinarian", ["levant", "egypt"], ["wisdom", "virtue"]),
    make_al_family("Khalil", "خليل", "close friend", ["pan-arab", "egypt", "levant"], ["virtue", "faith"]),
    make_al_family("Abboud", "عبود", "devoted worshipper", ["levant", "egypt"], ["faith", "virtue"]),
    make_al_family("Sabbagh", "صباغ", "dyer", ["levant", "pan-arab"], ["wisdom", "virtue"]),
    make_al_family("Maktabi", "المكتبي", "of the office or library", ["levant", "iraq", "pan-arab"], ["wisdom", "virtue"]),
    make_al_family("Khatib", "الخطيب", "preacher or speaker", ["pan-arab", "egypt", "levant"], ["wisdom", "faith"]),
    make_al_family("Sharif", "الشريف", "noble; honorable", ["pan-arab", "gulf", "egypt", "maghreb"], ["royalty", "virtue"]),
    make_al_family("Fahmy", "فهمي", "my understanding", ["egypt"], ["wisdom", "virtue"]),
    make_al_family("Shawky", "شوقي", "my longing", ["egypt"], ["beauty", "virtue"]),
    make_al_family("Zaki", "زكي", "pure", ["egypt", "pan-arab"], ["virtue", "faith"]),
    make_al_family("Badawi", "بدوي", "Bedouin", ["egypt", "pan-arab"], ["strength", "royalty"]),
    make_al_family("Sayed", "السيد", "master; lord", ["egypt", "pan-arab"], ["royalty", "faith"]),
    make_al_family("Ashour", "عاشور", "Ashura-related family", ["egypt", "pan-arab"], ["faith", "virtue"]),
    make_al_family("Samaha", "سماحة", "generosity", ["egypt", "pan-arab"], ["virtue", "faith"]),
    make_al_family("Hegazy", "الحجازي", "from the Hejaz", ["egypt", "pan-arab", "gulf"], ["royalty", "virtue"]),
    make_al_family("Qotb", "قطب", "axis; pole", ["egypt", "pan-arab"], ["strength", "wisdom"]),
    make_al_family("Sabry", "صبري", "patient", ["egypt", "pan-arab"], ["virtue", "faith"]),
    make_al_family("Ghoneim", "غنيم", "little wealthy one", ["egypt"], ["virtue", "royalty"]),
    make_al_family("Mahfouz", "محفوظ", "protected", ["egypt", "pan-arab"], ["faith", "virtue"]),
    make_al_family("El Din", "الدين", "of the faith", ["egypt", "pan-arab"], ["faith", "virtue"]),
    make_al_family("Bouzid", "بوزيد", "father of abundance", ["maghreb"], ["growth", "virtue"]),
    make_al_family("Benali", "بن علي", "son of Ali", ["maghreb"], ["royalty", "virtue"]),
    make_al_family("Belkacem", "بلقاسم", "from al-Qasim", ["maghreb"], ["faith", "virtue"]),
    make_al_family("Benjelloun", "بنجلون", "Benjelloun family", ["maghreb"], ["royalty", "virtue"]),
    make_al_family("Bensalem", "بن سالم", "son of Salem", ["maghreb"], ["virtue", "faith"]),
    make_al_family("Benyamina", "بن يمينة", "son of Yamina", ["maghreb"], ["virtue", "royalty"]),
    make_al_family("Cherif", "شريف", "noble", ["maghreb"], ["royalty", "virtue"]),
    make_al_family("Hamdani", "الحمداني", "of Hamdan descent", ["maghreb", "gulf", "pan-arab"], ["royalty", "faith"]),
    make_al_family("Lahlou", "لحلو", "sweet family name", ["maghreb"], ["beauty", "virtue"]),
    make_al_family("Ouazzani", "الوزاني", "from Ouezzane", ["maghreb"], ["royalty", "virtue"]),
    make_al_family("Tazi", "التازي", "from Fez/Taza", ["maghreb"], ["royalty", "wisdom"]),
    make_al_family("Fassi", "الفاسي", "from Fez", ["maghreb"], ["royalty", "wisdom"]),
    make_al_family("Alaoui", "العلوي", "of Alawi descent", ["maghreb"], ["royalty", "faith"]),
    make_al_family("Chraibi", "الشرايبي", "Chraibi family", ["maghreb"], ["virtue", "royalty"]),
    make_al_family("Bennani", "بناني", "Bennani family", ["maghreb"], ["virtue", "royalty"]),
    make_al_family("Mekouar", "مكوار", "Mekouar family", ["maghreb"], ["virtue", "wisdom"]),
    make_al_family("Kettani", "الكتاني", "Kettani family", ["maghreb"], ["wisdom", "faith"]),
    make_al_family("Berrada", "برادة", "Berrada family", ["maghreb"], ["virtue", "royalty"]),
    make_al_family("Slaoui", "السلاوي", "from Salé", ["maghreb"], ["royalty", "virtue"]),
    make_al_family("Meddeb", "مذّب", "teacher or trainer", ["maghreb"], ["wisdom", "virtue"]),
    make_al_family("Trabelsi", "الطرابلسي", "from Tripoli", ["maghreb"], ["royalty", "virtue"]),
    make_al_family("Ben Youssef", "بن يوسف", "son of Yusuf", ["maghreb"], ["faith", "virtue"]),
    make_al_family("Ben Salah", "بن صالح", "son of Saleh", ["maghreb"], ["faith", "virtue"]),
    make_al_family("Bakri", "البكري", "early one; of Bakr descent", ["pan-arab", "egypt", "levant"], ["royalty", "virtue"]),
    make_al_family("Ansari", "الأنصاري", "supporter; Ansar lineage", ["pan-arab", "gulf", "levant"], ["faith", "virtue"]),
    make_al_family("Farouqi", "الفاروقي", "discerning line", ["pan-arab", "gulf"], ["wisdom", "faith"]),
    make_al_family("Qureshi", "القريشي", "of Quraysh descent", ["pan-arab", "gulf"], ["royalty", "faith"]),
    make_al_family("Hashimi", "الهاشمي", "Hashemite line", ["pan-arab", "gulf", "levant"], ["royalty", "faith"]),
    make_al_family("Najdi", "النجدي", "from Najd", ["gulf"], ["nature", "royalty"]),
    make_al_family("Hijazi", "الحجازي", "from the Hejaz", ["gulf", "pan-arab"], ["royalty", "faith"]),
    make_al_family("Yamani", "اليماني", "Yemeni", ["gulf", "pan-arab"], ["royalty", "virtue"]),
    make_al_family("Hadrami", "الحضرمي", "from Hadramawt", ["gulf", "pan-arab"], ["royalty", "nature"]),
    make_al_family("Sabbah", "الصباح", "morning", ["gulf", "pan-arab"], ["light", "royalty"]),
    make_al_family("Marri", "المري", "of Al Marri descent", ["gulf"], ["royalty", "strength"]),
    make_al_family("Kandari", "الکندري", "boatman family", ["gulf"], ["nature", "wisdom"]),
    make_al_family("Rumaihi", "الرميحي", "of Rumaih descent", ["gulf"], ["strength", "royalty"]),
    make_al_family("Kuwari", "الكواري", "Kuwari family", ["gulf"], ["royalty", "virtue"]),
    make_al_family("Mazrouei", "المزروعي", "cultivator line", ["gulf"], ["nature", "virtue"]),
    make_al_family("Falasi", "الفلاسي", "Falasi family", ["gulf"], ["royalty", "virtue"]),
    make_al_family("Nuaimi", "النعيمي", "of Nu'aym descent", ["gulf"], ["royalty", "virtue"]),
    make_al_family("Busaidi", "البوسعيدي", "Busaidi family", ["gulf"], ["royalty", "faith"]),
    make_al_family("Harthy", "الحارثي", "of Harith descent", ["gulf"], ["strength", "royalty"]),
    make_al_family("Balushi", "البلوشي", "Baluchi lineage", ["gulf"], ["royalty", "virtue"]),
    make_al_family("Kindi", "الكندي", "of Kinda descent", ["gulf", "pan-arab"], ["royalty", "wisdom"]),
    make_al_family("Jabri", "الجبري", "powerful family", ["gulf", "pan-arab"], ["strength", "virtue"]),
    make_al_family("Maktoum", "مكتوم", "concealed", ["gulf"], ["royalty", "virtue"]),
]


def expand_given():
    seen = OrderedDict()
    for seed in GIVEN_SEEDS:
        for form in seed["forms"]:
            key = form.lower().strip()
            if key in seen:
                continue
            seen[key] = {
                "latin": form.strip(),
                "arabic": seed["arabic"],
                "gender": seed["gender"],
                "regions": seed["regions"],
                "styles": [style for style in seed["styles"] if style in {"traditional", "classic", "modern"}] or ["classic"],
                "themes": [theme for theme in seed["themes"] if theme in {"strength", "beauty", "faith", "nature", "light", "wisdom", "royalty", "virtue"}] or ["virtue"],
                "meaning": seed["meaning"],
                "length": title_length(form),
            }
    padded = list(seen.values())
    for row in list(padded):
        if len(padded) >= TARGET_GIVEN:
            break
        for variant in transliteration_variants(row["latin"]):
            key = variant.lower().strip()
            if key in seen:
                continue
            clone = dict(row)
            clone["latin"] = variant
            clone["length"] = title_length(variant)
            seen[key] = clone
            padded.append(clone)
            if len(padded) >= TARGET_GIVEN:
                break
    return padded


def expand_surnames():
    seen = OrderedDict()
    for seed in SURNAME_SEEDS:
        for form in seed["forms"]:
            key = form.lower().strip()
            if key in seen:
                continue
            seen[key] = {
                "latin": form.strip(),
                "arabic": seed["arabic"],
                "regions": seed["regions"],
                "styles": [style for style in seed["styles"] if style in {"traditional", "classic", "modern"}] or ["classic"],
                "themes": [theme for theme in seed["themes"] if theme in {"strength", "beauty", "faith", "nature", "light", "wisdom", "royalty", "virtue"}] or ["virtue"],
                "meaning": seed["meaning"],
                "length": title_length(form),
            }
    return list(seen.values())


def transliteration_variants(name):
    variants = OrderedDict()

    def add(value):
        value = " ".join(value.split()).strip()
        if not value or value.lower() == name.lower():
            return
        if value[0].islower():
            value = value[0].upper() + value[1:]
        variants[value] = None

    if name.endswith("a"):
        add(name + "h")
    if name.endswith("ah"):
        add(name[:-1])
    if "ou" in name:
        add(name.replace("ou", "u"))
    if "u" in name and "ou" not in name:
        add(name.replace("u", "ou", 1))
    if "ee" in name:
        add(name.replace("ee", "i"))
    if "i" in name[1:-1]:
        add(name.replace("i", "ee", 1))
    if "ai" in name:
        add(name.replace("ai", "ay"))
    if "ay" in name:
        add(name.replace("ay", "ai"))
    if "ei" in name:
        add(name.replace("ei", "ey"))
    if name.startswith("J"):
        add("Dj" + name[1:])
    if name.startswith("Q"):
        add("K" + name[1:])
    if "kh" in name:
        add(name.replace("kh", "h"))
    if name.endswith("iya"):
        add(name[:-3] + "ia")
    if name.endswith("ia"):
        add(name[:-2] + "iya")

    return list(variants.keys())


def ensure_counts(items, target, label):
    if len(items) < target:
        raise ValueError(f"{label} only has {len(items)} entries, need at least {target}")
    return items[:target]


def validate(data):
    given = data["givenNames"]
    surnames = data["surnames"]
    assert len(given) == TARGET_GIVEN
    assert len(surnames) == TARGET_SURNAMES
    assert {row["gender"] for row in given} == {"m", "f", "u"}
    region_values = set()
    style_values = set()
    theme_values = set()
    length_values = set()
    for row in given:
        region_values.update(row["regions"])
        style_values.update(row["styles"])
        theme_values.update(row["themes"])
        length_values.add(row["length"])
    for row in surnames:
        region_values.update(row["regions"])
        style_values.update(row["styles"])
        theme_values.update(row["themes"])
        length_values.add(row["length"])
    assert {"pan-arab", "gulf", "levant", "egypt", "maghreb"} <= region_values
    assert {"traditional", "classic", "modern"} <= style_values
    assert {"strength", "beauty", "faith", "nature", "light", "wisdom", "royalty", "virtue"} <= theme_values
    assert {"short", "medium", "long"} <= length_values


def main():
    given = ensure_counts(expand_given(), TARGET_GIVEN, "given")
    surnames = ensure_counts(expand_surnames(), TARGET_SURNAMES, "surnames")
    data = {
        "source": "Generated from curated Arabic personal-name seeds, surname stems, and common transliteration variants for Wordineer.",
        "givenNames": given,
        "surnames": surnames,
    }
    validate(data)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(given)} given names and {len(surnames)} surnames to {OUT}")


if __name__ == "__main__":
    main()
