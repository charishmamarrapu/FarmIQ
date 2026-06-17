# FarmIQ – Week 2 Testing and Integration Report
## Project Name
FarmIQ – Multi-Agent Agricultural Advisory System
# 1. Objective
The objective of Week 2 testing was to verify the functionality, reliability, and integration of all FarmIQ agents and ensure that the Retrieval-Augmented Generation (RAG) pipeline correctly retrieves agricultural knowledge from the vector database.

The following components were tested:
* Crop Advisory Agent
* Market Price Agent
* Weather Impact Agent
* Pest & Disease Agent
* RAG Pipeline
* Orchestrator Integration
---
# 2. Environment Setup
## Software Used
* Python 3.11
* VS Code
* ChromaDB
* LangChain
* Google Gemini API
* OpenWeather API
## API Configuration
* Google Gemini API Key configured
* OpenWeather API Key configured
---
# 3. RAG Pipeline Testing
## Command Executed
```bash
python src\rag\build_pipeline.py
```
## Results
### PDF Data Processing

| Source    | Pages Loaded | Chunks Created |
| --------- | ------------ | -------------- |
| PDF Set 1 | 680          | 2905           |
| PDF Set 2 | 72           | 425            |
| PDF Set 3 | 863          | 2415           |
| PDF Set 4 | 225          | 1519           |
### CSV Data Processing
| Dataset              | Records |
| -------------------- | ------- |
| Crop Production Data | 17      |
| Mandi Price Data     | 5155    |
### Final Statistics
* Total Chunks Embedded: 12,436
* Vector Store Created Successfully
* Storage Location: `vectorstore/`
## Status
PASS
---
# 4. Retrieval Testing
## Command Executed
```bash
python src\rag\test_retrieval.py
```
## Test Queries
1. Best crop to grow in Guntur district Kharif season
2. Fertilizer recommendation for paddy cultivation
3. Yellow leaves on tomato plant disease treatment
4. Current price of paddy in Krishna district mandi
5. Impact of heavy rainfall on cotton crop
6. PM-KISAN scheme eligibility for small farmers
7. Pest control for rice crop in AP
## Results
* Retrieval system loaded successfully.
* Vector store accessed successfully.
* Queries executed without runtime failures.
## Status
PASS
---
# 5. Crop Advisory Agent Testing
## Command Executed
```bash
python src\agents\crop_advisory_agent.py
```
## Test Questions
1. What are Kharif crops?
2. How to grow paddy crop?
3. What is the irrigation method for rice?
4. Fertilizer for cotton cultivation
## Observations
* Agent loaded successfully.
* Retrieved relevant agricultural information.
* Generated farmer-friendly responses.
* Successfully accessed RAG knowledge base.
## Sample Output
Kharif crops identified included:
* Rice
* Pearl Millet (Bajra)
* Pigeonpea
* Mustard
* Cowpea
* Greengram
## Status
PASS
---
# 6. Market Price Agent Testing
## Command Executed
```bash
python src\agents\market_price_agent.py
```
## Test Scenario
Query regarding Paddy prices in Krishna district.
## Observations
* Agent executed successfully.
* Generated market advisory.
* Historical mandi data retrieved successfully.
* Sell/Hold recommendation generated.
## Issue Identified
```text
Mandi API error:
Expecting value: line 1 column 1 (char 0)
```
The live mandi API response could not be parsed.
## Impact
* Live market prices unavailable.
* Historical data used as fallback.
## Status
PARTIAL PASS
---
# 7. Weather Impact Agent Testing
## Test Scenario
Cotton crop weather advisory for Guntur district.
## Observations
* Weather forecast successfully processed.
* Temperature analysis generated.
* Crop-specific recommendations provided.
* Irrigation suggestions generated.
## Sample Recommendations
* Increase irrigation frequency.
* Conserve soil moisture.
* Apply mulch where possible.
* Avoid field operations during peak heat.
## Issue Identified
```text
429 ResourceExhausted
Quota exceeded
```
Google Gemini free-tier request limit exceeded during testing.
## Impact
Temporary delay in response generation.
## Status
PASS
---
# 8. Pest & Disease Agent Testing
## Command Executed
```bash
python src\agents\pest_disease_agent.py
```
## Test Scenario
Tomato leaves turning yellow and curling.
## Observations
* Agent successfully identified probable fungal disease.
* Generated disease management recommendations.
* Retrieved information from agricultural documents.
## Sample Output
Possible disease:
* Fusarium Wilt
Recommended treatment:
* Seed treatment at 20 g/ml per kg of seed.
## Status
PASS
---
# 9. Orchestrator Integration Testing
## Command Executed
```bash
python src\agents\orchestrator.py
```
## Results
### Agent Initialization
```text
Loading all agents...
All 4 agents ready!
```
### Routing Verification
| Query Type    | Routed Agent         | Status |
| ------------- | -------------------- | ------ |
| Crop Query    | Crop Advisory Agent  | PASS   |
| Market Query  | Market Price Agent   | PASS   |
| Weather Query | Weather Impact Agent | PASS   |
| Pest Query    | Pest & Disease Agent | PASS   |
## Observations
* All agents loaded successfully.
* Routing logic worked correctly.
* Queries reached appropriate agents.
* Responses generated successfully.
## Status
PASS
---
# 10. Issues Encountered
## Issue 1 – Chroma Telemetry Warning
```text
capture() takes 1 positional argument but 3 were given
```
Impact:
No impact on system functionality.
Severity:
Low
---
## Issue 2 – Mandi API Failure
```text
Expecting value: line 1 column 1 (char 0)
```
Impact:
Live market data unavailable.
Severity:
Medium
---
## Issue 3 – Gemini API Rate Limit
```text
429 ResourceExhausted
Quota exceeded
```
Impact:
Temporary response delays.
Severity:
Medium
---
# 11. Overall Assessment
The FarmIQ system successfully completed Week 2 testing.
Achievements:
* RAG pipeline built successfully.
* Vector database created successfully.
* Crop Advisory Agent functioning correctly.
* Market Price Agent functioning with fallback mechanism.
* Weather Impact Agent generating weather advisories.
* Pest & Disease Agent generating disease recommendations.
* Orchestrator integration successful.
* Agent routing verified.
## Overall Result
PASS
System is functional and ready for further development and optimization in subsequent project phases.
---
# Tested By
**V. S. Hasini Reddy**
Testing & Integration Engineer
FarmIQ – Team 5