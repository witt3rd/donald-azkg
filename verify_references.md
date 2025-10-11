---
tags: [reference, verification]
---

# References and Citations Checker Process

1. **Locate References**  
   - Read the document to identify reference markers (e.g., "Claim X [12]").  
   - Note the claim or text being referenced (e.g., "Claim X") and its location.

2. **Find Citations**  
   - Search for the references section or footnotes.  
   - Match each marker (e.g., "[12]") to its citation entry (e.g., "[12] <citation>").  
   - *Failure:* Flag if a citation is missing.

3. **Research Citations**  
   - For each citation:  
     - If online, fetch the source.  
     - If not online, research it using web search or tools like Perplexity.  
   - *Failure:* Flag if the source can’t be found or accessed.

4. **Verify Support**  
   - Check if the cited source directly or plausibly supports the referenced claim.  
   - *Failure:* Flag if the source does not support the claim (e.g., "Claim X" is about robotics, but the source is about marine biology).

5. **Report Issues**  
   - Compile a list of failures: missing citations, inaccessible sources, or sources that don’t support claims.