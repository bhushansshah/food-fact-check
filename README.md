# Fact Verification of Food Product Claims with Language Models

## Project Action Plan

This project focuses on using Language Models (LLMs/SLMs) for the automatic verification and explanation of claims made on packaged food products using structured product data from Open Food Facts and similar datasets. Applications span both end-user assistants and backend automation for food platforms.

---

## **Action Plan**

### 1. **Labelled Dataset Creation**
- Identify and curate common types of claims made on food products (e.g., "gluten free", "low sugar", "rich in protein").
- Build a labeled dataset with both **positive samples** (where claims are true) and **negative samples** (where claims are misleading/false).
- Ensure diversity in claims, product categories, and brands.

### 2. **Zero-Shot LLM Benchmarking**
- Select and compare several popular LLMs for zero-shot performance on fact verification (e.g., GPT-4, Llama-2/3, Mistral, etc.).
- Evaluate on accuracy, explanation quality, and reasoning traces.

### 3. **Feasible LLMs/SLMs for Finetuning**
- Identify LLMs and SLMs suitable for finetuning within Google Colab T4 GPU constraints (e.g., Mistral-3B/4B, Phi-2, Gemma-2B, Llama-3 1.2B).
- Prioritize models that support parameter-efficient methods (LoRA/QLoRA).

### 4. **Instruction Finetuning Methods**
- Outline and implement instruction finetuning using methods such as:
  - LoRA (Low-Rank Adaptation)
  - QLoRA (Quantized LoRA)
  - Full SFT (for smallest models)
- Use Hugging Face Transformers, PEFT, and Accelerate libraries.

### 5. **Domain Adaptation Finetuning**
- Select relevant datasets for domain adaptation (e.g., food claim datasets, ingredient-to-clinical datasets).
- Finetune LLMs/SLMs on these before the main instruction task.

### 6. **Instruction Finetuning Post-Adaption**
- Apply the chosen instruction finetuning pipeline after domain adaptation to maximize real-world performance.

### 7. **Dual Use Case Evaluation**
- **User-centric Use Case:** Provide only product name/brand and prompt the model as an assistant for end-users (simulating consumer interaction).
- **Backend Automation Use Case:** Include all available product details (structured/natural language) for automated fact-checking.
- Compare models’ factual accuracy and explanation quality in both settings.

### 8. **Comprehensive Error & Robustness Analysis**
- Analyze model errors, including hallucinations, failure to ground predictions, and difficulty with rare/ambiguous claims.
- Optionally, compare in-context (few-shot) vs. instruction-tuned approaches.
- Optionally, include a simple classical (non-LLM) baseline for reference.

### 9. **Human Evaluation (Optional but Valuable)**
- Collect human judgments on correctness and justification quality for a sample of model outputs.

### 10. **Runtime and Resource Evaluation**
- Track and report on memory use, training time, and inference cost for each model/finetuning setup to support deployment considerations.

---

## **Future Work**

### **Generalization to Unseen Claims and Product Types**
- Explore model performance on new claim categories, rare product types, or domains (e.g., cosmetics, supplements) via zero-shot, few-shot, or transfer learning.
- Investigate the use of multimodal input (e.g., packaging images + OCRed claims) for claim extraction and verification in a unified pipeline.

---

## **Potential Impact**
- Improved automated claim verification for regulatory compliance and consumer trust.
- Enhanced LLM-based assistants for health, dietary, and transparency use-cases in food-tech.
- Strong foundation for further research in explainable, responsible, and robust LLMs for scientific and legal domains.

---

*This README reflects an evolving project strategy and will be updated as new results and insights emerge.*
