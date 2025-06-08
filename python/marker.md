## How to Use Marker to Convert arXiv PDFs to Markdown

**Summary**
Marker is a Python-based tool optimized for converting arXiv PDFs (and other documents) to structured Markdown, JSON, or HTML while preserving tables, equations, and formatting. Below is a step-by-step guide for installation, configuration, and conversion.

---

### **1. Installation**

```bash
# Install Marker with PyTorch (CPU/GPU support)
pip install marker-pdf
```

- **GPU Acceleration:** For NVIDIA GPUs, install CUDA-compatible PyTorch first for faster processing[1][4].
- **GUI Option:** Install the Streamlit-based GUI for a visual interface[2]:

  ```bash
  git clone https://github.com/VikParuchuri/marker
  cd marker/streamlit
  pip install -r requirements.txt
  streamlit run app.py
  ```

---

### **2. Basic Conversion (CLI)**

```bash
# Convert an arXiv PDF to Markdown
marker /path/to/arxiv_paper.pdf output.md
```

**Key Flags:**

- `--max_pages 50`: Limit pages processed
- `--lang en`: Specify language (supports 20+ languages)
- `--use_llm`: Enable hybrid mode with Gemini/LLM for higher accuracy[1][5]

---

### **3. Handling arXiv PDFs**

**Special Considerations:**

- **Equations:** Marker automatically converts most equations to LaTeX[4][5].
- **References:** Extracts and formats citations[2].
- **Multi-column Layouts:** Uses layout detection to maintain reading order[4].

**Example Workflow:**

```bash
# Download arXiv PDF
wget https://arxiv.org/pdf/2401.12345.pdf -O paper.pdf

# Convert with hybrid LLM mode (requires Gemini API key)
marker paper.pdf output.md --use_llm --llm_model gemini-2.0-flash
```

---

### **4. Advanced Features**

| Feature              | Command/Usage                          | Use Case                          |
| -------------------- | -------------------------------------- | --------------------------------- |
| Batch Processing     | `marker *.pdf --output_dir ./markdown` | Convert multiple papers at once   |
| Image Extraction     | `--extract_images`                     | Save figures alongside Markdown   |
| JSON Output          | `--output_format json`                 | Structured data for RAG pipelines |
| Page Range Selection | `--start_page 3 --end_page 10`         | Process specific sections         |

---

### **5. Troubleshooting**

**Common Issues:**

- **OCR Failures:** Add `--ocr_engine surya` for better handwriting/diagram support[4].
- **Formatting Errors:** Use `--use_llm` to fix table merges and inline math[1].
- **GPU Memory Errors:** Reduce batch size with `--batch_multiplier 2`[4].

---

### **6. Performance Benchmarks**

| Hardware        | Speed (Pages/Second) | Accuracy\* |
| --------------- | -------------------- | ---------- |
| NVIDIA H100     | 122                  | 98%        |
| Mac M2 Ultra    | 45                   | 95%        |
| CPU (i9-13900K) | 12                   | 92%        |

\*Accuracy measured on arXiv papers with tables/equations[1][5].

---

**Best Practices for arXiv Papers:**

1. Prefer PDFs from `arxiv.org/pdf/` over HTML/abstract pages.
2. Use `--use_llm` flag for papers with complex cross-page tables.
3. Combine with Firecrawl to first fetch the PDF URL before conversion.

For full documentation, see [Marker’s GitHub repository][https://github.com/VikParuchuri/marker](1)[4].

[1] <https://github.com/VikParuchuri/marker>
[2] <https://www.youtube.com/watch?v=ROqpVzEzRIQ>
[3] <https://blog.aitoolhouse.com/marker-a-new-python-based-library-that-converts-pdf-to-markdown-quickly-and-accurately/>
[4] <https://pypi.org/project/marker-pdf/0.3.2/>
[5] <https://www.reddit.com/r/llm_updated/comments/19dtd7z/marker_a_new_pdf_converter_suitable_for_rag/>
[6] <https://github.com/cuuupid/cog-marker>
[7] <https://news.ycombinator.com/item?id=38482007>
[8] <https://github.com/mustafaquraish/marker/blob/master/README.md>
[9] <https://docs.llamaindex.ai/en/stable/api_reference/readers/arxiv/>
[10] <https://arxiv.org/html/2409.05137v1>
