"""
Test Data Downloader — Fetches sample documents from the internet for RAG testing.

Downloads: PDF, DOCX, TXT files in Vietnamese, English, and other SEA languages.
Usage: python -m app.utils.test_data_loader
"""

import os
import json
import asyncio
import logging
import httpx

logger = logging.getLogger("budai.testdata")

# ═══════════════════════════════════════════════════════
#  TEST DOCUMENTS — Public domain / CC licensed
# ═══════════════════════════════════════════════════════
TEST_DOCUMENTS = [
    # ─── Vietnamese ───
    {
        "name": "vietnam_constitution_vi.txt",
        "lang": "vi",
        "category": "legal",
        "description": "Hiến pháp Việt Nam 2013 (trích)",
        "content": """HIẾN PHÁP NƯỚC CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM

Điều 1. Nước Cộng hòa xã hội chủ nghĩa Việt Nam là một nước độc lập, có chủ quyền, thống nhất và toàn vẹn lãnh thổ, bao gồm đất liền, hải đảo, vùng biển và vùng trời.

Điều 2. Nhà nước Cộng hòa xã hội chủ nghĩa Việt Nam là nhà nước pháp quyền xã hội chủ nghĩa của Nhân dân, do Nhân dân, vì Nhân dân. Nước Cộng hòa xã hội chủ nghĩa Việt Nam do Nhân dân làm chủ; tất cả quyền lực nhà nước thuộc về Nhân dân.

Điều 3. Nhà nước bảo đảm và phát huy quyền làm chủ của Nhân dân; công nhận, tôn trọng, bảo vệ và bảo đảm quyền con người, quyền công dân.

Điều 14. Ở nước Cộng hòa xã hội chủ nghĩa Việt Nam, các quyền con người, quyền công dân về chính trị, dân sự, kinh tế, văn hóa, xã hội được công nhận, tôn trọng, bảo vệ, bảo đảm theo Hiến pháp và pháp luật.

Điều 15. Quyền công dân không tách rời nghĩa vụ công dân. Mọi người có nghĩa vụ tôn trọng quyền của người khác. Công dân có trách nhiệm thực hiện nghĩa vụ đối với Nhà nước và xã hội.

Điều 16. Mọi người đều bình đẳng trước pháp luật. Không ai bị phân biệt đối xử trong đời sống chính trị, dân sự, kinh tế, văn hóa, xã hội.""",
    },
    {
        "name": "contract_template_vi.txt",
        "lang": "vi",
        "category": "business",
        "description": "Mẫu hợp đồng thuê nhà tiếng Việt",
        "content": """HỢP ĐỒNG THUÊ NHÀ Ở

Số: ___/HĐTN

Hôm nay, ngày ___ tháng ___ năm 2026, tại ___

BÊN CHO THUÊ (Bên A):
- Họ và tên: ___
- CMND/CCCD: ___
- Địa chỉ: ___

BÊN THUÊ (Bên B):
- Họ và tên: ___
- CMND/CCCD: ___
- Địa chỉ: ___

ĐIỀU 1. ĐỐI TƯỢNG CHO THUÊ
Bên A đồng ý cho Bên B thuê căn nhà tại địa chỉ: ___
Diện tích sử dụng: ___ m2
Tình trạng nhà: Đầy đủ nội thất cơ bản

ĐIỀU 2. GIÁ THUÊ VÀ PHƯƠNG THỨC THANH TOÁN
- Giá thuê: ___ đồng/tháng
- Tiền đặt cọc: ___ đồng (tương đương ___ tháng tiền thuê)
- Phương thức: Thanh toán vào ngày ___ hàng tháng
- Tiền điện: Theo giá điện sinh hoạt nhà nước
- Tiền nước: ___ đồng/m3
- Internet/cáp: Bên B tự chi trả

ĐIỀU 3. THỜI HẠN THUÊ
- Thời hạn: ___ tháng
- Từ ngày: ___ đến ngày: ___
- Gia hạn: Hai bên thỏa thuận trước 30 ngày

ĐIỀU 4. QUYỀN VÀ NGHĨA VỤ CỦA BÊN A
- Giao nhà đúng thời hạn và tình trạng đã thỏa thuận
- Bảo đảm quyền sử dụng ổn định cho Bên B
- Sửa chữa những hư hỏng lớn do hao mòn tự nhiên

ĐIỀU 5. QUYỀN VÀ NGHĨA VỤ CỦA BÊN B
- Sử dụng nhà đúng mục đích đã thỏa thuận
- Thanh toán đầy đủ, đúng hạn các khoản phí
- Bảo quản nhà ở, không được tự ý cải tạo
- Trả lại nhà đúng thời hạn và tình trạng ban đầu""",
    },
    {
        "name": "tech_overview_vi.txt",
        "lang": "vi",
        "category": "technology",
        "description": "Tổng quan AI và Machine Learning",
        "content": """TỔNG QUAN VỀ TRÍ TUỆ NHÂN TẠO VÀ HỌC MÁY

1. Giới thiệu
Trí tuệ nhân tạo (AI - Artificial Intelligence) là lĩnh vực khoa học máy tính nhằm tạo ra các hệ thống có khả năng thực hiện các nhiệm vụ đòi hỏi trí thông minh con người. Học máy (Machine Learning) là một nhánh của AI, cho phép máy tính học từ dữ liệu mà không cần lập trình rõ ràng.

2. Các loại học máy
- Học có giám sát (Supervised Learning): Mô hình được huấn luyện trên dữ liệu có nhãn
- Học không giám sát (Unsupervised Learning): Mô hình tự tìm cấu trúc trong dữ liệu
- Học tăng cường (Reinforcement Learning): Mô hình học qua tương tác với môi trường

3. Deep Learning
Học sâu sử dụng mạng nơ-ron nhiều lớp để xử lý dữ liệu phức tạp. Các kiến trúc phổ biến:
- CNN (Convolutional Neural Network): Xử lý ảnh
- RNN/LSTM: Xử lý chuỗi, ngôn ngữ
- Transformer: Kiến trúc hiện đại cho NLP (BERT, GPT)
- Diffusion Models: Sinh ảnh (Stable Diffusion, DALL-E)

4. Ứng dụng AI tại Việt Nam
- Ngân hàng: Phát hiện gian lận, credit scoring
- Y tế: Chẩn đoán hình ảnh y khoa
- Nông nghiệp: Dự đoán sâu bệnh, năng suất
- Giao thông: Xe tự lái, tối ưu lộ trình
- Giáo dục: Hệ thống học cá nhân hóa""",
    },
    # ─── English ───
    {
        "name": "asean_agreement_en.txt",
        "lang": "en",
        "category": "legal",
        "description": "ASEAN Charter Summary",
        "content": """CHARTER OF THE ASSOCIATION OF SOUTHEAST ASIAN NATIONS (Summary)

PREAMBLE
The peoples and Member States of ASEAN, committed to intensifying community building through enhanced regional cooperation and integration.

ARTICLE 1 - PURPOSES
1. To maintain and enhance peace, security and stability in the region.
2. To enhance regional resilience through political, security, economic and socio-cultural cooperation.
3. To preserve Southeast Asia as a Nuclear Weapon-Free Zone.
4. To create a single market and production base.
5. To alleviate poverty and narrow the development gap within ASEAN.

ARTICLE 2 - PRINCIPLES
ASEAN and its Member States shall act in accordance with:
(a) Respect for the independence, sovereignty, equality, territorial integrity and national identity
(b) Non-interference in the internal affairs of ASEAN Member States
(c) Adherence to the rule of law, good governance, democracy and constitutional government
(d) Respect for fundamental freedoms and human rights

MEMBER STATES
1. Brunei Darussalam
2. Kingdom of Cambodia
3. Republic of Indonesia
4. Lao People's Democratic Republic
5. Malaysia
6. Republic of the Union of Myanmar
7. Republic of the Philippines
8. Republic of Singapore
9. Kingdom of Thailand
10. Socialist Republic of Viet Nam""",
    },
    {
        "name": "ai_cloud_computing_en.txt",
        "lang": "en",
        "category": "technology",
        "description": "AI Cloud Computing Overview",
        "content": """AI CLOUD COMPUTING: A COMPREHENSIVE GUIDE (2025)

1. INTRODUCTION
Cloud computing has revolutionized how organizations deploy and scale AI workloads. The convergence of GPU acceleration, serverless architectures, and managed AI services has democratized access to powerful computing resources.

2. GPU CLOUD PROVIDERS
Major providers offering GPU instances for AI/ML:

2.1 RunPod
- H100: $2.49/hr (community), $3.29/hr (secure)
- A100 80GB: $1.64/hr
- A40 48GB: $0.39/hr
- RTX 4090: $0.44/hr
Best for: Development, fine-tuning, inference

2.2 TensorDock
- RTX 4090: $0.35/hr
- A100 40GB: $1.10/hr
- L40S: $0.75/hr
Best for: Budget-conscious deployments

2.3 Lambda Cloud
- H100: $2.49/hr
- H200: $3.99/hr
Best for: Large-scale training

3. COST OPTIMIZATION STRATEGIES
- Use spot/interruptible instances for training (50-80% savings)
- Right-size GPU selection (don't use H100 for inference)
- Implement auto-scaling for variable workloads
- Use quantized models (4-bit, 8-bit) to reduce VRAM
- Batch processing during off-peak hours

4. DEPLOYMENT PATTERNS
- Serverless GPU: Pay per inference call
- Dedicated instances: Consistent performance
- Multi-GPU: For large model training
- Hybrid: Local development + cloud deployment""",
    },
    # ─── Myanmar (Burmese) ───
    {
        "name": "myanmar_sample.txt",
        "lang": "my",
        "category": "general",
        "description": "Myanmar text sample for OCR/RAG testing",
        "content": """မြန်မာနိုင်ငံ၏ သမိုင်းအကျဉ်း

မြန်မာနိုင်ငံသည် အရှေ့တောင်အာရှတွင် တည်ရှိသော နိုင်ငံတစ်ခုဖြစ်သည်။ ၁၉၄၈ ခုနှစ်တွင် ဗြိတိသျှကိုလိုနီအုပ်ချုပ်မှုမှ လွတ်လပ်ရေးရရှိခဲ့သည်။

မြန်မာနိုင်ငံသည် တောင်အာရှနှင့် အရှေ့တောင်အာရှကြားတွင် တည်ရှိပြီး ဘင်္ဂလားဒေ့ရှ်၊ အိန္ဒိယ၊ တရုတ်၊ လာအိုနှင့် ထိုင်းတို့နှင့် နယ်နိမိတ်ချင်း ထိစပ်နေသည်။

မြို့တော်: နေပြည်တော်
လူဦးရေ: သန်း ၅၄ ခန့်
ဧရိယာ: ၆၇၆,၅၇၈ စတုရန်း ကီလိုမီတာ
ဘာသာစကား: မြန်မာဘာသာ""",
    },
    # ─── Khmer (Cambodian) ───
    {
        "name": "khmer_sample.txt",
        "lang": "km",
        "category": "general",
        "description": "Khmer text sample for OCR/RAG testing",
        "content": """ប្រវត្តិសង្ខេបនៃប្រទេសកម្ពុជា

ព្រះរាជាណាចក្រកម្ពុជា ជាប្រទេសមួយស្ថិតនៅក្នុងអាស៊ីអាគ្នេយ៍។ រាជធានីគឺភ្នំពេញ។

កម្ពុជាមានប្រវត org្តិយូរអង្វែង ជាពិសេសអរិយធម៌អង្គរដែលជារាជវង្សដ៏ខ្លាំងក្លាមួយនៅក្នុងអាស៊ី។ ប្រាសាទអង្គរវត្ត ជាប្រាសាទធំជាងគេបំផុតក្នុងពិភពលោក។

ទីក្រុង: ភ្នំពេញ
ប្រជាជន: ១៧ លាន
ភាសា: ភាសាខ្មែរ""",
    },
    # ─── Lao ───
    {
        "name": "lao_sample.txt",
        "lang": "lo",
        "category": "general",
        "description": "Lao text sample for OCR/RAG testing",
        "content": """ປະຫວັດສາດຫຍໍ້ຂອງປະເທດລາວ

ສາທາລະນະລັດ ປະຊາທິປະໄຕ ປະຊາຊົນລາວ ເປັນປະເທດທີ່ຕັ້ງຢູ່ໃນເຂດອາຊີຕາເວັນອອກສ່ຽງໃຕ້。

ນະຄອນຫຼວງ: ວຽງຈັນ
ປະຊາກອນ: ປະມານ ໗ ລ້ານຄົນ
ພາສາ: ພາສາລາວ

ລາວເປັນປະເທດທີ່ບໍ່ມີທາງອອກທະເລ ແລະ ມີຊາຍແດນຕິດກັບ ຈີນ, ມຽນມາ, ຫວຽດນາມ, ກຳປູເຈຍ ແລະ ໄທ.""",
    },
    # ─── Technical Documents ───
    {
        "name": "rag_architecture_en.txt",
        "lang": "en",
        "category": "technology",
        "description": "RAG Architecture Best Practices",
        "content": """RETRIEVAL-AUGMENTED GENERATION (RAG) ARCHITECTURE GUIDE

1. DOCUMENT PROCESSING PIPELINE
- Ingestion: Accept PDF, DOCX, HTML, Markdown, CSV
- Chunking: Recursive text splitting (512-1024 tokens)
- Embedding: Convert chunks to dense vectors
- Indexing: Store in vector database with metadata

2. CHUNKING STRATEGIES
a) Fixed-size chunks: Simple but may break context
b) Recursive splitting: Split on paragraphs → sentences → words
c) Semantic chunking: Use embeddings to find natural boundaries
d) Document-aware: Respect headings, tables, lists

3. RETRIEVAL STRATEGIES
a) Dense retrieval: Cosine similarity on embeddings
b) Sparse retrieval: BM25, TF-IDF keyword matching
c) Hybrid: Combine dense + sparse (Reciprocal Rank Fusion)
d) Re-ranking: Cross-encoder scoring after initial retrieval

4. GENERATION
- Context window management: Keep within model limits
- Source attribution: Map generated sentences to source chunks
- Hallucination detection: Verify claims against retrieved context
- Multi-turn: Maintain conversation history for follow-ups

5. EVALUATION METRICS
- Retrieval: Recall@k, MRR, NDCG
- Generation: RAGAS (Faithfulness, Relevance, Context Recall)
- End-to-end: User satisfaction, task completion rate

6. PRODUCTION CONSIDERATIONS
- Embedding model selection: Balance quality vs cost vs latency
- Vector DB scaling: Sharding, replication, filtering
- Caching: Cache frequent queries and embeddings
- Monitoring: Track latency, cost, error rates per request""",
    },
    {
        "name": "viettel_public_services.txt",
        "lang": "vi",
        "category": "telecom",
        "description": "Giới thiệu dịch vụ viễn thông (mẫu test)",
        "content": """TỔNG QUAN DỊCH VỤ VIỄN THÔNG TẠI VIỆT NAM

1. DỊCH VỤ DI ĐỘNG
Thị trường viễn thông di động Việt Nam có 3 nhà mạng lớn:
- Viettel: Thị phần ~55%, phủ sóng 4G/5G toàn quốc
- VNPT (VinaPhone): Thị phần ~25%
- Mobifone: Thị phần ~18%

Gói cước phổ biến:
- Gói data: 3GB/ngày từ 3,000đ/ngày
- Gói thoại: 1,500 phút nội mạng từ 50,000đ/tháng
- Gói combo: Data + thoại + SMS từ 77,000đ/tháng

2. DỊCH VỤ INTERNET CÁP QUANG (FTTH)
- Tốc độ: 50Mbps - 1Gbps
- Giá: 165,000đ - 500,000đ/tháng
- Phủ sóng: 63/63 tỉnh thành

3. DỊCH VỤ SỐ / CLOUD
- Cloud Computing: IaaS, PaaS, SaaS
- AI Platform: Nhận diện giọng nói, OCR, chatbot
- IoT Platform: Smart city, smart factory
- Data Center: Tier 3, Tier 4

4. XU HƯỚNG PHÁT TRIỂN
- 5G: Triển khai thương mại toàn quốc
- AI/ML: Tích hợp vào mọi dịch vụ
- Blockchain: Xác thực, bảo mật
- Edge Computing: Giảm độ trễ, tăng hiệu suất""",
    },
]


async def download_test_data(output_dir: str = "./data/test_documents"):
    """Create test documents from built-in templates."""
    os.makedirs(output_dir, exist_ok=True)

    created = []
    for doc in TEST_DOCUMENTS:
        filepath = os.path.join(output_dir, doc["name"])
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(doc["content"])

        created.append({
            "file": doc["name"],
            "lang": doc["lang"],
            "category": doc["category"],
            "description": doc["description"],
            "size": len(doc["content"]),
        })
        logger.info(f"📄 Created: {doc['name']} ({doc['lang']}, {doc['category']})")

    # Save manifest
    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({"documents": created, "total": len(created)}, f, indent=2, ensure_ascii=False)

    logger.info(f"✅ Created {len(created)} test documents in {output_dir}")
    return created


def get_test_data_info():
    """Get info about available test data."""
    return {
        "total_documents": len(TEST_DOCUMENTS),
        "languages": list(set(d["lang"] for d in TEST_DOCUMENTS)),
        "categories": list(set(d["category"] for d in TEST_DOCUMENTS)),
        "documents": [
            {"name": d["name"], "lang": d["lang"], "category": d["category"],
             "description": d["description"]}
            for d in TEST_DOCUMENTS
        ],
    }


# Run standalone
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(download_test_data())
    print("✅ Done! Test data created in ./data/test_documents/")
