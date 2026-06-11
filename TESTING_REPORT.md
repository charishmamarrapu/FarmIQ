# FarmIQ Testing Report
## Harvest IQ
FarmIQ – Multi-Agent Agricultural Advisory System using RAG

## Pipeline Test
### Objective
To verify that the RAG pipeline successfully loads agricultural data, creates chunks, generates embeddings, and stores them in a vector database.
### Execution
Command:
```bash
python src\rag\build_pipeline.py
```
### Results
* Loaded 680 pages from PDFs
* Created 2905 chunks
* Loaded 72 pages from PDFs
* Created 425 chunks
* Loaded 863 pages from PDFs
* Created 2415 chunks
* Loaded 225 pages from PDFs
* Created 1519 chunks
* Loaded 17 rows from crop production CSV
* Loaded 5155 rows from mandi prices CSV
* Total chunks embedded: 12436
* Vector store created successfully
* Vector store saved to `vectorstore/`
* Pipeline completed successfully
### Status
PASS 
---
## Retrieval Test
### Objective
To verify that the vector store can retrieve relevant information for agricultural queries.
### Execution
Command:
```bash
python src\rag\test_retrieval.py
```
### Test Cases
#### Test Case 1
Question:
Best crop to grow in Guntur district Kharif season
Result:
Relevant crop guide information retrieved.
Source:
Field Crop Kharif PDF
Status:
PASS 
---
#### Test Case 2
Question:
Fertilizer recommendation for paddy cultivation
Result:
Relevant fertilizer and agronomy information retrieved.
Source:
Principles of Agronomy PDF
Status:
PASS 
---
#### Test Case 3
Question:
Yellow leaves on tomato plant disease treatment
Result:
Agriculture-related information retrieved from the knowledge base.
Status:
PASS 
---
#### Test Case 4
Question:
Current price of paddy in Krishna district mandi
Result:
Price-related agricultural information retrieved.
Status:
PASS 
---
#### Test Case 5
Question:
Impact of heavy rainfall on cotton crop
Result:
Crop damage and weather impact information retrieved.
Source:
PMFBY Operational Guide PDF
Status:
PASS 
---
#### Test Case 6
Question:
PM-KISAN scheme eligibility for small farmers
Result:
PM-KISAN scheme guidelines retrieved successfully.
Source:
PM-KISAN Guidelines PDF
Status:
PASS ✅
---
#### Test Case 7
Question:
Pest control for rice crop in AP
Result:
Pest control related information retrieved.
Source:
Field Crop Kharif PDF
Status:
PASS 
---
## Integration Check
### Objective
To verify the complete FarmIQ RAG workflow.
### Workflow Verification
PDF Data & CSV Data
↓
Data Loading
↓
Chunking
↓
Embeddings Generation
↓
Vector Store Creation
↓
Retrieval
↓
Answer Generation
### Verification Details
* PDF documents loaded successfully
* CSV datasets loaded successfully
* Text chunks created successfully
* Embeddings generated successfully
* Vector database created successfully
* Retrieval executed successfully
* Relevant answers returned for user queries
### Status
PASS 
---
## Final Result
The FarmIQ RAG pipeline was successfully tested and validated.
* Data Loading: PASS ✅
* Chunking: PASS ✅
* Embedding Generation: PASS ✅
* Vector Store Creation: PASS ✅
* Retrieval Testing: PASS ✅
* Integration Testing: PASS ✅
### Overall Project Status
🎉 PASS – FarmIQ RAG Pipeline is functioning successfully and ready for integration with the multi-agent agricultural advisory system.