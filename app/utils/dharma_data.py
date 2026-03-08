"""
Dharma Data — Buddhist scripture collection for Dharma RAG.

Includes: Heart Sutra, Diamond Sutra, Dhammapada, and more.
Languages: Vietnamese, Pali, English, Myanmar, Khmer.
"""

import os
import json
import logging

logger = logging.getLogger("budai.dharma")

DHARMA_TEXTS = [
    # ─── Bát Nhã Tâm Kinh (Heart Sutra) ───
    {
        "name": "bat_nha_tam_kinh_vi.txt",
        "lang": "vi",
        "category": "kinh",
        "title": "Bát Nhã Ba La Mật Đa Tâm Kinh",
        "tradition": "Mahayana",
        "content": """BÁT NHÃ BA LA MẬT ĐA TÂM KINH
(Prajñāpāramitā Hṛdaya Sūtra)

Khi Ngài Quán Tự Tại Bồ Tát thực hành Bát Nhã Ba La Mật Đa sâu xa, Ngài soi thấy năm uẩn đều không, qua hết thảy khổ ách.

Này Xá Lợi Phất! Sắc chẳng khác không, không chẳng khác sắc. Sắc tức thị không, không tức thị sắc. Thọ, tưởng, hành, thức cũng đều như vậy.

Này Xá Lợi Phất! Tướng không của các pháp, không sinh, không diệt, không dơ, không sạch, không tăng, không giảm.

Cho nên trong chân không, không có sắc, không có thọ, tưởng, hành, thức. Không có mắt, tai, mũi, lưỡi, thân, ý. Không có sắc, thanh, hương, vị, xúc, pháp. Không có nhãn giới, cho đến không có ý thức giới. Không có vô minh, cũng không có hết vô minh. Cho đến không có già chết, cũng không có hết già chết.

Không có khổ, tập, diệt, đạo. Không có trí tuệ, cũng không có chứng đắc. Vì không có chỗ chứng đắc.

Bồ Tát y theo Bát Nhã Ba La Mật Đa, nên tâm không bị ngăn ngại. Vì không bị ngăn ngại nên không sợ hãi, xa lìa mộng tưởng điên đảo, đạt đến Niết Bàn cứu cánh.

Ba đời chư Phật y theo Bát Nhã Ba La Mật Đa, nên đắc Vô Thượng Chánh Đẳng Chánh Giác.

Cho nên biết Bát Nhã Ba La Mật Đa là đại thần chú, là đại minh chú, là vô thượng chú, là vô đẳng đẳng chú, có thể trừ tất cả khổ, chân thật không hư.

Nên nói chú Bát Nhã Ba La Mật Đa, liền nói chú rằng:

Yết đế, yết đế, ba la yết đế, ba la tăng yết đế, bồ đề tát bà ha.
(Gate gate pāragate pārasaṃgate bodhi svāhā)""",
    },
    {
        "name": "heart_sutra_en.txt",
        "lang": "en",
        "category": "sutra",
        "title": "Heart Sutra (Prajñāpāramitā Hṛdaya)",
        "tradition": "Mahayana",
        "content": """THE HEART OF THE PERFECTION OF WISDOM SUTRA

When Avalokiteśvara Bodhisattva was practicing the profound Prajñāpāramitā, he illuminated the five aggregates and saw that they are all empty, and he crossed beyond all suffering and difficulty.

Śāriputra, form does not differ from emptiness; emptiness does not differ from form. Form itself is emptiness; emptiness itself is form. So too are feeling, cognition, formation, and consciousness.

Śāriputra, all dharmas are marked with emptiness. They do not appear or disappear, are not tainted or pure, do not increase or decrease.

Therefore, in emptiness there is no form, feeling, cognition, formation, or consciousness; no eyes, ears, nose, tongue, body, or mind; no color, sound, smell, taste, touch, or dharma; no realm of eyes until no realm of mind consciousness.

There is no ignorance and also no ending of ignorance, until no old age and death and also no ending of old age and death. There is no suffering, no origination, no stopping, no path, no cognition, also no attainment with nothing to attain.

The Bodhisattva depends on Prajñāpāramitā and the mind is no hindrance. Without any hindrance no fears exist. Far apart from every inverted view one dwells in Nirvāṇa.

In the three worlds all Buddhas depend on Prajñāpāramitā and attain Anuttarā Samyaksaṃbodhi.

Therefore know that Prajñāpāramitā is the great transcendent mantra, the great bright mantra, the supreme mantra, the incomparable mantra, which is able to relieve all suffering, and is true not false.

So proclaim the Prajñāpāramitā mantra:
Gate gate pāragate pārasaṃgate bodhi svāhā.""",
    },
    # ─── Kim Cương Kinh (Diamond Sutra) ───
    {
        "name": "kim_cuong_kinh_vi.txt",
        "lang": "vi",
        "category": "kinh",
        "title": "Kim Cương Bát Nhã Ba La Mật Đa Kinh (trích)",
        "tradition": "Mahayana",
        "content": """KIM CƯƠNG BÁT NHÃ BA LA MẬT ĐA KINH
(Vajracchedikā Prajñāpāramitā Sūtra — Trích)

Phẩm 1: Nguyên Do

Tôi nghe như vầy: Một thời, Phật ở thành Xá Vệ, nơi vườn Kỳ Thọ Cấp Cô Độc, cùng với một nghìn hai trăm năm mươi vị đại Tỳ Kheo.

Phẩm 2: Thiện Hiện Khải Thỉnh

Trưởng lão Tu Bồ Đề, ở trong đại chúng, từ chỗ ngồi đứng dậy, trịch áo vai bên phải, gối phải quỳ sát đất, chắp tay cung kính mà bạch Phật rằng: "Thế Tôn, Như Lai khéo hộ niệm các Bồ Tát, khéo phó chúc các Bồ Tát. Thế Tôn, người thiện nam, người thiện nữ, phát tâm Vô Thượng Chánh Đẳng Chánh Giác, nên trụ tâm như thế nào, nên hàng phục tâm như thế nào?"

Phẩm 14: Ly Tướng Tịch Diệt

"Phàm cái gì có tướng, đều là hư vọng. Nếu thấy các tướng chẳng phải tướng, tức thấy Như Lai."

Phẩm 26: Pháp Thân Phi Tướng

"Nếu dùng sắc thấy ta, dùng âm thanh cầu ta, người ấy hành đạo tà, không thể thấy Như Lai."

Phẩm 32: Ứng Hóa Phi Chân

"Tất cả pháp hữu vi,
Như mộng, huyễn, bọt, bóng,
Như sương, cũng như chớp,
Nên quán chiếu như vậy."

(Nhất thiết hữu vi pháp,
Như mộng huyễn bào ảnh,
Như lộ diệc như điện,
Ưng tác như thị quán.)""",
    },
    # ─── Kinh Pháp Cú (Dhammapada) ───
    {
        "name": "phap_cu_vi.txt",
        "lang": "vi",
        "category": "kinh",
        "title": "Kinh Pháp Cú (Dhammapada — Trích)",
        "tradition": "Theravada",
        "content": """KINH PHÁP CÚ (DHAMMAPADA — Trích)

PHẨM SONG YẾU (Yamaka Vagga)

1. Tâm dẫn đầu các pháp,
   Tâm là chủ, tâm tạo.
   Nếu với tâm ô nhiễm,
   Nói lên hay hành động,
   Khổ não bước theo sau,
   Như xe, chân vật kéo.

2. Tâm dẫn đầu các pháp,
   Tâm là chủ, tâm tạo.
   Nếu với tâm thanh tịnh,
   Nói lên hay hành động,
   An lạc bước theo sau,
   Như bóng, không rời hình.

PHẨM TINH CẦN (Appamāda Vagga)

21. Tinh cần là đường sống,
    Buông lung là đường chết.
    Tinh cần là bất tử,
    Buông lung là tử vong.

PHẨM TÂM Ý (Citta Vagga)

33. Tâm hoảng hốt, dao động,
    Khó hộ trì, khó nhiếp,
    Người trí làm tâm thẳng,
    Như thợ tên, nắn tên.

35. Tâm xao động, bất thường,
    Khó kiểm soát, khó điều.
    Người trí điều phục tâm,
    Như thợ tên, nắn tên.

PHẨM HOA (Puppha Vagga)

51. Như đoá hoa tươi đẹp,
    Có sắc nhưng không hương,
    Lời nói khéo mà không
    Thực hành, cũng như vậy.

52. Như đoá hoa tươi đẹp,
    Có sắc lại thêm hương,
    Lời nói khéo, thực hành
    Kết quả tốt đẹp thay.

PHẨM PHẬT ĐÀ (Buddha Vagga)

183. Không làm mọi điều ác,
     Thành tựu các hạnh lành,
     Tự thanh lịnh ý chí,
     Là lời chư Phật dạy.

PHẨM AN LẠC (Sukha Vagga)

197. Vui thay, chúng ta sống,
     Không hận, giữa hận thù.
     Giữa những người thù hận,
     Ta sống, không hận thù.

198. Vui thay, chúng ta sống,
     Không bệnh, giữa ốm đau.
     Giữa những người bệnh hoạn,
     Ta sống, không ốm đau.

199. Vui thay, chúng ta sống,
     Không tham, giữa tham lam.
     Giữa những người tham lam,
     Ta sống, không tham lam.""",
    },
    {
        "name": "dhammapada_pali_en.txt",
        "lang": "pi-en",
        "category": "sutra",
        "title": "Dhammapada (Pali-English)",
        "tradition": "Theravada",
        "content": """DHAMMAPADA — The Path of Truth

Chapter 1: Yamaka Vagga (Twin Verses)

1. Manopubbaṅgamā dhammā, manoseṭṭhā manomayā.
   Manasā ce paduṭṭhena, bhāsati vā karoti vā,
   Tato naṃ dukkhamanveti, cakkaṃva vahato padaṃ.

   Mind is the forerunner of all actions.
   All deeds are led by mind, created by mind.
   If one speaks or acts with a corrupt mind,
   suffering follows, as the wheel follows the hoof.

2. Manopubbaṅgamā dhammā, manoseṭṭhā manomayā.
   Manasā ce pasannena, bhāsati vā karoti vā,
   Tato naṃ sukhamanveti, chāyāva anapāyinī.

   Mind is the forerunner of all actions.
   All deeds are led by mind, created by mind.
   If one speaks or acts with a pure mind,
   happiness follows, as a shadow that never departs.

Chapter 14: Buddha Vagga (The Buddha)

183. Sabbapāpassa akaraṇaṃ, kusalassa upasampadā,
     Sacittapariyodapanaṃ, etaṃ buddhāna sāsanaṃ.

     Not to do any evil, to cultivate good,
     to purify one's mind — this is the teaching of the Buddhas.

Chapter 15: Sukha Vagga (Happiness)

197. Susukhaṃ vata jīvāma, verinesu averino.
     Verinesu manussesu, viharāma averino.

     Happy indeed we live, friendly amidst the hostile.
     Amidst hostile people we dwell free from hatred.""",
    },
    # ─── Tứ Diệu Đế & Bát Chánh Đạo ───
    {
        "name": "tu_dieu_de_vi.txt",
        "lang": "vi",
        "category": "giao_ly",
        "title": "Tứ Diệu Đế và Bát Chánh Đạo",
        "tradition": "Chung",
        "content": """TỨ DIỆU ĐẾ (Cattāri Ariyasaccāni — Bốn Sự Thật Cao Quý)

1. KHỔ ĐẾ (Dukkha) — Sự thật về khổ
Sinh là khổ, già là khổ, bệnh là khổ, chết là khổ. Sầu, bi, khổ, ưu, não là khổ. Cầu không được là khổ. Tóm lại, năm uẩn thủ là khổ.

2. TẬP ĐẾ (Samudaya) — Sự thật về nguồn gốc của khổ
Đó là Ái (tanha - khát khao), dẫn đến tái sinh, cùng với hỷ và tham, tìm sự khoái lạc khắp nơi. Gồm: Dục ái, Hữu ái, Phi hữu ái.

3. DIỆT ĐẾ (Nirodha) — Sự thật về sự chấm dứt khổ
Đó là sự diệt tận, buông bỏ, từ bỏ, giải thoát, không chấp trước Ái.

4. ĐẠO ĐẾ (Magga) — Con đường dẫn tới chấm dứt khổ
Đó là Bát Chánh Đạo (Noble Eightfold Path):

BÁT CHÁNH ĐẠO (Aṭṭhaṅgika Magga)

🧠 TUỆ HỌC (Paññā)
1. Chánh Kiến (Sammā Diṭṭhi) — Hiểu biết đúng đắn
   Hiểu Tứ Diệu Đế, hiểu nhân quả, hiểu vô thường.

2. Chánh Tư Duy (Sammā Saṅkappa) — Suy nghĩ đúng đắn
   Từ bỏ tham dục, sân hận, hại người.

🗣️ GIỚI HỌC (Sīla)
3. Chánh Ngữ (Sammā Vācā) — Lời nói đúng đắn
   Không nói dối, không nói chia rẽ, không nói thô ác, không nói phù phiếm.

4. Chánh Nghiệp (Sammā Kammanta) — Hành động đúng đắn
   Không sát sinh, không trộm cắp, không tà dâm.

5. Chánh Mạng (Sammā Ājīva) — Sinh kế đúng đắn
   Không nghề nghiệp gây hại cho chúng sinh.

🧘 ĐỊNH HỌC (Samādhi)
6. Chánh Tinh Tấn (Sammā Vāyāma) — Nỗ lực đúng đắn
   Ngăn ác, diệt ác, phát thiện, tăng trưởng thiện.

7. Chánh Niệm (Sammā Sati) — Chánh niệm
   Quán thân, thọ, tâm, pháp. Tỉnh giác trong mọi hành động.

8. Chánh Định (Sammā Samādhi) — Tập trung đúng đắn
   Tứ thiền: Sơ thiền → Nhị thiền → Tam thiền → Tứ thiền.

NGŨ GIỚI (Pañca Sīla — Năm Giới Cơ Bản)
1. Không sát sinh (Pāṇātipātā veramaṇī)
2. Không trộm cắp (Adinnādānā veramaṇī)
3. Không tà dâm (Kāmesu micchācārā veramaṇī)
4. Không nói dối (Musāvādā veramaṇī)
5. Không dùng chất gây nghiện (Surāmeraya-majja-pamādaṭṭhānā veramaṇī)""",
    },
    # ─── Myanmar Buddhist Text ───
    {
        "name": "dhammapada_my.txt",
        "lang": "my",
        "category": "sutra",
        "title": "ဓမ္မပဒ (Dhammapada Myanmar)",
        "tradition": "Theravada",
        "content": """ဓမ္မပဒ — တရားလမ်း

ယမက ဝဂ် (အတွဲအကျဉ်း)

၁။ စိတ်သည် ခပ်သိမ်းသော တရားတို့၏ ရှေ့ဆောင်ဖြစ်၏၊
   စိတ်သည် အကြီးအမှူး ဖြစ်၏၊
   စိတ်ဖြင့် ဖြစ်စေအပ်ကုန်၏။
   ညစ်နွမ်းသော စိတ်ဖြင့် ပြောမူ ပြုမူအံ့၊
   ထိုသူကို ဒုက္ခသည် နောက်သို့ လိုက်၏၊
   ဥပမာသော် ဘီးသည် နွားခြေကို
   လိုက်သကဲ့သို့ ဖြစ်၏။

၂။ စိတ်သည် ခပ်သိမ်းသော တရားတို့၏ ရှေ့ဆောင်ဖြစ်၏၊
   ကြည်လင်သော စိတ်ဖြင့် ပြောမူ ပြုမူအံ့၊
   ထိုသူကို ချမ်းသာသည် နောက်သို့ လိုက်၏၊
   အရိပ်ကဲ့သို့ မကွာမခွါ လိုက်၏။

ဗုဒ္ဓ ဝဂ်

၁၈၃။ မကောင်းမှု ဟူ
သမျှကို မပြုရ၊ ကုသိုလ်ကောင်းမှုကို ဆည်းပူးရ၊
ကိုယ့်စိတ်ကို စင်ကြယ်အောင် ပြု
ရ၊ ဤသည်ကား ဘုရားတို့၏ အဆုံးအမ
ဖြစ်၏။""",
    },
    # ─── Khmer Buddhist Text ───
    {
        "name": "dhammapada_km.txt",
        "lang": "km",
        "category": "sutra",
        "title": "ធម្មបទ (Dhammapada Khmer)",
        "tradition": "Theravada",
        "content": """ធម្មបទ — ផ្លូវនៃធម៌

យមកវគ្គ (គាថាគូ)

១. ចិត្តជាប្រធាននៃធម៌ទាំងអស់
   ចិត្តជាមេ ចិត្តបង្កើត។
   បើនិយាយ ឬធ្វើអំពើ
   ដោយចិត្តកខ្វក់
   ទុក្ខនឹងដើរតាមបុគ្គលនោះ
   ដូចកង់រទេះដើរតាមជើងសត្វដែលលាក់។

២. ចិត្តជាប្រធាននៃធម៌ទាំងអស់
   ចិត្តជាមេ ចិត្តបង្កើត។
   បើនិយាយ ឬធ្វើអំពើ
   ដោយចិត្តជ្រះថ្លា
   សុខនឹងដើរតាមបុគ្គលនោះ
   ដូចស្រមោលមិនឃ្លាតចេញពីខ្លួន។

ពុទ្ធវគ្គ

១៨៣. ការមិនធ្វើអំពើអាក្រក់ទាំងអស់
     ការប្រកបរឿងល្អ
     ការបន្សុទ្ធចិត្តឱ្យស្អាត
     នេះជាពាក្យប្រដៅរបស់ព្រះពុទ្ធទាំងអស់។""",
    },
    # ─── Thiền / Meditation Guide ───
    {
        "name": "thien_dinh_vi.txt",
        "lang": "vi",
        "category": "thien",
        "title": "Hướng Dẫn Thiền Định Cơ Bản",
        "tradition": "Chung",
        "content": """HƯỚNG DẪN THIỀN ĐỊNH CƠ BẢN

1. THIỀN CHỈ (Samatha — Meditation for Calm)

Mục đích: Đạt sự an tĩnh, tập trung tâm ý.

Phương pháp Ānāpānasati (Quán niệm hơi thở):
- Ngồi thẳng lưng, hai tay đặt trên đầu gối
- Nhắm mắt nhẹ, thả lỏng toàn thân
- Chú ý vào hơi thở vào-ra ở đầu mũi
- Hít vào biết hít vào, thở ra biết thở ra
- Khi tâm lang thang, nhẹ nhàng đưa về hơi thở
- Bắt đầu 5-10 phút mỗi ngày, tăng dần

2. THIỀN QUÁN (Vipassanā — Insight Meditation)

Mục đích: Thấy rõ bản chất thực tại — vô thường, khổ, vô ngã.

Bốn nền tảng chánh niệm (Satipaṭṭhāna):
a) Quán Thân (Kāyānupassanā):
   - Biết rõ mỗi bước đi, mỗi cử động
   - Quán 32 phần thân thể
   - Quán tứ đại: đất, nước, gió, lửa

b) Quán Thọ (Vedanānupassanā):
   - Nhận biết cảm giác: dễ chịu, khó chịu, trung tính
   - Không phản ứng, chỉ quan sát

c) Quán Tâm (Cittānupassanā):
   - Nhận biết trạng thái tâm: tham, sân, si
   - Biết tâm có tham → "tâm có tham"
   - Không đánh giá, chỉ nhận biết

d) Quán Pháp (Dhammānupassanā):
   - Quán Ngũ Triền Cái (5 chướng ngại)
   - Quán Ngũ Uẩn (5 tập hợp)
   - Quán Tứ Diệu Đế

3. THIỀN TỪBI (Mettā Bhāvanā — Loving-Kindness)

Phát nguyện:
"Nguyện cho tôi được an lạc, hạnh phúc, không bệnh tật, không nguy hiểm."
"Nguyện cho cha mẹ tôi được an lạc..."
"Nguyện cho thầy cô tôi được an lạc..."
"Nguyện cho bạn bè tôi được an lạc..."
"Nguyện cho kẻ thù tôi được an lạc..."
"Nguyện cho tất cả chúng sinh được an lạc, hạnh phúc, thoát khỏi khổ đau."

Thời biểu gợi ý:
- Sáng sớm: 20 phút Samatha
- Tối: 20 phút Vipassanā
- Bất kì lúc nào: 5 phút Mettā""",
    },
    # ─── Lịch sử Phật giáo ĐNÁ ───
    {
        "name": "phat_giao_dna_vi.txt",
        "lang": "vi",
        "category": "lich_su",
        "title": "Lịch Sử Phật Giáo Đông Nam Á",
        "tradition": "Chung",
        "content": """LỊCH SỬ PHẬT GIÁO ĐÔNG NAM Á

1. VIỆT NAM 🇻🇳
Phật giáo du nhập vào Việt Nam từ thế kỷ thứ 2 sau CN, qua hai con đường: từ Ấn Độ (qua biển) và từ Trung Quốc (qua đường bộ). Thiền tông phát triển mạnh dưới thời Lý-Trần (thế kỷ 11-14), với Thiền phái Trúc Lâm do Trần Nhân Tông sáng lập. Hiện nay Phật giáo là tôn giáo lớn nhất Việt Nam với khoảng 15-20 triệu tín đồ.

2. MYANMAR 🇲🇲
Myanmar là quốc gia Phật giáo Theravada lớn nhất thế giới. Phật giáo đến Myanmar từ thời vua Asoka (thế kỷ 3 TCN). Bagan là trung tâm Phật giáo vĩ đại với hơn 2,000 chùa tháp. 88% dân số theo Phật giáo, và truyền thống tu tập Vipassanā (Thiền Minh Sát) rất mạnh, với các thiền sư nổi tiếng như Mahasi Sayadaw và S.N. Goenka.

3. CAMBODIA 🇰🇭
97% dân số Cambodia theo Phật giáo Theravada. Angkor Wat ban đầu là đền Hindu, sau chuyển sang Phật giáo vào thế kỷ 12. Phật giáo bị tàn phá nặng nề dưới thời Khmer Đỏ (1975-1979), nhưng đã hồi phục mạnh mẽ. Mỗi thanh niên Cambodia thường đi tu ít nhất một lần trong đời.

4. LAOS 🇱🇦
66% dân số theo Phật giáo Theravada. Luang Prabang là cố đô và trung tâm Phật giáo, nổi tiếng với nghi lễ khất thực mỗi sáng (Tak Bat). That Luang ở Vientiane là biểu tượng quốc gia.

5. THAILAND 🇹🇭
93% dân số theo Phật giáo Theravada. Thái Lan chưa bao giờ bị thực dân hoá, Phật giáo được bảo tồn liên tục. Bangkok có hơn 400 chùa. Truyền thống forest monks (sư rừng) nổi tiếng thế giới. Nghĩa vụ tu tập 3 tháng mùa mưa (Vassa) vẫn duy trì.

6. SRI LANKA 🇱🇰
70% dân số theo Phật giáo Theravada. Nơi lưu giữ Tam Tạng Pali (Tipiṭaka) cổ nhất. Cây Bồ Đề tại Anuradhapura được trồng từ nhánh cây Bồ Đề gốc ở Bodh Gaya, Ấn Độ.

THỐNG KÊ PHẬT TỬ ĐÔNG NAM Á
- Tổng: ~170 triệu Phật tử
- Theravada: Myanmar, Cambodia, Laos, Thailand, Sri Lanka
- Mahayana: Việt Nam, Trung Quốc, Hàn Quốc, Nhật Bản
- Vajrayana: Tây Tạng, Bhutan, Mongolia""",
    },
]


def create_dharma_data(output_dir: str = "./data/dharma"):
    """Create Dharma scripture files for RAG testing."""
    import os, json

    os.makedirs(output_dir, exist_ok=True)

    created = []
    for doc in DHARMA_TEXTS:
        filepath = os.path.join(output_dir, doc["name"])
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(doc["content"])
        created.append({
            "file": doc["name"],
            "lang": doc["lang"],
            "category": doc["category"],
            "title": doc["title"],
            "tradition": doc.get("tradition", ""),
            "size": len(doc["content"]),
        })
        logger.info(f"🪷 Created: {doc['name']} ({doc['title']})")

    manifest = os.path.join(output_dir, "manifest.json")
    with open(manifest, "w", encoding="utf-8") as f:
        json.dump({"dharma_texts": created, "total": len(created)}, f, indent=2, ensure_ascii=False)

    logger.info(f"🪷 Created {len(created)} Dharma texts in {output_dir}")
    return created


def get_dharma_info():
    """Get info about available Dharma texts."""
    return {
        "total_texts": len(DHARMA_TEXTS),
        "languages": list(set(d["lang"] for d in DHARMA_TEXTS)),
        "categories": list(set(d["category"] for d in DHARMA_TEXTS)),
        "traditions": list(set(d.get("tradition", "") for d in DHARMA_TEXTS)),
        "texts": [
            {"name": d["name"], "lang": d["lang"], "title": d["title"],
             "tradition": d.get("tradition", ""), "category": d["category"]}
            for d in DHARMA_TEXTS
        ],
    }
